import json
from model.risk_scoring import score_borrower

with open("data/simulated_data.json") as f:
    ALL_DATA = json.load(f)

def main():
    print("🏦 LoanGuard AI – Micro-Lender Risk Scoring MVP\n")
    print("Select a borrower profile:")
    profiles = list(ALL_DATA.keys())
    for i, profile in enumerate(profiles, 1):
        print(f"{i}. {profile.replace('_', ' ').title()}")

    choice = int(input("\nEnter choice (1-3): ")) - 1
    profile_name = profiles[choice]
    borrower_data = ALL_DATA[profile_name]

    print(f"\n📌 Profile: {profile_name.replace('_', ' ').title()}")
    print(f"    Transactions: {len(borrower_data['transactions'])}")
    print(f"    Past Loans: {len(borrower_data['repayments'])}")

    result = score_borrower(borrower_data)

    print("\n🔍 AI Risk Assessment:")
    print(f"    Risk Level: {result['emoji']} {result['risk_class']}")
    print(f"    Estimated Default Probability: {result['default_probability']}%")
    print(f"\n💡 Recommendation: {result['recommendation']}")
    print(f"\n📊 Key Features:")
    for key, value in list(result['features'].items())[:5]:
        print(f"    • {key}: {value:.2f}" if isinstance(value, float) else f"    • {key}: {value}")

if __name__ == "__main__":
    main()