"""
clean_data.py - Load the raw Kaggle CSV, apply the central column mapping,
impute missing values, and save a clean dataset.

Usage:
    python -m src.person_a.clean_data
    # or from project root:
    python src/person_a/clean_data.py
"""

import os
import sys
import pandas as pd

# -- Make imports work whether run as a module or as a standalone script --
_SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
_PROJECT_ROOT = os.path.abspath(os.path.join(_SCRIPT_DIR, "..", ".."))
if _PROJECT_ROOT not in sys.path:
    sys.path.insert(0, _PROJECT_ROOT)

from src.person_a.column_mapping import (
    KAGGLE_TO_CONTRACT,
    TARGET_COLUMN,
    ALL_MODEL_FEATURES,
)

# ---------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------
RAW_CSV = os.path.join(_PROJECT_ROOT, "data", "cs-training.csv")
CLEAN_CSV = os.path.join(_PROJECT_ROOT, "data", "clean_data.csv")


def load_and_clean(raw_path: str = RAW_CSV) -> pd.DataFrame:
    """Load raw Kaggle CSV, rename columns, impute, and return a clean DataFrame."""

    print(f"[clean_data] Loading raw data from {raw_path} ...")
    df = pd.read_csv(raw_path)

    # Drop the unnamed index column that Kaggle ships with the CSV
    if "Unnamed: 0" in df.columns:
        df.drop(columns=["Unnamed: 0"], inplace=True)

    # -- Apply the central column mapping ------------------------------
    df.rename(columns=KAGGLE_TO_CONTRACT, inplace=True)
    print(f"[clean_data] Renamed columns: {list(KAGGLE_TO_CONTRACT.keys())} -> {list(KAGGLE_TO_CONTRACT.values())}")

    # -- Impute missing values -----------------------------------------
    # income (was MonthlyIncome): fill with median
    median_income = df["income"].median()
    missing_income = df["income"].isna().sum()
    df["income"] = df["income"].fillna(median_income)
    print(f"[clean_data] Imputed {missing_income} missing 'income' values with median = {median_income:.2f}")

    # dependents (was NumberOfDependents): fill with 0 (mode)
    missing_deps = df["dependents"].isna().sum()
    df["dependents"] = df["dependents"].fillna(0)
    print(f"[clean_data] Imputed {missing_deps} missing 'dependents' values with 0")

    # -- Keep only the columns we need ---------------------------------
    keep_cols = [TARGET_COLUMN] + ALL_MODEL_FEATURES
    # Filter to only columns that actually exist (defensive)
    keep_cols = [c for c in keep_cols if c in df.columns]
    df = df[keep_cols]

    # -- Drop any remaining rows with NaN (there shouldn't be many) ----
    before = len(df)
    df.dropna(inplace=True)
    after = len(df)
    if before != after:
        print(f"[clean_data] Dropped {before - after} rows with remaining NaNs")

    print(f"[clean_data] Clean dataset shape: {df.shape}")
    return df


def main():
    df = load_and_clean()
    os.makedirs(os.path.dirname(CLEAN_CSV), exist_ok=True)
    df.to_csv(CLEAN_CSV, index=False)
    print(f"[clean_data] [OK] Saved clean data to {CLEAN_CSV}")


if __name__ == "__main__":
    main()
