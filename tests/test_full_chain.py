"""
test_full_chain.py - End-to-end integration test for the loan underwriting pipeline.

Runs 2 sample applicants through:
  score_applicant() -> get_cohort_default_rate() -> explain_risk() -> recommend_decision()

Prints every intermediate output with its Python type so any mismatch is
immediately visible.

Usage (from project root):
  python tests/test_full_chain.py
"""

import sys
import os
import time

# Ensure project root is on the path
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, PROJECT_ROOT)

from src.person_a.scoring_service import score_applicant, get_cohort_default_rate
from src.person_b.explain_api import explain_risk
from src.person_b.decision_engine import recommend_decision

# Two sample applicants from fake_applicants.py (one low risk, one high risk)
SAMPLE_APPLICANTS = [
    {
        "income": 12500,
        "debt_ratio": 0.15,
        "credit_lines": 8,
        "delinquencies": 0,
        "dependents": 0,
        "label": "Low Risk",
    },
    {
        "income": 1500,
        "debt_ratio": 1.20,
        "credit_lines": 10,
        "delinquencies": 5,
        "dependents": 2,
        "label": "High Risk",
    },
]


def run_chain(applicant: dict) -> None:
    """Run one applicant through the full pipeline, printing every step."""
    label = applicant.pop("label", "Unknown")
    print(f"\n{'='*60}")
    print(f"  Applicant: {label}")
    print(f"  Input dict: {applicant}")
    print(f"{'='*60}")

    # Step 1: score_applicant
    risk_score = score_applicant(applicant)
    print(f"\n  [1] score_applicant()")
    print(f"      Return value : {risk_score}")
    print(f"      Type         : {type(risk_score).__name__}")
    print(f"      In range 0-1?: {0.0 <= risk_score <= 1.0}")

    # Step 2: get_cohort_default_rate
    cohort_rate = get_cohort_default_rate(applicant)
    print(f"\n  [2] get_cohort_default_rate()")
    print(f"      Return value  : {cohort_rate}")
    print(f"      Type          : {type(cohort_rate).__name__}")
    print(f"      In range 0-100?: {0.0 <= cohort_rate <= 100.0}")

    # Step 3: explain_risk
    explanation = explain_risk(applicant, risk_score, cohort_rate)
    print(f"\n  [3] explain_risk()")
    print(f"      Return value : {explanation[:200]}{'...' if len(explanation) > 200 else ''}")
    print(f"      Type         : {type(explanation).__name__}")
    print(f"      Non-empty?   : {bool(explanation)}")

    # Small delay for Gemini rate limits
    time.sleep(4)

    # Step 4: recommend_decision
    decision = recommend_decision(explanation)
    print(f"\n  [4] recommend_decision()")
    print(f"      Return value : {decision}")
    print(f"      Type         : {type(decision).__name__}")
    print(f"      Has 'recommendation'?: {'recommendation' in decision}")
    print(f"      Has 'confidence'?    : {'confidence' in decision}")
    print(f"      recommendation value : {decision.get('recommendation')}")
    print(f"      confidence value     : {decision.get('confidence')}")

    # Validate expected types
    assert isinstance(risk_score, float), f"risk_score should be float, got {type(risk_score)}"
    assert isinstance(cohort_rate, float), f"cohort_rate should be float, got {type(cohort_rate)}"
    assert isinstance(explanation, str), f"explanation should be str, got {type(explanation)}"
    assert isinstance(decision, dict), f"decision should be dict, got {type(decision)}"
    assert "recommendation" in decision, "decision missing 'recommendation' key"
    assert "confidence" in decision, "decision missing 'confidence' key"

    print(f"\n  [OK] All assertions passed for {label}")


if __name__ == "__main__":
    print("=" * 60)
    print("  FULL-CHAIN INTEGRATION TEST")
    print("  score_applicant -> get_cohort_default_rate -> explain_risk -> recommend_decision")
    print("=" * 60)

    for applicant in SAMPLE_APPLICANTS:
        run_chain(dict(applicant))  # copy so .pop("label") doesn't mutate original
        time.sleep(4)  # respect Gemini rate limits between applicants

    print(f"\n{'='*60}")
    print("  [OK] ALL TESTS PASSED -- full chain is type-safe end to end")
    print(f"{'='*60}")
