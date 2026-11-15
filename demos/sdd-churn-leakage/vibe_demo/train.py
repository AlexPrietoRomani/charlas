"""Entrenamiento rápido del modelo de churn (versión inicial del equipo)."""

from pathlib import Path

import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

DATA_PATH = Path(__file__).resolve().parent.parent / "data" / "churn_events.csv"
FEATURES = [
    "tenure_months",
    "monthly_spend",
    "support_tickets_30d",
    "usage_drop_pct",
    "post_churn_cancellation_days",
]


def train_and_evaluate() -> float:
    """Entrena el clasificador de churn y retorna el ROC-AUC de validación."""
    df = pd.read_csv(DATA_PATH)
    X = df[FEATURES].fillna(-1.0)
    y = df["churned"]

    X_scaled = StandardScaler().fit_transform(X)
    X_train, X_test, y_train, y_test = train_test_split(
        X_scaled, y, test_size=0.30, random_state=42, stratify=y
    )

    model = LogisticRegression(max_iter=1000)
    model.fit(X_train, y_train)
    probs = model.predict_proba(X_test)[:, 1]
    auc = float(roc_auc_score(y_test, probs))
    print(f"ROC-AUC en validacion: {auc:.4f}")
    return auc


if __name__ == "__main__":
    train_and_evaluate()
