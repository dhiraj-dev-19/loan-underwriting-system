"""
scoring_service.py - Production-ready API contract functions for Person B's
Streamlit dashboard.

Functions:
    score_applicant(applicant_dict)       -> float  (0.0 – 1.0 risk probability)
    get_cohort_default_rate(applicant_dict) -> float  (0.0 – 100.0 percentage)

Contract input dict keys:
    income, debt_ratio, credit_lines, delinquencies, dependents
"""

import os
import sys
import json
import time
import joblib
import numpy as np
import pandas as pd

# -- Make imports work whether run as a module or as a standalone script --
_SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
_PROJECT_ROOT = os.path.abspath(os.path.join(_SCRIPT_DIR, "..", ".."))
if _PROJECT_ROOT not in sys.path:
    sys.path.insert(0, _PROJECT_ROOT)

from dotenv import load_dotenv
load_dotenv(os.path.join(_PROJECT_ROOT, ".env"))

from src.person_a.column_mapping import ALL_MODEL_FEATURES, CONTRACT_FEATURES

# ---------------------------------------------------------------------
# Paths & Configuration
# ---------------------------------------------------------------------
MODEL_PATH = os.path.join(_PROJECT_ROOT, "data", "model.pkl")
CLEAN_CSV = os.path.join(_PROJECT_ROOT, "data", "clean_data.csv")
CACHE_PATH = os.path.join(_PROJECT_ROOT, "data", "cohort_cache.json")

BQ_DATASET = os.environ.get("BQ_DATASET", "loan_underwriting")
BQ_TABLE = os.environ.get("BQ_TABLE", "loan_applicants")
BQ_QUERY_TIMEOUT_SECONDS = float(os.environ.get("BQ_QUERY_TIMEOUT", "5.0"))

# ---------------------------------------------------------------------
# Model loading (cached at module level for performance)
# ---------------------------------------------------------------------
_model = None


def _get_model():
    """Lazy-load the trained model (cached after first call)."""
    global _model
    if _model is None:
        if not os.path.exists(MODEL_PATH):
            raise FileNotFoundError(
                f"Model file not found at {MODEL_PATH}. Run train.py first."
            )
        _model = joblib.load(MODEL_PATH)
    return _model


# ---------------------------------------------------------------------
# Default / median values for features not in the 5-field contract
# These are computed from the training data and hard-coded here for
# inference speed; they only need updating if the dataset changes.
# ---------------------------------------------------------------------
_FEATURE_DEFAULTS = {
    # Contract features (will be overridden by applicant_dict)
    "income": 5400.0,
    "debt_ratio": 0.35,
    "credit_lines": 8,
    "delinquencies": 0,
    "dependents": 0,
    # Extra features (median/mode defaults from training data)
    "RevolvingUtilizationOfUnsecuredLines": 0.15,
    "age": 52,
    "NumberOfTime30-59DaysPastDueNotWorse": 0,
    "NumberOfTime60-89DaysPastDueNotWorse": 0,
    "NumberRealEstateLoansOrLines": 1,
}


# =====================================================================
# FUNCTION 1: score_applicant
# =====================================================================
def score_applicant(applicant_dict: dict) -> float:
    """
    Predict the probability of default for a single applicant.

    Args:
        applicant_dict: dict with keys
            {income, debt_ratio, credit_lines, delinquencies, dependents}

    Returns:
        float between 0.0 (low risk) and 1.0 (high risk)
    """
    model = _get_model()

    # Build a feature vector in the order the model expects
    row = dict(_FEATURE_DEFAULTS)  # start with defaults
    for key in CONTRACT_FEATURES:
        if key in applicant_dict:
            row[key] = applicant_dict[key]

    # Create a single-row DataFrame with the exact feature order
    feature_order = ALL_MODEL_FEATURES
    df = pd.DataFrame([row])[feature_order]

    # Predict probability of class 1 (default)
    prob = model.predict_proba(df)[0, 1]
    return float(np.clip(prob, 0.0, 1.0))


# =====================================================================
# FUNCTION 2: get_cohort_default_rate
# =====================================================================
def get_cohort_default_rate(applicant_dict: dict) -> float:
    """
    Query BigQuery for the historical default rate of applicants in a
    similar cohort (income +-15%, same credit_lines).

    Falls back to wider income bands (+-30%, +-50%) or the overall population
    default rate if the cohort is too small (< 20 rows). Falls back to a
    pre-computed local cache if BigQuery is unreachable or times out.

    NOTE: Cohort rates are drawn from the same BigQuery table used for
    model training, so a test applicant present in training data could
    overlap with their own cohort.  Not a blocker for a hackathon demo
    but worth noting for a production system.

    Args:
        applicant_dict: dict with keys {income, credit_lines, ...}

    Returns:
        float between 0.0 and 100.0 (percentage)
    """
    income = applicant_dict.get("income", 5400.0)
    credit_lines = applicant_dict.get("credit_lines", 8)

    # -- Try live BigQuery query ---------------------------------------
    try:
        rate = _query_bigquery_cohort(income, credit_lines)
        if rate is not None:
            return rate
    except Exception as e:
        print(f"[scoring] [WARN]  BigQuery query failed: {e}")

    # -- Fallback: local cache -----------------------------------------
    cached_rate = _lookup_cache(applicant_dict)
    if cached_rate is not None:
        print("[scoring] Using cached cohort default rate (BigQuery unavailable)")
        return cached_rate

    # -- Fallback: compute from local CSV ------------------------------
    print("[scoring] Computing cohort rate from local CSV fallback")
    return _compute_local_cohort_rate(income, credit_lines)


def _query_bigquery_cohort(
    income: float, credit_lines: int, min_cohort: int = 20
) -> float | None:
    """
    Query BigQuery with progressively wider income bands until the cohort
    has >= min_cohort rows.  Returns the default rate (0–100), or None if
    BigQuery is unreachable.
    """
    from google.cloud import bigquery

    gcp_project_id = os.environ.get("GCP_PROJECT_ID")
    if not gcp_project_id:
        raise KeyError(
            "GCP_PROJECT_ID environment variable is missing or empty. Please set it in your .env file."
        )

    client = bigquery.Client(project=gcp_project_id)
    table_ref = f"`{gcp_project_id}.{BQ_DATASET}.{BQ_TABLE}`"

    # Progressive income bands: +-15%, +-30%, +-50%, then full population
    bands = [0.15, 0.30, 0.50]

    for band in bands:
        lo = income * (1 - band)
        hi = income * (1 + band)

        query = f"""
        SELECT
            COUNT(*) AS cohort_size,
            COUNTIF(SeriousDlqin2yrs = 1) AS default_count
        FROM {table_ref}
        WHERE income BETWEEN {lo} AND {hi}
          AND credit_lines = {credit_lines}
        """

        job_config = bigquery.QueryJobConfig(
            query_parameters=[],
        )
        query_job = client.query(query, job_config=job_config)

        # Apply timeout
        try:
            rows = list(query_job.result(timeout=BQ_QUERY_TIMEOUT_SECONDS))
        except Exception as e:
            print(f"[scoring] BigQuery timeout/error at +-{int(band*100)}% band: {e}")
            return None

        if rows and rows[0]["cohort_size"] >= min_cohort:
            cohort_size = rows[0]["cohort_size"]
            default_count = rows[0]["default_count"]
            rate = (default_count / cohort_size) * 100.0
            print(
                f"[scoring] Cohort found: {cohort_size} rows "
                f"(income +-{int(band*100)}%), default rate = {rate:.2f}%"
            )
            return round(rate, 2)

        print(
            f"[scoring] Cohort too small at +-{int(band*100)}% "
            f"({rows[0]['cohort_size'] if rows else 0} rows), widening..."
        )

    # -- Full population fallback --------------------------------------
    query = f"""
    SELECT
        COUNT(*) AS total,
        COUNTIF(SeriousDlqin2yrs = 1) AS default_count
    FROM {table_ref}
    """
    rows = list(client.query(query).result(timeout=BQ_QUERY_TIMEOUT_SECONDS))
    if rows and rows[0]["total"] > 0:
        rate = (rows[0]["default_count"] / rows[0]["total"]) * 100.0
        print(f"[scoring] Using full population default rate: {rate:.2f}%")
        return round(rate, 2)

    return None


# ---------------------------------------------------------------------
# Local fallback: compute from clean_data.csv
# ---------------------------------------------------------------------
def _compute_local_cohort_rate(
    income: float, credit_lines: int, min_cohort: int = 20
) -> float:
    """Compute cohort default rate from the local CSV as a fallback."""
    if not os.path.exists(CLEAN_CSV):
        print("[scoring] [WARN]  Local CSV not found; returning population estimate.")
        return 6.7  # approximate overall default rate for this dataset

    df = pd.read_csv(CLEAN_CSV)

    bands = [0.15, 0.30, 0.50]
    for band in bands:
        lo = income * (1 - band)
        hi = income * (1 + band)
        cohort = df[
            (df["income"].between(lo, hi)) & (df["credit_lines"] == credit_lines)
        ]
        if len(cohort) >= min_cohort:
            rate = cohort["SeriousDlqin2yrs"].mean() * 100.0
            return round(rate, 2)

    # Full population fallback
    rate = df["SeriousDlqin2yrs"].mean() * 100.0
    return round(rate, 2)


# ---------------------------------------------------------------------
# Demo cache: pre-computed cohort rates for the 3 demo profiles
# ---------------------------------------------------------------------
def precompute_demo_cache():
    """
    Pre-compute and save cohort default rates for the 3 demo profiles.
    Run this once before the demo to prime the local cache fallback.
    """
    demo_profiles = {
        "low_risk": {"income": 9500, "debt_ratio": 0.15, "credit_lines": 10,
                     "delinquencies": 0, "dependents": 1},
        "high_risk": {"income": 2200, "debt_ratio": 0.85, "credit_lines": 3,
                      "delinquencies": 4, "dependents": 3},
        "borderline": {"income": 5000, "debt_ratio": 0.45, "credit_lines": 7,
                       "delinquencies": 1, "dependents": 2},
    }

    cache = {}
    for label, profile in demo_profiles.items():
        rate = _compute_local_cohort_rate(
            profile["income"], profile["credit_lines"]
        )
        score = score_applicant(profile)
        cache[label] = {
            "profile": profile,
            "cohort_default_rate": rate,
            "risk_score": round(score, 4),
        }
        print(f"[cache] {label}: risk_score={score:.4f}, cohort_rate={rate:.2f}%")

    os.makedirs(os.path.dirname(CACHE_PATH), exist_ok=True)
    with open(CACHE_PATH, "w") as f:
        json.dump(cache, f, indent=2)
    print(f"[cache] [OK] Saved demo cache to {CACHE_PATH}")
    return cache


def _lookup_cache(applicant_dict: dict) -> float | None:
    """Look up an applicant in the pre-computed demo cache."""
    if not os.path.exists(CACHE_PATH):
        return None
    try:
        with open(CACHE_PATH) as f:
            cache = json.load(f)
        for label, entry in cache.items():
            profile = entry["profile"]
            if (
                abs(profile["income"] - applicant_dict.get("income", -1)) < 1.0
                and profile["credit_lines"] == applicant_dict.get("credit_lines", -1)
            ):
                print(f"[scoring] Cache hit: {label}")
                return entry["cohort_default_rate"]
    except Exception:
        pass
    return None
