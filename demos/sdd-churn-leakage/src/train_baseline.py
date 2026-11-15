"""Script semilla (ANTIEJEMPLO de taller): entrena con fuga temporal y lo desenmascara.

Este módulo es el corazón de la demo en vivo. Ejecuta DOS evaluaciones sobre el
mismo dataset y las confronta:

1. **Pipeline con fuga (antiejemplo):** escala TODO el dataset con
   ``StandardScaler().fit_transform(X)`` ANTES de hacer el split aleatorio
   (data leakage clásico de preprocesamiento) e incluye la columna
   ``post_churn_cancellation_days``, que solo existe cuando el churn ya
   ocurrió (fuga temporal). Resultado: un AUC falso ~0.96+.

2. **Evaluación honesta:** split temporal (entrena con snapshots antiguos,
   evalúa con snapshots futuros) usando solo features disponibles en el
   momento de la predicción. Resultado: el AUC real, claramente menor.

Ejecución:
    python demos/sdd-churn-leakage/src/train_baseline.py
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

SEED = 42
DATA_PATH = Path(__file__).resolve().parent.parent / "data" / "churn_events.csv"

# Features legítimas: todas conocidas EN el momento del snapshot.
FEATURES_HONESTAS: list[str] = [
    "tenure_months",
    "monthly_spend",
    "support_tickets_30d",
    "usage_drop_pct",
]
# Antiejemplo: se suma la columna post-churn, imposible de conocer a tiempo.
FEATURES_FUGA: list[str] = FEATURES_HONESTAS + ["post_churn_cancellation_days"]

# Split temporal: entrena con snapshots anteriores al corte, evalúa con los
# posteriores (simula producción: el futuro nunca estuvo en el entrenamiento).
FECHA_CORTE_TEST = "2024-05-01"


def run_baseline(data_path: Path = DATA_PATH) -> dict[str, float | str]:
    """Ejecuta el pipeline con fuga y la evaluación honesta sobre el dataset.

    Args:
        data_path: Ruta al CSV de eventos de churn.

    Returns:
        Diccionario con ``leaky_auc`` (AUC falso), ``honest_auc`` (AUC real),
        ``brecha`` (diferencia) y ``mensaje`` (veredicto legible).
    """
    df = pd.read_csv(data_path, parse_dates=["snapshot_date"])
    target = df["churned"]

    # --- 1. Antiejemplo: fuga de preprocesamiento + fuga temporal ---
    X_fuga = df[FEATURES_FUGA].fillna(-1.0)  # -1 = "dato no disponible aún"
    # BUG DIDÁCTICO: el scaler aprende media/desviación de TODO el dataset
    # (incluye el test set) antes de partir los datos.
    X_fuga_escalado = StandardScaler().fit_transform(X_fuga)
    X_train, X_test, y_train, y_test = train_test_split(
        X_fuga_escalado,
        target,
        test_size=0.30,
        random_state=SEED,
        stratify=target,
    )
    modelo_fuga = LogisticRegression(max_iter=1000).fit(X_train, y_train)
    leaky_auc = float(roc_auc_score(y_test, modelo_fuga.predict_proba(X_test)[:, 1]))

    # --- 2. Evaluación honesta: split temporal, sin fuga ---
    entrenamiento = df["snapshot_date"] < FECHA_CORTE_TEST
    prueba = ~entrenamiento
    pipeline_honesto = make_pipeline(
        StandardScaler(),
        LogisticRegression(max_iter=1000),
    )
    pipeline_honesto.fit(df.loc[entrenamiento, FEATURES_HONESTAS], target[entrenamiento])
    probas = pipeline_honesto.predict_proba(df.loc[prueba, FEATURES_HONESTAS])[:, 1]
    honest_auc = float(roc_auc_score(target[prueba], probas))

    return {
        "leaky_auc": leaky_auc,
        "honest_auc": honest_auc,
        "brecha": leaky_auc - honest_auc,
        "mensaje": (
            f"El modelo con fuga promete AUC={leaky_auc:.3f}, "
            f"pero en producción vale AUC={honest_auc:.3f} "
            f"(brecha de {leaky_auc - honest_auc:.3f})."
        ),
    }


def main() -> None:
    """Imprime el veredicto de la demo y termina con código 0."""
    resultados = run_baseline()
    print("=" * 62)
    print("DEMO: El modelo de 0.96 AUC que miente en producción")
    print("=" * 62)
    print(f"AUC con fuga (split aleatorio + post_churn): {resultados['leaky_auc']:.4f}")
    print(f"AUC honesto (split temporal, sin fuga):      {resultados['honest_auc']:.4f}")
    print(f"Brecha: {resultados['brecha']:.4f}")
    print(resultados["mensaje"])


if __name__ == "__main__":
    main()
