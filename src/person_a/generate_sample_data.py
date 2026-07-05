"""
generate_sample_data.py - Generate a synthetic dataset that mirrors the
"Give Me Some Credit" Kaggle dataset schema and distributions.

This allows the full pipeline to be tested without Kaggle authentication.
Replace data/cs-training.csv with the real Kaggle file when available.

Usage:
    python src/person_a/generate_sample_data.py
"""

import os
import sys
import numpy as np
import pandas as pd

_SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
_PROJECT_ROOT = os.path.abspath(os.path.join(_SCRIPT_DIR, "..", ".."))

OUTPUT_PATH = os.path.join(_PROJECT_ROOT, "data", "cs-training.csv")
N_ROWS = 150_000
SEED = 42


def generate():
    rng = np.random.default_rng(SEED)

    # -- Target: ~6.7% default rate (matches Kaggle distribution) ------
    n_default = int(N_ROWS * 0.067)
    target = np.zeros(N_ROWS, dtype=int)
    target[:n_default] = 1
    rng.shuffle(target)

    # -- Features ------------------------------------------------------
    # RevolvingUtilizationOfUnsecuredLines: mostly 0-1, with outlier spikes
    revolving = rng.exponential(0.3, N_ROWS)
    revolving = np.clip(revolving, 0, 50000)
    # Make defaulters have higher utilization on average
    revolving[target == 1] *= rng.uniform(1.5, 3.0, n_default)

    # age: 21-109, median ~52
    age = rng.normal(52, 14, N_ROWS).astype(int)
    age = np.clip(age, 21, 109)

    # NumberOfTime30-59DaysPastDueNotWorse: mostly 0, some 1-2, rare >2
    past_due_30 = rng.poisson(0.2, N_ROWS)
    past_due_30[target == 1] += rng.poisson(0.8, n_default)
    past_due_30 = np.clip(past_due_30, 0, 13)

    # DebtRatio: mostly 0-1, with outlier spikes
    debt_ratio = rng.exponential(0.35, N_ROWS)
    debt_ratio = np.clip(debt_ratio, 0, 5000)

    # MonthlyIncome: median ~5400, with ~20% missing (matching Kaggle)
    monthly_income = rng.lognormal(8.5, 0.8, N_ROWS)
    monthly_income = np.round(monthly_income, 2)
    # Introduce ~20% missing values
    missing_mask = rng.random(N_ROWS) < 0.20
    monthly_income_series = pd.Series(monthly_income, dtype=float)
    monthly_income_series[missing_mask] = np.nan

    # NumberOfOpenCreditLinesAndLoans: 0-58, median ~8
    credit_lines = rng.poisson(8, N_ROWS)
    credit_lines = np.clip(credit_lines, 0, 58)

    # NumberOfTimes90DaysLate: mostly 0
    past_due_90 = rng.poisson(0.1, N_ROWS)
    past_due_90[target == 1] += rng.poisson(0.5, n_default)
    past_due_90 = np.clip(past_due_90, 0, 17)

    # NumberRealEstateLoansOrLines: 0-54, median ~1
    real_estate = rng.poisson(1.0, N_ROWS)
    real_estate = np.clip(real_estate, 0, 54)

    # NumberOfTime60-89DaysPastDueNotWorse: mostly 0
    past_due_60 = rng.poisson(0.08, N_ROWS)
    past_due_60[target == 1] += rng.poisson(0.3, n_default)
    past_due_60 = np.clip(past_due_60, 0, 11)

    # NumberOfDependents: 0-20, with ~2.6% missing
    dependents = rng.poisson(0.8, N_ROWS).astype(float)
    dependents = np.clip(dependents, 0, 20)
    dep_missing = rng.random(N_ROWS) < 0.026
    dependents_series = pd.Series(dependents)
    dependents_series[dep_missing] = np.nan

    # -- Build DataFrame (same column order as Kaggle) -----------------
    df = pd.DataFrame({
        "Unnamed: 0": np.arange(1, N_ROWS + 1),
        "SeriousDlqin2yrs": target,
        "RevolvingUtilizationOfUnsecuredLines": revolving,
        "age": age,
        "NumberOfTime30-59DaysPastDueNotWorse": past_due_30,
        "DebtRatio": debt_ratio,
        "MonthlyIncome": monthly_income_series,
        "NumberOfOpenCreditLinesAndLoans": credit_lines,
        "NumberOfTimes90DaysLate": past_due_90,
        "NumberRealEstateLoansOrLines": real_estate,
        "NumberOfTime60-89DaysPastDueNotWorse": past_due_60,
        "NumberOfDependents": dependents_series,
    })

    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    df.to_csv(OUTPUT_PATH, index=False)

    print(f"[generate] DONE - Synthetic dataset saved to {OUTPUT_PATH}")
    print(f"[generate]    Shape: {df.shape}")
    print(f"[generate]    Default rate: {target.mean()*100:.1f}%")
    print(f"[generate]    MonthlyIncome missing: {missing_mask.sum():,} ({missing_mask.mean()*100:.1f}%)")
    print(f"[generate]    NumberOfDependents missing: {dep_missing.sum():,} ({dep_missing.mean()*100:.1f}%)")


if __name__ == "__main__":
    generate()
