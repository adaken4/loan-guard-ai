import json
from collections import defaultdict

def extract_features(data):
    txns = data["transactions"]
    repayments = data["repayments"]

    total_income = sum(txn["amount"] for txn in txns if txn["type"] == "income")
    total_expense = sum(txn["amount"] for txn in txns if txn["type"] == "expense")
    net_cashflow = total_income - total_expense

    # Gambling ratio
    gambling_expense = sum(txn["amount"] for txn in txns if txn.get("category") == "gambling")
    gambling_ratio = gambling_expense / total_expense if total_expense > 0 else 0

    # Savings ratio
    savings_expense = sum(txn["amount"] for txn in txns if txn.get("category") == "savings")
    savings_ratio = savings_income_ratio = savings_expense / total_income if total_income > 0 else 0

    # Income consistency (std of income)
    incomes = [txn["amount"] for txn in txns if txn["type"] == "income"]
    income_std = (sum((x - (sum(incomes) / len(incomes))) ** 2 for x in incomes) / len(incomes)) ** 0.5 if incomes else 0

    # Repayment stats
    total_loans = len(repayments)
    on_time = sum(1 for r in repayments if r["status"] == "on_time")
    late = sum(1 for r in repayments if r["status"] == "late")
    missed = sum(1 for r in repayments if r["status"] == "missed")
    repayment_rate = on_time / total_loans if total_loans > 0 else 1.0

    return {
        "total_income": total_income,
        "total_expense": total_expense,
        "net_cashflow": net_cashflow,
        "gambling_ratio": gambling_ratio,
        "savings_ratio": savings_ratio,
        "income_std": income_std,
        "repayment_rate": repayment_rate,
        "missed_repayments": missed,
        "total_loans": total_loans
    }