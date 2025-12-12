import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.calibration import CalibratedClassifierCV
from sklearn.frozen import FrozenEstimator
import joblib
import random
from model.feature_engineering import extract_features
from model.config import PROFILES
from data.simulate_data import simulate_transactions
from model.evaluate_model import evaluate_model

# Generate synthetic training data (in real life: labeled historical data)
def generate_training_data():
    X, y = [], []
    labels = {"good_spender": 0, "gambling_spender": 2, "inconsistent_earner": 1}

    for profile in labels:
        for _ in range(200):
            data = simulate_transactions(profile, month=6)
            feats = list(extract_features(data).values())
            
            base_label = labels[profile]
            final_label = base_label

            # Introduce some noise to the labels for realism
            if base_label == 0 and random.random() < 0.05:
                final_label = 2
            elif base_label == 2 and random.random() < 0.15:
                final_label = 1
            
            X.append(feats)
            y.append(final_label)

    return np.array(X), np.array(y)

X, y = generate_training_data()
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
base_model = RandomForestClassifier(n_estimators=50, random_state=42)
base_model.fit(X_train, y_train)

fronzen_estimator = FrozenEstimator(base_model)

model = CalibratedClassifierCV(
    estimator=fronzen_estimator,
    method='isotonic'
)

model.fit(X_train, y_train)

# Evaluate model
print("\n📊 Evaluating model performance...")
metrics = evaluate_model(model, X_test, y_test)

joblib.dump(model, "model/risk_model.pkl")
print("\n✅ Model trained and saved to model/risk_model.pkl")