"""Tests del semilla del taller SDD: reproducibilidad de la demo de data leakage.

Verifica el "contrato" del laboratorio en vivo:
1. El dataset Golden Data existe, es suficientemente grande y tiene el esquema esperado.
2. El antiejemplo reproduce la brecha de fuga: AUC falso >= 0.93 y muy superior al AUC honesto.
3. La simulación CLI del script termina con código 0.

Ejecución (desde la raíz del repo):
    python -m pytest demos/sdd-churn-leakage/tests -v
"""

from __future__ import annotations

import subprocess
import sys
import time
from pathlib import Path

import pandas as pd

SRC_DIR = Path(__file__).resolve().parents[1] / "src"
sys.path.insert(0, str(SRC_DIR))

import train_baseline  # noqa: E402

CSV_PATH = SRC_DIR.parent / "data" / "churn_events.csv"

ESQUEMA_ESPERADO = [
    "customer_id",
    "snapshot_date",
    "tenure_months",
    "monthly_spend",
    "support_tickets_30d",
    "usage_drop_pct",
    "post_churn_cancellation_days",
    "churned",
]


def test_dataset_existe_con_esquema_y_volumen() -> None:
    """El CSV existe, tiene >= 1000 filas y el esquema Golden Data completo."""
    assert CSV_PATH.exists(), (
        f"No existe {CSV_PATH}. Genera el dataset con: "
        "python demos/sdd-churn-leakage/src/generate_data.py"
    )
    df = pd.read_csv(CSV_PATH)
    assert len(df) >= 1000, f"El dataset tiene {len(df)} filas; se esperaban >= 1000"
    assert list(df.columns) == ESQUEMA_ESPERADO
    assert df["churned"].isin([0, 1]).all(), "churned debe ser binario (0/1)"
    assert df["customer_id"].notna().all()
    # Invariante de la fuga: el dato post-churn jamás existe sin churn.
    con_fuga = df["post_churn_cancellation_days"].notna()
    assert (df.loc[con_fuga, "churned"] == 1).all(), (
        "Fuga rota: hay post_churn_cancellation_days en filas sin churn"
    )


def test_brecha_de_fuga_reproducible() -> None:
    """run_baseline() corre en < 3s y reproduce la brecha AUC falso vs honesto."""
    inicio = time.perf_counter()
    resultados = train_baseline.run_baseline()
    duracion = time.perf_counter() - inicio

    assert duracion < 3.0, f"run_baseline() tardó {duracion:.2f}s; debe correr en < 3s"
    assert resultados["leaky_auc"] >= 0.93, (
        f"AUC falso {resultados['leaky_auc']:.4f} < 0.93: la fuga dejó de ser dramática"
    )
    assert resultados["honest_auc"] < resultados["leaky_auc"], (
        "El AUC honesto debe ser estrictamente menor que el AUC con fuga; "
        "si no, la demo pierde su punto pedagógico"
    )


def test_cli_termina_sin_error() -> None:
    """La simulación CLI del script termina con código 0."""
    resultado = subprocess.run(
        [sys.executable, str(SRC_DIR / "train_baseline.py")],
        capture_output=True,
        text=True,
        timeout=60,
    )
    assert resultado.returncode == 0, (
        f"El CLI falló con código {resultado.returncode}:\n{resultado.stderr}"
    )
    assert "AUC" in resultado.stdout, "El CLI debe imprimir los AUC de la demo"
