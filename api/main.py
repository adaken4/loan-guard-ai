from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Any
import joblib
import traceback
import os
import numpy as np
from datetime import datetime
from fastapi.middleware.cors import CORSMiddleware

from model.feature_engineering import extract_features
from data.simulate_data import simulate_transactions
from model.risk_scoring import score_borrower

app = FastAPI(title="LoanGuard AI - Micro-Lender Risk Scoring API", version="0.1.0")

ALLOWED_ORIGINS = os.environ.get(
    "CORS_ORIGINS",
    "http://localhost:3000,http://127.0.0.1:3000"
).split(',')

# ---- CORS ----
app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---- Model Lazy Loader ----
MODEL_PATH = "model/risk_model.pkl"
model = None

def load_model():
    global model
    if model is None:
        if not os.path.exists(MODEL_PATH):
            raise RuntimeError("Model not trained. Train it first.")
        model = joblib.load(MODEL_PATH)
    return model

# ---- Request Schemas ----
class BorrowerInput(BaseModel):
    profile: str # good_spender | gambling_spender | inconsistent_earner

class ScoreResponse(BaseModel):
    risk_class: str
    default_probability: float
    recommendation: str

class Transaction(BaseModel):
    date: str
    amount: float
    type: str
    category: str | None = None

class Repayment(BaseModel):
    loan_id: str | None = None
    due_date: str | None = None
    paid_date: str | None = None
    status: str

class BorrowerRequest(BaseModel):
    transactions: List[Transaction]
    repayments: List[Repayment]

@app.post("/score")
def score_endpoint(payload: BorrowerRequest):
    try:
        data = payload.dict()
        result = score_borrower(data)
        return {"success": True, "result": result}
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))
    
@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.post("/predict", response_model=ScoreResponse)
def predict_from_profile(payload: BorrowerInput):
    clf = load_model()

    if payload.profile not in ["good_spender", "gambling_spender", "inconsistent_earner"]:
        raise HTTPException(status_code=400, detail="Invalid profile")
    
    tx_data = simulate_transactions(payload.profile)
    feats = extract_features(tx_data)
    X = np.array([list(feats.values())])

    proba = clf.predict_proba(X)[0]
    risk_class_idx = int(np.argmax(proba))
    # model_confidence = np.max(proba)

    # # Realistic PD changes blended with model confidence
    # risk_pd_ranges = {
    #     0: (0.02, 0.05),
    #     1: (0.15, 0.30),
    #     2: (0.70, 0.95)
    # }
    # min_pd, max_pd = risk_pd_ranges.get(risk_class_idx)

    # default_probability = round((min_pd + (max_pd - min_pd) * model_confidence) * 100, 1)  # Probability of high risk

    default_probability = round(proba[1] * 0.5 + proba[2] * 100, 1)

    risk_labels = {0: "Low Risk", 1: "Medium Risk", 2: "High Risk"}
    risk_class = risk_labels.get(risk_class_idx, "Unknown")

    if risk_class_idx == 0:
        recommendation = "Approve loan at requested amount"
    elif risk_class_idx == 1:
        recommendation = "Approve reduced loan amount (e.g., 50% of request)"
    else:
        recommendation = "Reject loan application"

    return ScoreResponse(
        risk_class=risk_class,
        default_probability=default_probability,
        recommendation=recommendation
    )

@app.post("/admin/retrain")
def retrain():
    return {"status": "stub", "message": "Retraining pipeline not wired yet"}