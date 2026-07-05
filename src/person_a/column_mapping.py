"""
column_mapping.py - Single source of truth for Kaggle-to-contract field name mapping.

This dictionary is used in clean_data.py on ingestion, so every downstream script
(train.py, scoring_service.py, gpu_benchmark.py) works with the unified contract
field names and never references raw Kaggle column headers ad hoc.
"""

# ---------------------------------------------------------------------
# Kaggle raw column name  ->  Contract / internal field name
# ---------------------------------------------------------------------
KAGGLE_TO_CONTRACT = {
    "MonthlyIncome":                       "income",
    "DebtRatio":                           "debt_ratio",
    "NumberOfOpenCreditLinesAndLoans":      "credit_lines",
    "NumberOfDependents":                   "dependents",
    "NumberOfTimes90DaysLate":              "delinquencies",
}

# Reverse map (contract -> Kaggle) for any script that needs to go the other way
CONTRACT_TO_KAGGLE = {v: k for k, v in KAGGLE_TO_CONTRACT.items()}

# ---------------------------------------------------------------------
# Columns kept but NOT renamed (target + other useful features)
# ---------------------------------------------------------------------
TARGET_COLUMN = "SeriousDlqin2yrs"

# Additional raw features that are kept as-is (not part of the 5-field contract
# but used as model features to improve AUC)
EXTRA_FEATURES = [
    "RevolvingUtilizationOfUnsecuredLines",
    "age",
    "NumberOfTime30-59DaysPastDueNotWorse",
    "NumberOfTime60-89DaysPastDueNotWorse",
    "NumberRealEstateLoansOrLines",
]

# The 5 contract-name features (after renaming)
CONTRACT_FEATURES = list(KAGGLE_TO_CONTRACT.values())

# All features used for model training (contract names + extras)
ALL_MODEL_FEATURES = CONTRACT_FEATURES + EXTRA_FEATURES
