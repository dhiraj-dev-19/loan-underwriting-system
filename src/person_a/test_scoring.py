"""
test_scoring.py - Verify the score_applicant() and get_cohort_default_rate()
contract functions with three mock applicant profiles.

This script tests locally without BigQuery (falls back to local CSV computation).

Usage:
    python -m src.person_a.test_scoring
    # or from project root:
    python src/person_a/test_scoring.py
"""

import os
import sys

# -- Make imports work whether run as a module or as a standalone script --
_SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
_PROJECT_ROOT = os.path.abspath(os.path.join(_SCRIPT_DIR, "..", ".."))
if _PROJECT_ROOT not in sys.path:
    sys.path.insert(0, _PROJECT_ROOT)

from src.person_a.scoring_service import (
    score_applicant,
    get_cohort_default_rate,
    precompute_demo_cache,
)

# ---------------------------------------------------------------------
# Test profiles
# ---------------------------------------------------------------------
PROFILES = {
    "low_risk": {
        "income": 9500,
        "debt_ratio": 0.15,
        "credit_lines": 10,
        "delinquencies": 0,
        "dependents": 1,
    },
    "high_risk": {
        "income": 2200,
        "debt_ratio": 0.85,
        "credit_lines": 3,
        "delinquencies": 4,
        "dependents": 3,
    },
    "borderline": {
        "income": 5000,
        "debt_ratio": 0.45,
        "credit_lines": 7,
        "delinquencies": 1,
        "dependents": 2,
    },
}


def run_tests():
    """Run all test profiles and print results."""
    print("=" * 70)
    print("  SCORING SERVICE - CONTRACT FUNCTION TESTS")
    print("=" * 70)

    all_passed = True

    for label, profile in PROFILES.items():
        print(f"\n{'-' * 70}")
        print(f"  Profile: {label.upper()}")
        print(f"  Input:   {profile}")
        print(f"{'-' * 70}")

        # -- Test score_applicant --------------------------------------
        try:
            risk_score = score_applicant(profile)
            print(f"  risk_score        = {risk_score:.4f}")

            # Sanity checks
            assert 0.0 <= risk_score <= 1.0, f"Score out of range: {risk_score}"

            if label == "low_risk" and risk_score > 0.5:
                print(f"  [WARN]  WARNING: low_risk profile scored high ({risk_score:.4f})")
            if label == "high_risk" and risk_score < 0.3:
                print(f"  [WARN]  WARNING: high_risk profile scored low ({risk_score:.4f})")

            print(f"  [OK] score_applicant passed")
        except Exception as e:
            print(f"  [FAIL] score_applicant FAILED: {e}")
            all_passed = False

        # -- Test get_cohort_default_rate ------------------------------
        try:
            cohort_rate = get_cohort_default_rate(profile)
            print(f"  cohort_default_rate = {cohort_rate:.2f}%")

            # Sanity checks
            assert 0.0 <= cohort_rate <= 100.0, f"Rate out of range: {cohort_rate}"

            print(f"  [OK] get_cohort_default_rate passed")
        except Exception as e:
            print(f"  [FAIL] get_cohort_default_rate FAILED: {e}")
            all_passed = False

    # -- Pre-compute demo cache ----------------------------------------
    print(f"\n{'-' * 70}")
    print("  PRE-COMPUTING DEMO CACHE")
    print(f"{'-' * 70}")
    try:
        cache = precompute_demo_cache()
        print(f"  [OK] Demo cache saved ({len(cache)} profiles)")
    except Exception as e:
        print(f"  [FAIL] Demo cache failed: {e}")
        all_passed = False

    # -- Summary -------------------------------------------------------
    print(f"\n{'=' * 70}")
    if all_passed:
        print("  [OK] ALL TESTS PASSED")
    else:
        print("  [FAIL] SOME TESTS FAILED - see above for details")
    print(f"{'=' * 70}")
    return all_passed


if __name__ == "__main__":
    success = run_tests()
    sys.exit(0 if success else 1)
