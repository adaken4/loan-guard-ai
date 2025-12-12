import joblib
from .feature_engineering import extract_features

model = joblib.load("model/risk_model.pkl")
RISK_LABELS = {0: "Low Risk", 1: "Medium Risk", 2: "High Risk"}
EMOJIS = {0: "✅", 1: "⚠️", 2: "❌"}

def score_borrower(data):
    features = extract_features(data)
    X = list(features.values())
    pred_class = model.predict([X])[0]
    pred_proba = model.predict_proba([X])[0]
    # Weighted default probability: Low=5%, Medium=25%, High=80%
    default_prob = round((pred_proba[0] * 5 + pred_proba[1] * 25 + pred_proba[2] * 80), 1)

    risk_label = RISK_LABELS[pred_class]
    emoji = EMOJIS[pred_class]

    # Recommendation logic
    if pred_class == 0:
        recommendation = "Approve loan at requested amount"
    elif pred_class == 1:
        recommendation = "Approve reduced loan amount (e.g., 50% of request)"
    else:
        recommendation = "Reject loan application"
    
    return {
        "risk_class": risk_label,
        "default_probability": default_prob,
        "emoji": emoji,
        "recommendation": recommendation,
        "features": features
    }