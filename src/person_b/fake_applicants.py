# src/person_b/fake_applicants.py

fake_applicants = [
    {
        "income": 12500,
        "debt_ratio": 0.15,
        "credit_lines": 8,
        "delinquencies": 0,
        "dependents": 0,
        "risk_level_label": "Low"
    },
    {
        "income": 22000,
        "debt_ratio": 0.08,
        "credit_lines": 12,
        "delinquencies": 0,
        "dependents": 2,
        "risk_level_label": "Low"
    },
    {
        "income": 6000,
        "debt_ratio": 0.35,
        "credit_lines": 6,
        "delinquencies": 0,
        "dependents": 1,
        "risk_level_label": "Medium"
    },
    {
        "income": 4500,
        "debt_ratio": 0.48,
        "credit_lines": 5,
        "delinquencies": 0,
        "dependents": 3,
        "risk_level_label": "Medium"
    },
    {
        "income": 3200,
        "debt_ratio": 0.22,
        "credit_lines": 3,
        "delinquencies": 0,
        "dependents": 0,
        "risk_level_label": "Medium"
    },
    {
        "income": 2500,
        "debt_ratio": 0.65,
        "credit_lines": 4,
        "delinquencies": 2,
        "dependents": 1,
        "risk_level_label": "High"
    },
    {
        "income": 5000,
        "debt_ratio": 0.55,
        "credit_lines": 15,
        "delinquencies": 3,
        "dependents": 4,
        "risk_level_label": "High"
    },
    {
        "income": 1500,
        "debt_ratio": 1.20,
        "credit_lines": 10,
        "delinquencies": 5,
        "dependents": 2,
        "risk_level_label": "High"
    }
]

if __name__ == "__main__":
    import pprint
    print("Generated 8 fake applicant records:")
    pprint.pprint(fake_applicants)
