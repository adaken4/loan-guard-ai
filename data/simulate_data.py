import json
import random
from datetime import datetime, timedelta
from model.config import PROFILES

random.seed(42) # For deterministic output

def simulate_transactions(profile_name, month=6):
    profile = PROFILES[profile_name]
    transactions = []
    repayments = []
    current_date = datetime(2025, 6, 1)  # Start date

    for _ in range(month * 4):
        # Simulate income
        if profile["income_freq"] == "bi-weekly" and _ % 2 == 0:
            income = profile["income_amount"]
        elif profile["income_freq"] == "weekly":
            income = profile["income_amount"]
        elif profile["income_freq"] == "irregular":
            income = random.randint(*profile["income_amount"]) if isinstance(profile["income_amount"], list) else profile["income_amount"]
        else:
            income = 0

        if income > 0:
            transactions.append({"date": current_date.isoformat(), "amount": income, "type": "income"})

        # Simulate expenses
        total_expenses = income * 0.9 if income > 0 else random.randint(100, 400)
        for cat, ratio in profile["expense_types"].items():
            noise = random.uniform(-0.1, 0.1)  # Small noise for realism
            adjusted_ratio = max(0, ratio + noise)

            amt = total_expenses * adjusted_ratio
            if amt > 0:
                transactions.append({"date": current_date.isoformat(), "amount": round(amt, 2), "type": "expense", "category": cat})

        # Simulate loan repayment (assume 1 loan/month)
        repayment_on_time = random.random() < (profile["repayment_reliability"] * random.uniform(0.9, 1.05))
        repayments.append({
            "loan_id": f"LOAN-{_}",
            "due_date": (current_date + timedelta(days=30)).isoformat(),
            "paid_date": (current_date + timedelta(days=30 + (0 if repayment_on_time else random.randint(1, 20)))).isoformat(),
            "status": (
                "on_time" if repayment_on_time
                else "late" if random.random() > 0.3
                else "missed"
            )
        })

        current_date += timedelta(weeks=1)

    return {"profile": profile_name, "transactions": transactions, "repayments": repayments}

if __name__ == "__main__":
    all_data = {}
    for name in PROFILES:
        all_data[name] = simulate_transactions(name)
    with open("data/simulated_data.json", "w") as f:
        json.dump(all_data, f, indent=2)
    print("✅ Simulated data saved to data/simulated_data.json")
