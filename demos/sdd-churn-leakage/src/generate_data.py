"""Genera el dataset sintético de eventos de churn con una fuga temporal plantada.

El dataset simula snapshots mensuales de clientes de una empresa de suscripción.
La columna ``post_churn_cancellation_days`` es la trampa didáctica: registra los
días entre el churn y la cancelación del contrato, un dato que solo existe
DESPUÉS de que el churn ya ocurrió. En un snapshot real nunca podría conocerse.

La generación es determinista (``seed=42``) y corre en milisegundos, para que la
demo en vivo sea reproducible y rápida.

Ejecución:
    python demos/sdd-churn-leakage/src/generate_data.py
"""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd

SEED = 42
N_FILAS_OBJETIVO = 1200
MAX_CLIENTES = 400
N_SNAPSHOTS = 6
FECHA_INICIO = "2024-01-01"
# Desviación estándar del ruido de etiqueta (factores no observables).
RUIDO_ETIQUETA = 1.70
# Probabilidad de que un churn tenga registrado el dato post-churn.
PROB_FUGA_PRESENTE = 0.80

# Esquema esperado del CSV (Golden Data del laboratorio).
COLUMNAS: list[str] = [
    "customer_id",
    "snapshot_date",
    "tenure_months",
    "monthly_spend",
    "support_tickets_30d",
    "usage_drop_pct",
    "post_churn_cancellation_days",
    "churned",
]

DATA_DIR = Path(__file__).resolve().parent.parent / "data"
CSV_PATH = DATA_DIR / "churn_events.csv"


def generar_eventos(seed: int = SEED, n_filas: int = N_FILAS_OBJETIVO) -> pd.DataFrame:
    """Genera snapshots mensuales de clientes con churn simulado y fuga plantada.

    Args:
        seed: Semilla aleatoria; fija la reproducibilidad total del dataset.
        n_filas: Número objetivo de filas (snapshots) a generar.

    Returns:
        DataFrame con el esquema ``COLUMNAS`` y ~``n_filas`` registros.
    """
    rng = np.random.default_rng(seed)
    fechas = pd.date_range(FECHA_INICIO, periods=N_SNAPSHOTS, freq="MS")
    registros: list[dict[str, object]] = []

    cliente_idx = 0
    while len(registros) < n_filas and cliente_idx < MAX_CLIENTES:
        cliente_idx += 1
        cliente_id = f"C{cliente_idx:04d}"
        tenure_inicial = int(rng.integers(3, 37))
        gasto_base = float(rng.lognormal(mean=3.4, sigma=0.35))
        # ~35% de clientes "frágiles": su riesgo sube con el tiempo.
        fragil = bool(rng.random() < 0.35)

        for t in range(N_SNAPSHOTS):
            rampa = t / (N_SNAPSHOTS - 1)
            riesgo = (0.30 + 0.45 * rampa) if fragil else (0.08 * rampa)
            tickets = int(rng.poisson(lam=0.3 + 2.2 * riesgo))
            caida_uso = float(np.clip(rng.normal(2.0 + 20.0 * riesgo, 3.0), 0.0, 60.0))
            tenure = tenure_inicial + t
            gasto = gasto_base * float(np.exp(rng.normal(0.0, 0.03)))

            # Score latente: combinación lineal de señal real observable
            # (tenure, gasto, tickets, uso). Ningún modelo puede hacer mejor
            # que rankear según este score, salvo por el ruido de etiqueta.
            z = (
                -2.4
                - 0.03 * tenure
                + 0.5 * np.log(gasto / 30.0)
                + 1.2 * tickets
                + 0.07 * caida_uso
            )
            # Ruido de etiqueta: factores no observables (mood del cliente,
            # ofertas de la competencia) que impiden un churn determinista.
            se_va = bool(z + rng.normal(0.0, RUIDO_ETIQUETA) > 0.0)

            # FUGA: el dato post-churn solo existe si el churn ya ocurrió
            # (y en ~20% de los churn ni siquiera entonces), para que el AUC
            # falso sea creíble (~0.96) y no una separación perfecta de 1.00.
            if se_va and rng.random() < PROB_FUGA_PRESENTE:
                dias_cancelacion: float | None = float(rng.integers(1, 91))
            else:
                dias_cancelacion = None

            registros.append(
                {
                    "customer_id": cliente_id,
                    "snapshot_date": fechas[t].strftime("%Y-%m-%d"),
                    "tenure_months": tenure,
                    "monthly_spend": round(gasto, 2),
                    "support_tickets_30d": tickets,
                    "usage_drop_pct": round(caida_uso, 2),
                    "post_churn_cancellation_days": dias_cancelacion,
                    "churned": int(se_va),
                }
            )
            if se_va:
                # El cliente se fue: no genera snapshots futuros.
                break

    return pd.DataFrame(registros, columns=COLUMNAS)


def main() -> None:
    """Genera el CSV en ``data/churn_events.csv`` e imprime un resumen."""
    df = generar_eventos()
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    df.to_csv(CSV_PATH, index=False)
    print(f"CSV generado: {CSV_PATH}")
    print(f"Filas: {len(df)} | Clientes: {df['customer_id'].nunique()}")
    print(f"Tasa de churn: {df['churned'].mean():.2%}")
    con_fuga = df["post_churn_cancellation_days"].notna()
    print(
        "Fuga plantada: "
        f"{con_fuga.sum()} filas con post_churn_cancellation_days "
        f"(churned=1 en {int(((con_fuga) & (df['churned'] == 1)).sum())} de ellas)"
    )


if __name__ == "__main__":
    main()
