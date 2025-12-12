from sklearn.metrics import accuracy_score, classification_report, confusion_matrix, roc_auc_score
import json

def evaluate_model(model, X_test, y_test):
    y_pred = model.predict(X_test)
    y_proba = model.predict_proba(X_test)
    
    metrics = {
        "accuracy": round(accuracy_score(y_test, y_pred), 4),
        "classification_report": classification_report(y_test, y_pred, output_dict=True),
        "confusion_matrix": confusion_matrix(y_test, y_pred).tolist(),
        "roc_auc_ovr": round(roc_auc_score(y_test, y_proba, multi_class='ovr', average='weighted'), 4)
    }
    
    with open("model/metrics.json", "w") as f:
        json.dump(metrics, f, indent=2)
    
    print(f"✅ Model Accuracy: {metrics['accuracy']*100:.2f}%")
    print(f"✅ ROC-AUC Score: {metrics['roc_auc_ovr']:.4f}")
    
    return metrics
