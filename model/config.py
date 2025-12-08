PROFILES = {
    "good_spender": {
        "income_freq": "biweekly",
        "income_amount": 800,
        "expense_types": {"groceries": 0.4, "utilities": 0.2, "savings": 0.3, "entertainment": 0.1},
        "repayment_reliability": 0.98
    },
    "gambling_spender": {
        "income_freq": "weekly",
        "income_amount": 600,
        "expense_types": {"gambling": 0.5, "food": 0.3, "bills": 0.15, "other": 0.05},
        "repayment_reliability": 0.65
    },
    "inconsistent_earner": {
        "income_freq": "irregular",
        "income_amount": [300, 1200],
        "expense_types": {"essentials": 0.7, "debt": 0.2, "misc": 0.1},
        "repayment_reliability": 0.70
    }
}
