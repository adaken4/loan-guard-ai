# 🛡️ LoanGuard AI

### From Transaction to Trust: Intelligent Risk Scoring for Micro-Lenders

## 📖 Overview

**LoanGuard AI** is a full-stack predictive analytics platform designed to solve the critical bottleneck in micro-lending: **Risk Assessment**.

In emerging markets like Kenya, manual credit scoring is slow, subjective, and often excludes "thin-file" borrowers who lack formal credit history. LoanGuard AI transforms raw behavioral data—transactions, spending patterns, and repayment history—into an instant, objective, and transparent **Trust Score**.

### The Problem

  * **Financial Exclusion:** Worthy borrowers are rejected due to lack of traditional collateral.
  * **High Default Rates:** Manual vetting misses subtle behavioral red flags (e.g., gambling patterns).
  * **Scalability:** Human loan officers cannot process thousands of micro-loans efficiently.

### The Solution

LoanGuard AI uses a custom-trained **Random Forest Classifier**, enhanced with **Isotonic Probability Calibration**, to predict the probability of loan default with high precision. It provides lenders with not just a "Yes/No" but a granular risk profile.

-----

## 🚀 Key Features

  * **📊 Behavioral Feature Engineering:** Unlike generic models, we engineer domain-specific features such as `gambling_ratio`, `income_consistency`, and `repayment_reliability` to catch high-risk behaviors early.
  * **⚖️ Calibrated Probabilities:** We solve the "overconfidence" problem of standard ML models by applying **Isotonic Regression**, converting raw model outputs into realistic, policy-compliant Probabilities of Default (PD).
  * **⚡ Real-Time API:** A high-performance FastAPI backend that scores borrowers in milliseconds.
  * **🖥️ lender Dashboard:** A responsive Next.js frontend for loan officers to visualize risk and make data-driven decisions.

-----

## 🧠 The AI Model (Predictive Analytics)

We chose a **White-Box Approach** over deep learning to ensure transparency and auditability in financial decision-making.

[Image of Random Forest Model Architecture]

1.  **Data Simulation:** We generated synthetic data representing three core archetypes: *Good Spender*, *Gambling Spender*, and *Inconsistent Earner*.
2.  **Algorithm:** **Random Forest Classifier** (Scikit-Learn). Selected for its ability to handle tabular data and provide feature importance.
3.  **Calibration Layer:** Post-training, we utilize `CalibratedClassifierCV` (Isotonic) to map the model's raw scores to accurate probability estimates, ensuring a 50% risk score actually means a 50% chance of default.

-----

## 🏗️ Architecture

LoanGuard AI follows a modern, decoupled microservices architecture:

  * **Frontend:** Next.js & Tailwind CSS (Deployed on Vercel)
  * **Backend API:** Python FastAPI (Dockerized & Deployed on Render)
  * **Inference Engine:** Scikit-learn Pipeline (Serialized via Joblib)

For a complete breakdown of the data flow, model design, and deployment strategy, please see the **[Full System Architecture Document](ARCHITECTURE.md)**.

-----

## 🛠️ Tech Stack

  * **Language:** Python 3.12, TypeScript
  * **ML Libraries:** Scikit-learn, NumPy, Pandas, Joblib
  * **API Framework:** FastAPI, Uvicorn, Pydantic
  * **Frontend:** Next.js 16, React, Tailwind CSS
  * **Deployment:** Docker, Render, Vercel

-----

## ⚡ Getting Started

### Prerequisites

  * Docker & Docker Compose
  * Python 3.10+
  * Node.js 18+

### 1\. Clone the Repository

```bash
git clone https://github.com/adaken4/loan-guard-ai.git
cd loan-guard-ai
```

### 2\. Backend Setup (API & Model)

You can run the backend using Docker (Recommended) or locally.

**Option A: Docker**

```bash
# Build the image
docker build -t loanguard-api .

# Run the container
docker run -p 8000:8000 loanguard-api
```

**Option B: Local Python Env**

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Train the model (creates model/risk_model.pkl)
python -m model.train_model

# Run the API
uvicorn api.main:app --reload
```

*The API will be available at `http://localhost:8000`*

### 3\. Frontend Setup (Dashboard)

```bash
cd frontend
npm install
npm run dev
```

*The dashboard will be available at `http://localhost:3000`*

-----

## 🔌 API Usage

**Endpoint:** `POST /score`

**Request Body:**

```json
{
  "transactions": [
    {"date": "2025-10-01", "amount": 800, "type": "income"},
    {"date": "2025-10-02", "amount": 200, "type": "expense", "category": "gambling"}
  ],
  "repayments": [
    {"loan_id": "L1", "status": "on_time"}
  ]
}
```

**Response:**

```json
{
  "risk_class": "Low Risk",
  "default_probability": 12.5,
  "recommendation": "Approve loan at requested amount"
}
```

-----

## 👥 Team

  * **Solo Developer:** [@adaken4](https://www.google.com/search?q=https://github.com/adaken4)

-----

## 📜 License

Distributed under the MIT License. See `LICENSE` for more information.