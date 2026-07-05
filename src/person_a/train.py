"""
train.py - Train a Random Forest classifier on the cleaned loan data.

Targets AUC >= 0.75 on an 80/20 hold-out split.
Saves the trained model to data/model.pkl using joblib.

Usage:
    python -m src.person_a.train
    # or from project root:
    python src/person_a/train.py
"""

import os
import sys
import joblib
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import roc_auc_score, classification_report

# -- Make imports work whether run as a module or as a standalone script --
_SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
_PROJECT_ROOT = os.path.abspath(os.path.join(_SCRIPT_DIR, "..", ".."))
if _PROJECT_ROOT not in sys.path:
    sys.path.insert(0, _PROJECT_ROOT)

from src.person_a.column_mapping import TARGET_COLUMN, ALL_MODEL_FEATURES

# ---------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------
CLEAN_CSV = os.path.join(_PROJECT_ROOT, "data", "clean_data.csv")
MODEL_PATH = os.path.join(_PROJECT_ROOT, "data", "model.pkl")


def train_model(clean_csv: str = CLEAN_CSV) -> tuple:
    """
    Train a RandomForestClassifier and return (model, auc_score).

    Returns:
        model: the trained sklearn RandomForestClassifier
        auc:   ROC AUC score on the hold-out test set
    """
    print(f"[train] Loading clean data from {clean_csv} ...")
    df = pd.read_csv(clean_csv)

    # -- Separate features and target ----------------------------------
    feature_cols = [c for c in ALL_MODEL_FEATURES if c in df.columns]
    X = df[feature_cols]
    y = df[TARGET_COLUMN]

    print(f"[train] Features ({len(feature_cols)}): {feature_cols}")
    print(f"[train] Target distribution:\n{y.value_counts(normalize=True).to_string()}")

    # -- Train/test split (80/20, stratified) --------------------------
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.20, random_state=42, stratify=y
    )
    print(f"[train] Train size: {len(X_train):,}  |  Test size: {len(X_test):,}")

    # -- Train Random Forest -------------------------------------------
    # class_weight="balanced" compensates for the heavy class imbalance
    # (~93% non-default, ~7% default).
    model = RandomForestClassifier(
        n_estimators=200,
        max_depth=12,
        min_samples_leaf=50,
        class_weight="balanced",
        random_state=42,
        n_jobs=-1,
    )
    print("[train] Training RandomForestClassifier ...")
    model.fit(X_train, y_train)

    # -- Evaluate ------------------------------------------------------
    y_prob = model.predict_proba(X_test)[:, 1]
    auc = roc_auc_score(y_test, y_prob)
    print(f"\n[train] [OK] ROC AUC Score: {auc:.4f}")

    if auc < 0.75:
        print("[train] [WARN]  AUC is below 0.75 - consider tuning hyperparameters.")
    else:
        print("[train] [OK] AUC target (>= 0.75) met!")

    # -- Feature importance --------------------------------------------
    importances = sorted(
        zip(feature_cols, model.feature_importances_),
        key=lambda x: x[1],
        reverse=True,
    )
    print("\n[train] Feature importances (top 10):")
    for name, imp in importances[:10]:
        print(f"  {name:45s} {imp:.4f}")

    return model, auc


def main():
    model, auc = train_model()

    # -- Save model ----------------------------------------------------
    os.makedirs(os.path.dirname(MODEL_PATH), exist_ok=True)
    joblib.dump(model, MODEL_PATH)
    print(f"\n[train] [OK] Model saved to {MODEL_PATH}")
    print(f"[train] Final AUC: {auc:.4f}")


if __name__ == "__main__":
    main()
