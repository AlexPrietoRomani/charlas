# demos/sdd-churn-leakage — El modelo de 0.96 AUC que miente en producción

Mini-proyecto **reutilizable de laboratorio en vivo** para la charla de Spec-Driven
Development (SDD) aplicado a Data Science. En ~10 minutos se demuestra, con datos
reproducibles, por qué un pipeline "vibe coding" (sin especificación, sin tests de
contrato) produce un modelo que brilla en el notebook y se desploma en producción.

## El caso real (la historia que abre la charla)

Un equipo de retención de clientes entrena un clasificador de churn y celebra un
**AUC de 0.96**. Lo suben a producción y, a las semanas, las predicciones no sirven:
el modelo no sabe anticipar el churn, solo lo está *recordando*. Dos errores clásicos
conviven en ese notebook:

1. **Fuga temporal (target leakage):** el dataset incluye
   `post_churn_cancellation_days` — los días entre el churn y la cancelación del
   contrato. Ese dato **solo existe cuando el churn ya ocurrió**; en el momento de
   la predicción es imposible conocerlo. El modelo aprende a leer el futuro.
2. **Fuga de preprocesamiento:** el `StandardScaler` se ajusta con
   `fit_transform(X)` sobre **todo** el dataset **antes** del split, así que la
   media y desviación del test set ya contaminaron el entrenamiento. Y encima el
   split es **aleatorio**: snapshots del futuro acaban en el train.

La evaluación honesta — split **temporal** (entrenar con el pasado, evaluar con el
futuro) y solo features disponibles al momento de predecir — muestra el AUC real:
~**0.83**. La brecha no es ruido: es la diferencia entre un dashboard bonito y una
decisión de negocio.

## Estructura

```
demos/sdd-churn-leakage/
├── README.md              ← esta guía
├── AGENTS.md              ← constitución del mini-proyecto para project-suite
├── data/churn_events.csv  ← Golden Data (determinista, seed=42)
├── src/
│   ├── generate_data.py   ← genera el dataset con la fuga plantada
│   └── train_baseline.py  ← antiejemplo: pipeline con fuga + evaluación honesta
└── tests/
    └── test_demo_seed.py  ← contrato del laboratorio (pytest)
```

## Comandos

```bash
# 1. Regenerar el Golden Data (determinista: seed=42, ~1200 filas, <0.5s)
python demos/sdd-churn-leakage/src/generate_data.py

# 2. Correr la demo: AUC falso vs AUC honesto
python demos/sdd-churn-leakage/src/train_baseline.py

# 3. Verificar el contrato del laboratorio
python -m pytest demos/sdd-churn-leakage/tests -v
```

Salida esperada del pipeline (los valores exactos son reproducibles):

```
AUC con fuga (split aleatorio + post_churn): 0.9593
AUC honesto (split temporal, sin fuga):      0.8318
Brecha: 0.1275
```

## Guion de la demo en vivo (~10 min)

### Parte 1 — Vibe Coding (antiejemplo, 3 min)

> *"Necesito un modelo de churn. Pásame los datos y pide el AUC al chat."*

1. Abre `train_baseline.py` y ejecútalo tal cual. Celebra el **0.96** en pantalla.
2. Pregunta al público: *"¿lo subiríamos a producción?"* — alguien siempre dirá que sí.
3. Señala la línea del bug: `StandardScaler().fit_transform(X)` antes del split y la
   columna `post_churn_cancellation_days` dentro de `X`. Explica por qué cada una es
   una fuga y por qué el split aleatorio es una tercera fuga (el futuro en el train).
4. Muestra la evaluación honesta del mismo script: **0.83**. El colapso se ve en vivo.

### Parte 2 — SDD con project-suite (el camino correcto, 5 min)

La misma tarea, pero especificada **antes** de escribir código. Con `project-suite`
instalado, en el directorio del mini-proyecto:

1. **Especificación (`/especificar`):** entrevistado por el agente, defines QUÉ hace el
   sistema y CÓMO fluye el dato. Aquí es donde se escribe la regla que evita la fuga:
   *"las features deben existir en el instante del snapshot; la variable objetivo es el
   churn en los 30 días posteriores; la evaluación es temporal"*.
2. **Arquitectura + modelo de datos:** `architecture.md` y `diseno_db.md` documentan el
   esquema del CSV (el Golden Data de `tests/test_demo_seed.py`) y las políticas de
   escritura por columna.
3. **Plan (`/planificar`):** el spec se convierte en Fases → Sub fases → Tareas en
   `tareas.md`, cada Tarea con su DoD y sus tests.
4. **Construcción (`/construir`):** un subagente por Tarea, siguiendo `python-standards`,
   corriendo `testear` y cerrando con `verificar-dod`. Ningún checkbox `[X]` sin DoD verde.
5. **Coherencia (`auditar-coherencia`):** docs vs código; si el pipeline cambia, el spec
   no se queda atrás.

El contraste pedagógico: el vibe coding produce el 0.96 mentiroso en minutos; el SDD
tarda lo mismo en especificar **la restricción** que habría impedido el despliegue.

### Parte 3 — Cierre (2 min)

- El AUC falso no es un bug del modelo: es un bug del **proceso**. La especificación es
  donde se declaran las invariantes temporales; los tests de contrato (Golden Data) son
  donde se vuelven verificables.
- Moral: *"En ML, el examen importa menos que la validez del examen."*

## Reglas del Golden Data

- El dataset es **determinista** (`seed=42`): cualquier regeneración produce las mismas
  filas, y los AUC de la demo son estables.
- `tests/test_demo_seed.py` es el **contrato**: esquema exacto, >= 1000 filas, la fuga
  solo puede existir en filas con `churned=1`, la brecha debe reproducirse
  (`leaky_auc >= 0.93` > `honest_auc`) y el CLI debe terminar en código 0.
- Si tocás `generate_data.py`, los tests te van a avisar si rompés la trampa didáctica.

---

*Mini-proyecto creado por Alex Prieto <alexprieto1997@gmail.com> para la charla SDD.*
