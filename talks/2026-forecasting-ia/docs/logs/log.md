# Bitácora de Incidencias y Decisiones Técnicas — Charla Forecasting & IA

Registro cronológico y forense de anomalías, bugs, auditorías y refactorizaciones críticas del proyecto.

---

## 2026-10-04 — Detección y erradicación total de datos sintéticos no declarados en el Caso Café Jaén — `data/`, `scripts/`, `presentacion.html`, `notebooks/`

### 1. Síntoma Observado / Reporte
Durante la auditoría del proyecto previa a la presentación ante audiencia universitaria, se identificó que el dataset `data/cafe_ndvi_rendimiento.csv` (utilizado en la diapositiva del Caso B) contenía valores de rendimiento y NDVI generados artificialmente mediante fórmulas lineales paramétricas acopladas a ruido gaussiano (`np.random.normal`), pretendiendo representar la realidad agrícola de Jaén (Cajamarca). Asimismo, la correlación NDVI vs Rendimiento arrojaba un \(R^2 = 0.788\) artificial que contradecía la literatura biofísica sobre la saturación del dosel foliar en cultivos bajo sombra.

```python
# Traza de generación sintética original en scripts/build_agro_dataset.py:
rendimiento = 20.0 + 15.0 * (ndvi - 0.6) + np.random.normal(0, 1.5, n)
```

### 2. Hipótesis de Diagnóstico
1. **Hipótesis 1 (Descartada):** El archivo `cafe_ndvi_rendimiento.csv` era una exportación preliminar de datos del Ministerio de Agricultura (SIEA) con alguna interpolación menor.
   *Resultado:* Descartada tras auditar el script `scripts/build_agro_dataset.py`, donde se comprobó que el 100% de los datos provenía de un generador sintético sin base de datos real.
2. **Hipótesis 2 (Confirmada):** Existía disponibilidad pública y abierta para reconstruir la serie completa con rigor científico estricto: estadísticas oficiales de producción y superficie del SIEA/MIDAGRI (Compendios Estadísticos INEI Cajamarca 2000–2024), extracción de reflectancia MODIS MOD13Q1 desde Microsoft Planetary Computer STAC con máscara de fiabilidad de pixel, y reanálisis ERA5 vía Open-Meteo Archive.

### 3. Causa Raíz
Prácticas de prototipado rápido previas generaron datos simulados con fines de maquetado visual, pero estos no fueron etiquetados explícitamente como "sintéticos" ni aislados del flujo de producción. Esto generó una ilusión de correlación perfecta (\(r \approx 0.88\)) que vulneraba el principio de rigor metodológico y exponía el discurso a la invalidación ante una audiencia académica.

### 4. Resolución e Implementación
1. **Aislamiento y Trazabilidad:** Se trasladó el archivo simulado a `data/deprecated/cafe_ndvi_rendimiento_SINTETICO.csv` y se creó `data/deprecated/README.md`. Se desactivó `scripts/build_agro_dataset.py`.
2. **Recolección Oficial MIDAGRI/SIEA:** Se creó `scripts/compile_midagri_jaen.py`, extrayendo 24 campañas oficiales (2000–2024) de los compendios del INEI (Lib1492 y CompDptal2025). Se validó la consistencia aritmética (\(\text{producción} \approx \text{superficie} \times \text{rendimiento}\), \(\Delta < 0.1\%\)).
3. **Extracción Satelital Real:** Se implementó `scripts/extract_modis_jaen.py`, descargando concurrentemente 576 compuestos MODIS MOD13Q1 (2000–2024) para el polígono de Jaén (`jaen_limite.geojson`), aplicando filtro de calidad `QA Pixel Reliability`.
4. **Agregación Fenológica Determinista:** Se creó `scripts/build_cafe_real.py` (cero llamadas a `np.random`), fusionando el clima ERA5 por ventanas botánicas (Floración Ago–Oct, Llenado Nov–Feb, Cosecha Mar–Jul) en `data/cafe_jaen_campanias.csv`.
5. **Auditoría Científica de Hipótesis:** Se evaluaron H1 a H4 en `scripts/eval_hipotesis_cafe.py`, confirmando que el NDVI anual satura en copas densas (\(r = 0.154, p = 0.600\)) y que fue totalmente ciego a la crisis de la Roya Amarilla de 2012–2014 (-56.0% en rendimiento vs +1.4% en NDVI).
6. **Refactorización de la Interfaz:** Se reescribió `scripts/build_deck.py` para compilar exactamente 20 diapositivas Split-Screen 40/60, conectadas a los nuevos CSVs reales, con notas de orador (tecla `N`) y sin cifras cableadas a mano.

### 5. Verificación y Mediciones
- `grep -r "np.random" scripts/build_cafe_real.py` devuelve 0 ocurrencias.
- `presentacion.html` contiene exactamente 20 elementos `<section class="slide">`.
- Búsqueda de cifras sintéticas previas (`29.98`, `0.788`, `cafe_ndvi_rendimiento.csv`) limpia en código activo.
- Todos los hashes SHA-256 de las fuentes crudas y derivadas registrados en `data/SOURCES.md`.
- El benchmark de 8 modelos en Iquitos (`data/benchmark_punchana.csv`) y la validación temporal expansiva de café (`data/cafe_jaen_resultados.csv`) operan con reproducibilidad matemática total.

### 6. Lecciones Aprendidas (Retroalimentación)
- **Invariante de Veracidad:** En proyectos de docencia y divulgación científica, nunca se debe mezclar código de prototipado sintético con pipelines de análisis. Si se requiere una simulación para ilustrar un concepto pedagógico (como el cono estocástico o la no-extrapolación), debe rotularse explícitamente en pantalla como `SIMULACIÓN` o `EXPERIMENTO PROPIO`.
- **La física antes del ajuste:** El fracaso del NDVI para anticipar la roya amarilla en Jaén demuestra que ningún hiperparámetro de Machine Learning puede compensar la limitación física de un sensor que solo observa la superficie del dosel forestal.

---

## 2026-10-05 — Refactorización Front-Design: Erradicación de vacíos verticales, márgenes en 4 lados y enriquecimiento visual — `scripts/deck_styles.py`, `scripts/deck_slides_p1.py`, `scripts/deck_slides_p2.py`, `scripts/build_deck.py`

### 1. Síntoma Observado / Reporte
Durante la inspección visual en navegador de las 20 diapositivas generadas (`presentacion.html`), se evidenciaron tres problemas estéticos y de legibilidad para proyección en auditorio:
1. Vacíos verticales excesivos (>80px, alcanzando hasta ~350px en el panel narrativo de diapositivas con poco texto).
2. Ausencia de márgenes perimetrales: el contenido tocaba los bordes superior, inferior y laterales de la pantalla, transmitiendo sensación de encajonamiento.
3. Elementos visuales subdimensionados: tipografía pequeña (11-12px) ilegible a distancia, SVGs con coordenadas estrechas que producían colisiones de etiquetas (e.g., en Slide 08 entre NDVI ~0.80 y ZONA SATURACIÓN; en Slide 09 etiqueta COSECHA colisionando con el borde del donut fenológico), y falta de interacción para ampliar infografías de alta densidad creadas con NotebookLM.

### 2. Hipótesis de Diagnóstico
1. **Hipótesis 1 (Confirmada):** El layout flex/grid estiraba los contenedores a `height: 100%`, pero los componentes internos carecían de metadatos estructurados secundarios (KPIs, especificaciones de cómputo, badges de verificación).
2. **Hipótesis 2 (Confirmada):** Los SVGs tenían `viewBox` estáticos muy reducidos (e.g., 460x210 para Slide 09) que no escalaban proporcionalmente al ancho disponible en monitores 1080p.
3. **Hipótesis 3 (Confirmada):** Las infografías ricas generadas por IA estaban limitadas a miniaturas sin mecanismo de zoom, perdiendo el detalle de telemetría de drones y descomposición ontológica.

### 3. Causa Raíz
El diseño previo priorizó la estructura mínima semántica sin considerar la escala real de visualización en pantallas Full HD (1920×1080) ni la distancia focal de un auditorio universitario, dejando grandes huecos blancos bajo las tarjetas de texto y sub-utilizando el panel visual.

### 4. Resolución e Implementación
1. **Sistema de Espaciado y Tokens (`scripts/deck_styles.py`):**
   - Se introdujeron tokens CSS: `--deck-pad-x: clamp(24px, 2.5vw, 44px)`, `--deck-pad-y: clamp(16px, 2.0vh, 28px)`, `--deck-gap: clamp(18px, 1.8vw, 28px)`.
   - Se aplicó encuadre perimetral en 4 lados sobre `.deck-container` y `.slide` con `inset: var(--deck-pad-y) var(--deck-pad-x)`.
   - Se escaló la tipografía: títulos (22–30px), tesis (14–16px), viñetas (13–14.5px), notas técnicas mono (10.5–12.5px).
   - Se estilizó `.card-frase-clave` con bordes de 5px y gradientes sutiles.
2. **Componente `.kpi-strip`:** Se implementó una barra superior de 4 tarjetas de métricas en los paneles visuales, anclando datos reales verificados (`data/*.csv` y `data/*.json`) y eliminando el espacio muerto superior.
3. **Re-ingeniería Vectorial (SVGs):**
   - Slide 08: Se separaron coordenadas verticales (`y=20` vs `y=42`) entre NDVI y saturación.
   - Slide 09: Se expandió el viewBox a `0 0 740 280` (`cx=370, cy=140, r=90`), eliminando solapamientos con las fases fenológicas.
   - Slide 06: Se sustituyeron bloques de texto plano por diagramas vectoriales de arquitecturas (LSTM loop vs PatchTST patch projection).
4. **Modal Lightbox Interactivo (`scripts/build_deck.py`):**
   - Se integró un modal accesible con zoom para infografías NotebookLM en Slides 02 y 15 con tecla `Escape` o clic de cierre.
5. **Rediseño Completo de Diapositivas 11–20 (`scripts/deck_slides_p2.py`):**
   - Slide 11: Malla icosaédrica multiescala + KPI strip.
   - Slide 12: Mapa vectorial de confluencia de ríos Nanay/Amazonas/Itaya + sensor Punchana + serie SENAMHI.
   - Slide 13: Benchmark 8 modelos con test Diebold-Mariano y ranking operativo.
   - Slide 14: Demo interactiva 7d con bandas P10–P90 y conmutadores.
   - Slide 15: Telemetría dron CENFROCAFE con HUD activo y serie oficial SIEA 2000–2024.
   - Slide 16: Dispersión y prueba forense de ceguera de roya.
   - Slide 17: Validación temporal Walk-Forward expansiva.
   - Slide 18: 5 mandamientos estructurados como tarjetas horizontales con números `01` a `05` e insignias por categoría.
   - Slide 19: Árbol de decisión con flujo condicional y tarjetas de colores diferenciados.
   - Slide 20: Repositorio abierto con código QR vectorial nítido, 49 citas y garantías de reproducibilidad.

### 5. Verificación y Mediciones
- Auditoría automatizada vía Playwright en `scripts/audit_layout.py` sobre 1920×1080:
  - En las 20 diapositivas: `emptyPx <= 31px` en narrativa y `emptyPx <= 25px` en visual (equivalente a 3% de padding base estricto). Cero vacíos > 80px.
- Verificación funcional vía `scripts/verify_presentation.py`:
  - 20 diapositivas cargadas exitosamente.
  - 0 advertencias o errores en consola JavaScript.
  - 100% de los canvas y SVGs con datos reales renderizados.

### 6. Lecciones Aprendidas
- **Diseño orientado a la densidad de información (Tufte):** Los espacios en blanco en presentaciones técnicas no se resuelven aumentando arbitrariamente el tamaño de fuente, sino estructurando capas secundarias de información relevante (unidades físicas, latencias de cómputo, valores p de pruebas estadísticas).
- **Consistencia perimetral:** Garantizar un encuadre visual con márgenes reales en los cuatro lados evita la fatiga visual del espectador y transmite rigor profesional de nivel publicación.

