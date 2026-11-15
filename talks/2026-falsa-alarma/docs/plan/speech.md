# Speech — Falsa alarma o amenaza real

Guía de lo que se debe decir por diapositiva. No es un guion literal, sino los puntos clave que el presentador debe cubrir.

Cada diapositiva tiene:
- **Qué decir:** Puntos clave del discurso
- **Fundamento técnico:** Conceptos técnicos que respaldan lo dicho (para saber cuánto explayarse)
- **Nivel de profundidad:** Si conviene ir profundo (P) o superficial (S) según la audiencia

---

## 01. APERTURA

**Qué decir:**
- "Hoy les voy a contar una historia sobre agricultura de precisión en el Valle del Elqui, Chile."
- "Un modelo predictivo de heladas con 96% de exactitud. Suena perfecto, ¿no?"
- "El dilema es: ¿qué pasa con ese 4% restante? ¿Importa?"
- Presentar el título: "Falsa alarma o amenaza real — el dilema oculto detrás de cada dato."

**Fundamento técnico:**
- El 96% de accuracy se calcula como `(TP + TN) / (TP + TN + FP + FN)`.
- Con datos desbalanceados (91% noches sin helada), un modelo trivial que siempre prediga "sin helada" obtiene 91% de accuracy.
- La métrica esconde la distribución de errores: ¿cuántos de esos 4% son FP vs. FN?

**Nivel:** S — Solo plantear la paradoja, no resolverla aún.

**Tiempo sugerido:** 1 minuto

---

## 02. TEORÍA

**Qué decir:**
- "Los datos no se explican solos. Necesitan una historia."
- Presentar el libro *Storytelling with Data* de Cole Nussbaumer Knaflic.
- "La metodología no es solo hacer gráficos bonitos. Es estructurar una narrativa que conduzca a una acción."
- "El objetivo es pasar de datos crudos a una decisión informada."

**Fundamento técnico:**
- **Teoría de la carga cognitiva (Sweller, 1988):** El cerebro tiene capacidad limitada para procesar información nueva. Las visualizaciones deben minimizar la carga extrínseca (ruido) y maximizar la intrínseca (datos útiles).
- **Atributos preatentivos:** Color, tamaño, orientación y forma se procesan en <500ms antes de la atención focalizada. Se usan para dirigir la mirada sin esfuerzo consciente.
- **Narrativa:** La estructura clásica (gancho → tensión → resolución) activa la memoria episódica, haciendo que el mensaje se retenga mejor que una lista de métricas.

**Nivel:** S — Mencionar el marco sin profundizar en teoría cognitiva.

**Tiempo sugerido:** 1.5 minutos

---

## 03. METODOLOGÍA

**Qué decir:**
- "Hay un proceso de 6 pasos para llegar de los datos a la narrativa:"
  1. Entender el contexto (¿quién escucha? ¿qué necesita saber?)
  2. Elegir la visualización adecuada
  3. Eliminar el ruido visual
  4. Enfocar la atención con atributos preatentivos
  5. Pensar como diseñador (jerarquía, alineación)
  6. Contar una historia con gancho, desarrollo y desenlace
- "Este marco lo aplicamos al caso de las heladas."

**Fundamento técnico:**

**Paso 1 — Contexto:**
- Identificar audiencia (gerente vs. técnico), decisión que debe tomar, y nivel de conocimiento previo.
- Un gerente necesita ROI; un científico necesita methodology.
- **Marco de stakeholders (Lecoutre, 2016):** Cada audiencia tiene un "nivel de decisión":
  - **Estratégica:** ¿Invertimos en este modelo? (C-suite)
  - **Operativa:** ¿Activamos la aspersión esta noche? (Supervisor de campo)
  - **Táctica:** ¿Qué umbral usamos? (Analista de datos)

**Paso 2 — Visualización:**
- Series de tiempo para tendencias, tablas para comparaciones exactas, scatter plots para correlaciones.
- **Teorema de la inmunidad del estilo (Cleveland & McGill, 1984):** La precisión perceptual varía por tipo de gráfico:
  1. Posición a lo largo de una escala común (mejor) → barras, scatter
  2. Posición sin escala comun → diagramas de caja
  3. Longitud → barras
  4. Ángulo/pendiente → pie charts, gauges (peor)
- **Regla:** Elegir el gráfico que maximice la precisión perceptual para la tarea (comparación, tendencia, distribución).

**Paso 3 — Ruido:**
- Gridlines, bordes 3D, gradientes decorativos. Tufte lo llama "chartjunk".
- **Principio de la tinta de datos (Tufte, 1983):** La proporción de tinta que comunica datos vs. tinta total debe ser máxima.
- **Data-ink ratio:** `(Tinta de datos) / (Tinta total)`. Ideal: >70%.
- **Ejemplo:** Un gráfico con gridlines, bordes y leyendas innecesarias tiene ~40% data-ink. Sin esos elementos: ~85%.

**Paso 4 — Preatentivos:**
- Color rojo para alertas, tamaño proporcional al valor, contraste para jerarquía.
- **Teoría de la preatención (Treisman, 1985):** El sistema visual humano detecta "discontinuidades" en <200ms antes de la atención focalizada.
- **Atributos preatentivos efectivos:** Color (rojo vs. gris), tamaño (grande vs. pequeño), orientación (vertical vs. horizontal), forma (círculo vs. cuadrado).
- **Uso deliberado:** Si todo es rojo, nada es rojo. El color debe reservarse para lo que importa.

**Paso 5 — Diseño:**
- Alineación, espaciado consistente, regla de tercios.
- **Gestalt (Koffka, 1935):** El cerebro agrupa elementos por proximidad, similitud, continuidad y cierre.
- **Jerarquía visual:** Tamaño → peso → color → posición. Lo más importante = más grande, más oscuro, más arriba.

**Paso 6 — Narrativa:**
- Gancho (dato impactante), tensión (problema), resolución (acción concreta).
- **Estructura de 3 actos (Aristóteles):**
  1. **Inicio:** Establece el mundo (el 96% de accuracy)
  2. **Medio:** Introduce el conflicto (el 4% que falla cuesta US$ 53.500)
  3. **Fin:** Resolución (subir el umbral ahorra US$ 48.950)
- **Principio de "start with why" (Sinek, 2009):** No empezar con qué (el modelo), sino por qué (el costo del error).

**Nivel:** P si la audiencia es de DS/DA; S si es gerencial.

**Tiempo sugerido:** 2 minutos (P: 4-5 minutos con toda la teoría)

---

## 04. COMPARATIVA

**Qué decir:**
- "Comparemos dos enfoques: el tradicional vs. el estratégico."
- **Tradicional:** El analista exporta métricas a un reporte plano → el gerente lo archiva → nadie actúa → el error se repite.
- **Estratégico:** Se identifica el patrón clave → se contextualiza con storytelling → se toma una decisión → se mide el impacto.
- "La diferencia no es la tecnología, es la narrativa."

**Fundamento técnico:**
- **Flujo tradicional (inercial):** Datos → Excel → email → archivador. El problema: no hay feedback loop. El modelo se entrena una vez y nunca se recalibra.
- **Flujo estratégico:** Datos → análisis → narrativa → decisión → monitoreo → recalibración. Incluye un ciclo de retroalimentación continuo.
- **Concepto clave:** El valor de un modelo no está en su precisión técnica, sino en si genera una acción medible. Un modelo perfecto que nadie interpreta tiene valor cero.

**Nivel:** S — Mostrar la diferencia visual sin entrar en detalles de implementación.

**Tiempo sugerido:** 2 minutos

---

## 05. STORYTELLING PARA DA Y DS

**Qué decir:**
- "¿Qué cambia entre contar una historia para un equipo de Analytics vs. Data Science?"
- **DA (Analytics):** Enfoque en tendencias, reportes, KPIs. Audiencia: gerencia, operaciones.
- **DS (Data Science):** Enfoque en modelos, predicciones, error. Audiencia: técnicos, inversión.
- "Ambos necesitan storytelling. El DS a menudo lo olvida: cree que el modelo se vende solo."

**Fundamento técnico:**

**DA — Analytics:**
- El producto es un dashboard o reporte. La audiencia quiere saber "¿cómo estamos?" → KPIs, tendencias, comparaciones.
- El storytelling es **horizontal**: resumen ejecutivo → detalle por dimensión.
- **Marco CRISP-DM (Cross-Industry Standard Process for Data Mining):**
  1. Business Understanding → ¿Qué KPI importa?
  2. Data Understanding → ¿De dónde viene?
  3. Data Preparation → ¿Limpieza, agregación?
  4. Modeling → No siempre. A veces con SQL basta.
  5. Evaluation → ¿Respondió la pregunta?
  6. Deployment → Dashboard, reporte, alerta.
- **Error común:** Saltar al dashboard sin entender la pregunta de negocio.

**DS — Data Science:**
- El producto es un modelo o predicción. La audiencia quiere saber "¿qué va a pasar?" → forecast, intervals, confidence.
- El storytelling es **vertical**: supuestos → datos → modelo → predicción → validación → impacto.
- **Marco de comunicabilidad (Breiman, 2001):** Los dos cultos del DS:
  - **Culto de los datos:** "Los datos hablan por sí solos" → error. Los datos necesitan contexto.
  - **Culto de los modelos:** "El modelo es la respuesta" → error. El modelo es una herramienta, no un fin.
- **Error común del DS:** Presentar la arquitectura del modelo (random forest, XGBoost) en vez del impacto del negocio. El gerente no le importa el algoritmo, le importa si le ahorró dinero.
- **Regla de oro:** Si no puedes explicar el resultado sin usar la palabra "modelo", no lo has entendido lo suficiente para presentarlo.

**Nivel:** P si la audiencia es DS; S si es mixta.

**Tiempo sugerido:** 1.5 minutos (P: 3 minutos)

---

## 06. CONTEXTO

**Qué decir:**
- "Estamos en el Valle del Elqui, Coquimbo, Chile. Latitud 30.03° S."
- "Cultivo: fresa (Fragaria ananassa). Temporada: invierno 2025."
- "Los datos climáticos vienen de la API de Open-Meteo, con downscaling de modelos NOAA GFS y ECMWF."
- "El umbral de daño por helada es -0.5 °C. Por debajo de eso, la flor se congela."

**Fundamento técnico:**
- **Open-Meteo API:** Provee pronósticos meteorológicos abiertos usando modelos numéricos (GFS de NOAA, ECMWF de Europa). Resolución: hasta 1km con downscaling estadístico.
- **Umbral de daño (-0.5 °C):** La fresa en floración es extremadamente sensible. A -0.5 °C, el agua intracelular se congela, rompe las paredes celulares y la flor muere. No hay recuperación.
- **Downscaling:** Los modelos globales resuelven a ~10km. El downscaling estadístico (regresión + elevación) lo reduce a ~1km, capturando microclimas del valle.

**Nivel:** S — Contexto geográfico y agronómico, sin entrar en detalles de downscaling.

**Tiempo sugerido:** 1 minuto

---

## 06. LA TENSIÓN

**Qué decir:**
- "Aquí es donde la historia se pone interesante."
- "Tenemos un modelo que funciona el 96% de las noches. Pero el 4% que falla… falla justo cuando importa."
- "La tensión es: ¿confiamos ciegamente en el modelo, o diseñamos una estrategia de respaldo?"

**Fundamento técnico:**

**Paradoja de la exactitud:**
- Accuracy alta + error costoso = ilusión de seguridad.
- Es el mismo problema que en medicina: una prueba con 99% de accuracy que falla el 1% de los casos fatales es inútil para enfermedades letales.
- **Ejemplo clínico:** Un test de cáncer con 99% de accuracy y 1% de FN. Si la enfermedad afecta a 1 de 10.000 personas, el 1% de FN = 0.1 personas perdidas por cada 10.000 testeadas. Pero el 1% de FP = 100 personas con falsa alarma. La utilidad del test depende del costo relativo.

**Distribución del error:**
- No todos los errores son iguales. Un FP (falsa alarma) cuesta US$ 650. Un FN (amenaza no detectada) cuesta US$ 53.500.
- La accuracy no distingue entre ellos.
- **Descomposición de la accuracy:**
  ```
  Accuracy = (TP + TN) / Total
            = P(Positive) × Recall + P(Negative) × Specificity
            = 0.09 × 0.86 + 0.91 × 0.99
            = 0.077 + 0.901
            = 0.978 ≈ 96%
  ```
  - El 91% de specificity (TN/Total) domina la accuracy porque los negativos son la mayoría.
  - El recall del 86% es bajo pero no se ve porque los positivos son pocos.

**Concepto clave — Pérdida esperada:**
- La métrica correcta no es accuracy, sino la **pérdida esperada**:
  ```
  L = C(FP) × P(FP) + C(FN) × P(FN)
    = 650 × 0.067 + 53,500 × 0.013
    = 43.5 + 695.5
    = US$ 739 por noche esperada
  ```
- Minimizar L ≠ Maximizar accuracy.
- **Umbral óptimo:** El umbral donde `dL/dU = 0`, es decir, donde el costo marginal de un FP adicional iguala el beneficio marginal de evitar un FN.

**Nivel:** P — Es el corazón del problema. Vale la pena detenerse.

**Tiempo sugerido:** 1 minuto (P: 3-4 minutos con las fórmulas)

---

## 07. CONCEPTOS

**Qué decir:**
- "Necesitamos entender dos conceptos clave: Error Tipo I y Error Tipo II."
- **Error Tipo I (Falsa Alarma):** El modelo dice "helada" pero no heló. Costo: agua y energía desperdiciadas.
- **Error Tipo II (Amenaza No Detectada):** El modelo dice "seguro" pero heló. Costo: pérdida de cultivo.
- "En agricultura, el Error Tipo II es mucho más caro que el Tipo I."

**Fundamento técnico:**

**Inferencia estadística (Neyman-Pearson, 1933):**
- **Hipótesis nula (H₀):** No hay helada (clase negativa)
- **Hipótesis alternativa (H₁):** Hay helada (clase positiva)
- **Error Tipo I (α):** Rechazar H₀ cuando es verdadera → falsa alarma
  - `α = P(Decidir "helada" | No hay helada) = FP / (FP + TN)`
  - En nuestro caso: α = 5 / 68 = **0.074 (7.4%)**
- **Error Tipo II (β):** No rechazar H₀ cuando es falsa → amenaza no detectada
  - `β = P(Decidir "no helada" | Hay helada) = FN / (FN + TP)`
  - En nuestro caso: β = 1 / 6 = **0.167 (16.7%)**
- **Potencia:** `1 - β` = probabilidad de detectar la helada cuando ocurre
  - Potencia = 1 - 0.167 = **0.833 (83.3%)**

**Matriz de decisión completa:**
|  | H₀ verdadera (No helada) | H₁ verdadera (Helada) |
|---|---|---|
| **Decidir H₀ (No proteger)** | ✅ TN (68 noches) = US$ 0 | ❌ FN (1 noche) = US$ 53,500 |
| **Decidir H₁ (Proteger)** | ⚠️ FP (5 noches) = US$ 3,250 | ✅ TP (5 noches) = US$ 3,250 |

**Asimetría de costos:**
- `C(FN) / C(FP) = 53,500 / 650 = 82.3×`
- **Teorema de minimización de pérdidas (deGroot, 1970):** El umbral de decisión óptimo no es el que maximiza la probabilidad de acierto, sino el que minimiza la pérdida esperada:
  ```
  Umb* = F⁻¹[ C(FP) / (C(FP) + C(FN)) ]
  ```
  donde F es la distribución de temperaturas pronosticadas.
- **En nuestro caso:** Umb* = F⁻¹[650 / (650 + 53,500)] = F⁻¹[0.012] ≈ umbral muy bajo
  - Pero esto asume que la distribución es perfecta. En la práctica, el umbral se ajusta por la incertidumbre del modelo.

**Conexión con test de hipótesis:**
- En estadística clásica, α se fija (típicamente 0.05) y se minimiza β.
- Aquí, los costos son asimétricos, así que α y β se ajustan conjuntamente para minimizar la pérdida total.
- Es lo que Neyman y Pearson llamaron "test más poderoso" para un nivel de significancia dado, pero con la extensión de que el nivel de significancia óptimo depende de los costos.

**Nivel:** P — Conceptos fundamentales. Explicar con paciencia.

**Tiempo sugerido:** 2 minutos (P: 5-6 minutos con la teoría completa)

---

## 08. DIAGRAMAS

**Qué decir:**
- "Veamos cómo fluyen las decisiones en un sistema agrícola tradicional vs. estratégico."
- Mostrar los diagramas Mermaid: el flujo de datos → modelo → decisión → consecuencia.
- "Note cómo el flujo estratégico incluye retroalimentación y monitoreo continuo."

**Fundamento técnico:**
- **Diagrama tradicional (sin feedback):**
  ```
  Datos → Modelo → Predicción → Decisión → Resultado (se acabó)
  ```
  - Sin monitoreo, sin recalibración, sin aprendizaje.
- **Diagrama estratégico (con feedback):**
  ```
  Datos → Modelo → Predicción → Decisión → Resultado
                ↑                              ↓
                └──── Recalibración ←── Monitoreo
  ```
  - Incluye un ciclo de vida completo: predicción → decisión → validación → ajuste.
- **Concepto clave:** El modelo no es estático. Debe adaptarse a cambios en el clima, costos y tecnología.

**Nivel:** S — Los diagramas hablan por sí solos.

**Tiempo sugerido:** 1.5 minutos

---

## 09. VALORIZACIÓN

**Qué decir:**
- "Ahora hablemos de dinero. ¿Cuánto cuesta cada tipo de error?"
- **Falsa alarma:** US$ 650 por noche (agua + energía + personal).
- **Amenaza no detectada:** US$ 53.500 por noche (pérdida de cultivo en floración).
- "Un solo Error Tipo II cuesta 82 veces más que todas las falsas alarmas combinadas."

**Fundamento técnico:**
- **Costo de falsa alarma (FP):**
  - Agua: ~200 m³ × US$ 1.5/m³ = US$ 300
  - Energía (bombeo): US$ 150
  - Personal nocturno: US$ 200
  - **Total: US$ 650/noche**
- **Costo de amenaza no detectada (FN):**
  - Pérdida de floración: 100% de la producción del sector D
  - US$ 53.500 (estimación basada en rendimiento histórico × precio FOB)
- **Ratio:** 53.500 / 650 = **82.3×**
- **Matriz de decisión:**
  | | Helada real (Sí) | No helada (No) |
  |---|---|---|
  | **Proteger** | TP (US$ 650) | FP (US$ 650) |
  | **No proteger** | FN (US$ 53.500) | TN (US$ 0) |

**Nivel:** P si la audiencia quiere ver los números; S si solo necesitan el impacto.

**Tiempo sugerido:** 1.5 minutos

---

## 10. TRADE-OFF

**Qué decir:**
- "Aquí es donde entra la Teoría de Detección de Señales (SDT)."
- "No se puede eliminar un error sin aumentar el otro. Hay un trade-off."
- "La pregunta no es '¿cero errores?' sino '¿cuánto estoy dispuesto a pagar por reducir el riesgo?'"
- "Es la misma tensión que existe en medicina (pruebas falsas positivas) o en ciberseguridad (falsas alarmas de intrusión)."

**Fundamento técnico:**

**Teoría de Detección de Señales (SDT) — Green & Swets (1966):**
- **Origen:** Desarrollada durante la Segunda Guerra Mundial para detectar submarinos en ruidos de fondo oceánico.
- **Conceptos clave:**
  - **Señal (S):** Distribución de temperatura cuando SÍ hay helada. Media: μ_S, Desviación: σ_S.
  - **Ruido (N):** Distribución de temperatura cuando NO hay helada. Media: μ_N, Desviación: σ_N.
  - **Sensibilidad (d'):** Distancia entre las dos distribuciones normalizadas:
    ```
    d' = (μ_S - μ_N) / σ
    ```
    Un d' alto = el modelo distingue bien entre helada y no helada.
  - **Umbral (c):** Punto de corte entre las distribuciones. Determina el balance FP/FN.

**Curva ROC (Receiver Operating Characteristic):**
- **Eje X:** Tasa de FP = 1 - Especificidad = FP / (FP + TN)
- **Eje Y:** Tasa de TP = Sensibilidad = Recall = TP / (TP + FN)
- **Cada punto de la curva** corresponde a un umbral diferente.
- **AUC (Area Under the Curve):** Probabilidad de que el modelo clasifique un positivo más alto que un negativo. AUC = 0.5 = aleatorio; AUC = 1.0 = perfecto.
- **El punto óptimo NO es el de mayor AUC.** Es el que minimiza la pérdida según los costos.

**Punto óptimo en la curva ROC:**
- **Método del "cost curve" (Drummond & Holte, 2006):**
  1. Para cada punto (FPR, TPR) de la ROC, calcular la pérdida:
     ```
     L = C(FP) × FPR × P(N) + C(FN) × (1 - TPR) × P(P)
     ```
  2. El punto óptimo es el de menor L.
  3. Visualmente: dibujar una línea con pendiente `-C(FP)×P(N) / [C(FN)×P(P)]` y encontrar dónde es tangente a la curva.

**Fórmula del umbral óptimo (bayesiano):**
- Si asumimos distribuciones normales:
  ```
  Umb* = (μ_S + μ_N) / 2 + σ² × ln[C(FP)×P(N) / C(FN)×P(P)] / (μ_S - μ_N)
  ```
- **Interpretación:**
  - Primer término: punto medio entre las distribuciones (umbral de máxima exactitud).
  - Segundo término: ajuste por asimetría de costos y priors.
  - Si `C(FN) >> C(FP)`, el segundo término es negativo → el umbral se mueve hacia la derecha (más conservador).

**En nuestro caso:**
- μ_S ≈ -1.5 °C (temperatura cuando hay helada)
- μ_N ≈ 4.0 °C (temperatura cuando no hay helada)
- σ ≈ 2.5 °C (variabilidad del pronóstico)
- d' = (4.0 - (-1.5)) / 2.5 = **2.2** (sensibilidad moderada-alta)
- Con costos 82:1, el umbral óptimo se desplaza ~2σ hacia la derecha del punto medio.

**Nivel:** P — Es el concepto más técnico de la presentación. Usar si hay tiempo.

**Tiempo sugerido:** 1.5 minutos (P: 5-7 minutos con la teoría completa)

---

## 11. MÉTRICAS

**Qué decir:**
- "La exactitud (accuracy) es una métrica engañosa para datos desbalanceados."
- "Un modelo que siempre dice 'no habrá helada' acierta 91% de las noches. ¿Es bueno? No."
- "Necesitamos métricas que capturen la asimetría: precisión, recall, F1, y especialmente la matriz de costo."
- "La exactitud esconde el error que más importa."

**Fundamento técnico:**

**Métricas estándar (definiciones formales):**

| Métrica | Fórmula | Interpretación | Valor nuestro |
|---|---|---|---|
| **Accuracy** | `(TP+TN)/Total` | % de predicciones correctas | 96% |
| **Precisión** | `TP/(TP+FP)` | % de alarmas que son reales | 50% (5/10) |
| **Recall (Sensibilidad)** | `TP/(TP+FN)` | % de heladas detectadas | 86% (5/6) |
| **Especificidad** | `TN/(TN+FP)` | % de no-heladas detectadas | 93% (68/73) |
| **F1-Score** | `2×(P×R)/(P+R)` | Media armónica de P y R | 63% |
| **Fβ-Score** | `(1+β²)×(P×R)/(β²×P+R)` | F1 ponderado (β>1 favorece recall) | Ver abajo |

**Fβ-Score y la asimetría:**
- F1 asume que precision y recall son igualmente importantes. No lo son.
- F2 Score (β=2) pesa el recall 2× más que la precision:
  ```
  F2 = 5×P×R / (4×P + R)
  ```
- F0.5 Score (β=0.5) pesa la precision 2× más que el recall.
- **En nuestro caso:** F2 = 5×0.5×0.86 / (4×0.5 + 0.86) = 2.15 / 2.86 = **0.75**
  - Mejor que F1 (0.63) porque penaliza más los FN.

**Métrica de negocio (la que importa):**
- **Pérdida esperada:**
  ```
  L = C(FP) × FP + C(FN) × FN
    = 650 × 5 + 53,500 × 1
    = 3,250 + 53,500
    = US$ 56,750 (total temporada)
  ```
- **Pérdida por noche esperada:**
  ```
  L_per_night = L / 75 noches = US$ 756.67
  ```
- Minimizar L ≠ Maximizar accuracy.

**Comparación de modelos:**

| Modelo | Accuracy | Recall | F1 | Pérdida total |
|---|---|---|---|---|
| Siempre "no helada" | 91% | 0% | 0 | US$ 374,500 |
| Umbral 2°C (actual) | 96% | 86% | 63% | US$ 56,750 |
| Umbral 3°C | 93% | 100% | 53% | US$ 4,550 |
| Umbral 3.5°C | 91% | 100% | 48% | US$ 4,550 |

- El umbral 3°C tiene peor accuracy (93% vs 96%) pero 12× más barato.
- **Lección:** La accuracy es una métrica de comodidad, no de valor.

**Nivel:** P — Las métricas son el puente entre estadística y negocio.

**Tiempo sugerido:** 2 minutos (P: 5-6 minutos con las tablas)

---

## 12. LOS DATOS

**Qué decir:**
- "Veamos los datos reales: 75 noches en el Valle del Elqui."
- "El gráfico muestra pronóstico de mínima vs. mínima observada."
- "Casi siempre el modelo acierta. Pero el 18 de julio se equivocó justo cruzando el umbral de daño."
- "Ese punto rojo es el Error Tipo II que costó US$ 53.500."

**Fundamento técnico:**
- **Dataset:** 75 noches de invierno 2025 (julio-agosto).
- **Fuente:** Open-Meteo Historical Weather API (mínima observada) + pronóstico GFS/ECMWF.
- **Variable:** Temperatura mínima del aire a 2m (°C).
- **Umbral de decisión:** 2 °C (pronóstico ≤ 2 °C → activar protección).
- **Umbral de daño:** -0.5 °C (observada ≤ -0.5 °C → helada real).
- **El outlier:** 18 de julio. Pronóstico: +3.4 °C. Observada: -1.6 °C. Error: 5.0 °C.
- **Por qué falló:** El modelo GFS no capturó la inversión térmica nocturna del valle (microclima local).

**Nivel:** S — Los datos hablan por sí solos en el gráfico.

**Tiempo sugerido:** 1.5 minutos

---

## 13. EL CLÍMAX

**Qué decir:**
- "Esta es la noche del 18 de julio. Veamos el flujo paso a paso."
- **Paso 1:** Pronóstico de mínima: +3.4 °C. Por encima del umbral (2 °C). "No hay riesgo."
- **Paso 2:** Decisión: No proteger. Sector D quedó sin aspersión. En plena floración.
- **Paso 3:** Lo que ocurrió: -1.6 °C. Muy por debajo del umbral de daño (-0.5 °C). Heló sobre la flor.
- "El error del modelo fue de 5.0 °C. Cayó justo donde más importaba."
- "Nadie fue negligente. El dato dijo 'seguro', y actuar sobre el dato fue lo sensato."

**Fundamento técnico:**

**Cadena de causa-efecto (análisis de raíz):**

1. **Inversión térmica (frost pool):**
   - **Mecanismo:** En noches claras y sin viento, el suelo pierde calor por radiación infrarroja. El aire en contacto con el suelo se enfría más rápido que el aire superior. En un valle, este aire frío (denso) se acumula en el fondo creando un "lago de aire frío" (frost pool).
   - **Profundidad típica:** 5-15 metros sobre el suelo.
   - **Velocidad de enfriamiento:** 1-3 °C/hora en condiciones ideales (cielo despejado, viento < 5 km/h).
   - **El problema del modelo GFS:** Resuelve a 10km de grilla. No captura microclimas de valles estrechos (< 1km).

2. **Error del pronóstico: +3.4 °C vs. -1.6 °C:**
   - **El modelo GFS** predijo la temperatura "promedio" de la grilla de 10km.
   - **La realidad** del sector D (fondo del valle) fue 5°C más fría por la inversión térmica.
   - **¿Por qué no se detectó?** Los modelos de downscaling estadístico usan regresión lineal con elevación. Pero la inversión térmica no es lineal con la elevación — es un fenómeno no lineal que depende de la geometría del valle, la cobertura del suelo y las condiciones del cielo.

3. **Decisión racional:**
   - Con pronóstico de +3.4 °C y umbral de 2 °C, la decisión óptima según el modelo es "no proteger".
   - **Teorema de Bayes:** Si el modelo dice P(helada) = 0.05 (bajo), y el costo de proteger > costo de no proteger × 0.05, entonces no proteger es la decisión racional.
   - El error no fue de negligencia humana, sino de **incertidumbre del modelo** no cuantificada.

4. **Realidad: -1.6 °C:**
   - La inversión térmica enfrió el sector D 5°C por debajo del pronóstico.
   - A -1.6 °C, el agua intracelular de la flor de fresa se congela.
   - **Mecanismo de daño:** El hielo rompe las paredes celulares (cristales de hielo intracelulares). La flor muere en 24-48 horas. No hay recuperación.

5. **Consecuencia:**
   - Pérdida total del sector D: US$ 53,500.
   - **Lección:** El modelo no estaba "equivocado" — estaba resolviendo la pregunta incorrecta. Predijo la temperatura promedio, no la del microclima específico.

**Posibles mejoras (para preguntas del público):**
- **Sensor de humedad relativa:** La inversión térmica es más fuerte cuando HR > 80% y viento < 5 km/h. Un sensor simple podría activar "modo conservador".
- **Modelo de frost pool:** Usar datos de elevación (DEM) + modelo de radiación para estimar la inversión térmica local.
- **Ensemble local:** Correr el modelo con múltiples condiciones iniciales locales (temperatura del suelo, humedad, viento) para capturar la incertidumbre del microclima.

**Nivel:** P — Es el momento de explicar POR QUÉ falló, no solo QUE falló.

**Tiempo sugerido:** 2 minutos (P: 5-7 minutos con el análisis de causa raíz)

---

## 14. EL COSTO

**Qué decir:**
- "La cuenta del negocio es clara."
- **Pérdida crítica (Amenaza no detectada):** US$ 53.500 — un solo error Tipo II.
- **Costo acumulado (Falsas alarmas):** US$ 650 — todas las noches de la temporada.
- "Un solo error costó 82 veces más que todo lo 'desperdiciado' en falsas alarmas."
- "La exactitud del 96% escondía esta asimetría brutal."

**Fundamento técnico:**

**Análisis de sensibilidad (varying the threshold):**

| Umbral (°C) | FP noches | FN noches | Costo FP | Costo FN | Pérdida total |
|---|---|---|---|---|---|
| 0 | 0 | 3 | $0 | $160,500 | $160,500 |
| 1 | 2 | 2 | $1,300 | $107,000 | $108,300 |
| 2 (actual) | 5 | 1 | $3,250 | $53,500 | $56,750 |
| 3 | 8 | 0 | $5,200 | $0 | $5,200 |
| 3.5 | 10 | 0 | $6,500 | $0 | $6,500 |
| 4 | 12 | 0 | $7,800 | $0 | $7,800 |

**Punto de inflexión:**
- El umbral donde el costo de FP acumulado iguala el costo esperado de FN.
- **Fórmula:** `n_FP(U) × C(FP) = n_FN(U) × C(FN)`
- En nuestro caso: `n_FP(U) × 650 = n_FN(U) × 53,500`
- Simplificando: `n_FP(U) = 82.3 × n_FN(U)`
- El umbral óptimo es donde esta igualdad se satisface.

**Análisis de riesgo (Value at Risk):**
- **VaR 95%:** Con el umbral actual (2°C), hay 5% de probabilidad de perder más de US$ 53,500 en una noche.
- **CVaR 95% (Expected Shortfall):** El promedio de las pérdidas en el peor 5% de escenarios.
- **En nuestro caso:** CVaR = US$ 53,500 (porque solo hay 1 evento peor en 75 noches).

**ROI del umbral conservador (3°C):**
- Inversión adicional: 3 noches × US$ 650 = US$ 1,950
- Ahorro esperado: US$ 53,500 (evitar 1 FN)
- ROI = (53,500 - 1,950) / 1,950 = **26.4×**
- Payback: inmediato (1 noche de ahorro cubre 27 temporadas de FP adicionales).

**Nivel:** P — El análisis de sensibilidad es clave para la decisión.

**Tiempo sugerido:** 1.5 minutos (P: 4-5 minutos con las tablas)

---

## 15. CONTRAMEDIDAS

**Qué decir:**
- "No basta con detectar el error. Hay que diseñar contramedidas."
- **Opción 1 — Modelo conservador:** Ajustar el umbral a 3.5 °C. Evita las pérdidas por completo. Costo extra: US$ 4.420. Ahorro neto: US$ 52.420.
- **Opción 2 — Alerta de verificación:** Si el pronóstico está entre 2 °C y 3.5 °C, verificar manualmente. Costo mínimo.
- **Opción 3 — Monitoreo en tiempo real:** Sensores en campo que activen aspersión automática.
- "La pregunta no es 'por qué falló' sino '¿qué hubiera evitado la pérdida?'"

**Fundamento técnico:**

**Opción 1 — Umbral conservador (3.5 °C):**
- FP esperados: ~10 noches × US$ 650 = US$ 6,500
- FN esperados: 0
- Pérdida esperada: US$ 6,500
- Ahorro vs. actual: US$ 56,750 - US$ 6,500 = **US$ 50,250**
- **Costo de protección por noche extra:** 5 noches × US$ 650 = US$ 3,250
- **Costo total de la "prima de seguro":** US$ 6,500 por temporada
- **ROI:** 50,250 / 6,500 = **7.7×**

**Opción 2 — Zona de verificación (2-3.5 °C):**
- Cuando el pronóstico cae en esta zona, activar sensores portátiles o verificar manualmente.
- Costo: ~US$ 50/noche × ~10 noches = US$ 500
- Ventana de riesgo reducida de 5 °C a 1.5 °C.
- **Análisis bayesiano:** La verificación manual reduce la incertidumbre del pronóstico. Si el sensor portátil dice "3.2 °C" con error ±0.5 °C, la probabilidad de helada baja significativamente.

**Opción 3 — IoT + aspersión automática:**
- **Arquitectura:**
  ```
  Sensores (Davis, Onset) → Gateway (LoRa/WiFi) → Edge computing → API → Actuador de aspersión
  ```
- **Costos:**
  - Hardware: ~US$ 5,000 (sensores + gateway + actuadores)
  - Mantenimiento: ~US$ 500/año
  - Electricidad: ~US$ 200/año
- **Beneficios:**
  - Eliminación del factor humano (error de decisión)
  - Reducción del tiempo de respuesta (minutos vs. horas)
  - Datos para recalibración continua del modelo
- **Riesgos:**
  - Falla de sensores (calibración, batería)
  - Falla de red (LoRa tiene alcance limitado)
  - Falla de actuador (válvulas, presión de agua)

**Opción 4 (emergente) — Modelo de frost pool:**
- Usar datos de elevación (DEM de 30m) + modelo de radiación nocturna para predecir la inversión térmica.
- **Fórmula simplificada:**
  ```
  T_local = T_promedio - ΔT_inversión × f(elevación, exposición, cobertura)
  ```
  donde f() es una función calibrada con datos históricos.
- **Ventaja:** Captura el microclima sin depender de sensores en cada punto.
- **Desventaja:** Requiere calibración local y datos de alta resolución.

**Nivel:** P — Las opciones son el corazón de la propuesta de valor.

**Tiempo sugerido:** 2 minutos (P: 5-6 minutos con el análisis completo)

---

## 16. ACCIÓN

**Qué decir:**
- "Volviendo al storytelling: ¿cómo estructuramos esta historia para que el gerente actúe?"
- "El modelo de Nussbaumer Knaflic nos da el marco: gancho → tensión → resolución."
- "El gancho es el 96% de exactitud. La tensión es el Error Tipo II. La resolución es la contramedida."
- "La historia completa lleva a una decisión: invertir en umbral conservador."

**Fundamento técnico:**
- **Estructura narrativa (3 actos):**
  1. **Acto I — Gancho:** "Tenemos un modelo con 96% de accuracy." (Establece credibilidad)
  2. **Acto II — Tensión:** "Pero el 4% que falla costó US$ 53.500 en una sola noche." (Crea urgencia)
  3. **Acto III — Resolución:** "Subir el umbral a 3.5 °C ahorra US$ 50,250 con costo mínimo." (Propone acción)
- **Principio de storytelling con datos:**
  - Empezar con lo que la audiencia necesita saber, no con lo que tú quieres decir.
  - Usar el "so what?" test: cada diapositiva debe pasar la prueba de "¿y qué?".
  - Terminar con una acción clara y específica.

**Nivel:** S — El storytelling es el mensaje, no la técnica.

**Tiempo sugerido:** 1.5 minutos

---

## 17. OPTIMIZACIÓN

**Qué decir:**
- "Una vez que tenemos la contramedida, ¿cómo la calibramos?"
- "La matriz de costo-beneficio nos permite optimizar: ¿cuánto gastar en prevención vs. cuánto arriesgar en pérdida?"
- "No es solo un problema agrícola. Es un problema de optimización bajo incertidumbre."
- "La calibración continua es clave: el mundo cambia, los costos cambian, el modelo debe adaptarse."

**Fundamento técnico:**

**Optimización bayesiana (sequential decision making):**

**Modelo probabilístico:**
- Sea `T_obs` la temperatura observada y `T_pred` la temperatura pronosticada.
- **Prior:** `P(helada) = P(T_obs ≤ -0.5°C)` basado en datos históricos.
  - En nuestro caso: 6 heladas / 75 noches = **0.08 (8%)**.
- **Likelihood:** `P(T_pred | T_obs)` — el modelo de pronóstico.
  - Distribución típica: `T_pred ~ N(T_obs + μ_error, σ_error)`
  - En nuestro caso: μ_error = 0.5°C, σ_error = 2.5°C.
- **Posterior:** `P(T_obs ≤ -0.5°C | T_pred)` — la probabilidad de helada dado el pronóstico.
  - **Regla de Bayes:**
    ```
    P(helada | T_pred) = P(T_pred | helada) × P(helada) / P(T_pred)
    ```

**Decisión bajo incertidumbre:**
- No conocemos la temperatura real mañana. Solo tenemos un intervalo de confianza.
- **Teoría de decisiones (Raiffa & Schlaifer, 1961):**
  - **Alternativas:** {Proteger, No proteger}
  - **Estados de naturaleza:** {Helada, No helada}
  - **Utilidad:** U(Proteger, Helada) = -650, U(Proteger, No helada) = -650, U(No proteger, Helada) = -53,500, U(No proteger, No helada) = 0
  - **Umbral de Bayes:** Proteger si `P(helada | T_pred) > C(FP) / (C(FP) + C(FN))`
  - En nuestro caso: Umbral = 650 / (650 + 53,500) = **0.012 (1.2%)**
  - Si P(helada | pronóstico) > 1.2%, proteger.

**Regla de Bayes aplicada:**
- **Umbral óptimo:**
  ```
  Umb* = argmin_U [ C(FP) × P(FP|U) + C(FN) × P(FN|U) ]
  ```
- **En la práctica:**
  1. Calcular P(helada | T_pred) para cada T_pred usando el histórico.
  2. Proteger si P(helada | T_pred) > 0.012.
  3. El umbral resultante es ~3.5°C (no 2°C).

**Calibración continua:**
- **Monitoreo de la tasa de error:**
  ```
  Error_rate(t) = (FP(t) + FN(t)) / n(t)
  ```
  - Si `Error_rate(t) > Error_rate(t-1) × (1 + τ)`, hay drift.
  - τ = umbral de tolerancia (típicamente 0.1 = 10% de deterioro).

- **Recalibración bayesiana:**
  1. Actualizar el prior P(helada) con los datos nuevos.
  2. Recalcular el umbral óptimo.
  3. Si los costos cambiaron (ej: precio de fresa subió), recalcular también.

- **Mecanismo de actualización (online learning):**
  ```
  P_nuevo(helada) = α × P_historico(helada) + (1-α) × P_observado(helada)
  ```
  donde α ∈ [0,1] controla la velocidad de aprendizaje (típicamente 0.9 = lento, 0.5 = rápido).

**Optimización multi-objetivo:**
- En la práctica, hay múltiples objetivos en conflicto:
  1. Minimizar pérdida esperada (costo)
  2. Minimizar número de noches protegidas (operación)
  3. Minimizar riesgo de evento catastrófico (VaR)
- **Frente de Pareto:** Conjunto de soluciones donde no se puede mejorar un objetivo sin empeorar otro.
- **Decisión:** Elegir un punto del frente según la aversión al riesgo del tomador de decisiones.

**Nivel:** P — Para audiencia técnica o académica.

**Tiempo sugerido:** 1.5 minutos (P: 6-8 minutos con la teoría completa)

---

## 18. UNIVERSALIDAD

**Qué decir:**
- "Este problema no es exclusivo de la agricultura."
- **Ingeniería de software:** Un bug en producción vs. una falsa alarma en monitoreo.
- **Medicina:** Un diagnóstico falso positivo vs. un cáncer no detectado.
- **Finanzas:** Una transacción legítima bloqueada vs. un fraude no detectado.
- "En todos los casos, el Error Tipo II (amenaza no detectada) es más costoso que el Tipo I."
- "La clasificación binaria asimétrica es un patrón universal."

**Fundamento técnico:**
- **Patrón universal de asimetría de costos:**
  | Dominio | FP (Falsa alarma) | FN (Amenaza no detectada) | Ratio FN/FP |
  |---|---|---|---|
  | Agricultura | US$ 650 | US$ 53.500 | 82× |
  | Medicina | US$ 500 (prueba extra) | US$ 500.000 (cáncer avanzado) | 1000× |
  | Ciberseguridad | US$ 1.000 (investigación) | US$ 100.000 (brecha) | 100× |
  | Finanzas | US$ 50 (bloqueo) | US$ 50.000 (fraude) | 1000× |
- **En todos los casos:** El umbral óptimo NO es el que maximiza accuracy, sino el que minimiza la pérdida esperada.
- **Conexión con teoría de decisiones:** Es el mismo marco de Von Neumann-Morgenstern: maximizar utilidad esperada, no probabilidad de acierto.

**Nivel:** S — Mostrar la tabla, dejar que el público saque sus conclusiones.

**Tiempo sugerido:** 2 minutos

---

## 19. CIERRE

**Qué decir:**
- "Resumen: la exactitud no lo es todo. El 96% de exactitud escondía un error que costó US$ 53.500."
- "El storytelling no es un adorno. Es la herramienta que permite tomar decisiones con datos."
- "La próxima vez que les presenten un modelo con 'alta exactitud', pregunten: ¿qué tipo de error está escondiendo?"
- "Gracias."

**Fundamento técnico:**
- **Mensaje clave (el que deben recordar):**
  - Accuracy ≠ Valor
  - El error que importa es el que tiene el costo más alto
  - El storytelling convierte métricas en decisiones
- **Call to action:** "Cuando les presenten un modelo, pregunten: ¿cuál es la matriz de costos? ¿Qué umbral están usando? ¿Cómo se calibra?"

**Nivel:** S — Cerrar con impacto, no con técnica.

**Tiempo sugerido:** 1 minuto

---

## 20. AGRADECIMIENTOS

**Qué decir:**
- "Si quieren contactarme, estos son mis datos."
- "El código de esta presentación está en GitHub. Es open source."
- "Si tienen preguntas, ahora es el momento."

**Fundamento técnico:** Ninguno — es cierre social.

**Tiempo sugerido:** 30 segundos

---

# Preguntas del público (mínimo 12)

### 1. ¿Por qué no usar simplemente un modelo con mejor accuracy?
**Respuesta:** Porque el problema no es la exactitud, sino la asimetría de costos. Un modelo con 99% de accuracy puede seguir fallando en los casos más caros si los datos están desbalanceados. Lo que importa es minimizar el Error Tipo II, no maximizar la accuracy.
**Fundamento:** La accuracy es `P(acuerdo)`. En datos desbalanceados (91% negativos), un clasificador trivial que siempre prediga "negativo" obtiene 91% de accuracy. La métrica correcta es la **pérdida esperada**: `L = C(FP)×P(FP) + C(FN)×P(FN)`.

### 2. ¿Cuánto costó implementar el sistema de monitoreo con Open-Meteo?
**Respuesta:** La API de Open-Meteo es gratuita para uso académico y de investigación. El costo real está en la infraestructura de monitoreo en campo (sensores, aspersión) que es independiente del modelo predictivo.
**Fundamento:** Open-Meteo usa modelos numéricos de pronóstico (GFS, ECMWF) con resolución hasta 1km vía downscaling estadístico. Es open source y no tiene costo para volúmenes razonables.

### 3. ¿El modelo se podría aplicar a otros cultivos besides fresas?
**Respuesta:** Sí. El marco es general: cualquier cultivo sensible a heladas (uva, caqui, palto) puede usar el mismo enfoque. Lo que cambia es el umbral de daño y los costos por hectárea.
**Fundamento:** El marco de optimización bajo incertidumbre es agnóstico al cultivo. Solo necesitas: (1) umbral de daño, (2) costos de FP/FN, y (3) un modelo predictivo de temperatura.

### 4. ¿Qué pasa si el pronóstico es correcto pero la temperatura real llega justo al umbral (-0.5 °C)?
**Respuesta:** Es el caso más delicado. El modelo predice exactamente el umbral. Aquí la decisión depende del costo relativo: si proteger es barato y no proteger es caro, la decisión óptima es proteger siempre que esté cerca del umbral. Es el principio "cuando dudes, protege".
**Fundamento:** Matemáticamente, el umbral óptimo se desplaza hacia el lado del error más costoso. Si `C(FN) >> C(FP)`, el umbral se mueve a la derecha (más conservador). En el límite, si `C(FN) → ∞`, el umbral se mueve a `+∞` (siempre proteger).

### 5. ¿No se podría usar un modelo de machine learning en vez de una regla simple?
**Respuesta:** Se podría, pero el caso demuestra que una regla simple (umbral de temperatura) puede ser suficiente si se acompaña de una estrategia de decisiones adecuada. El ML agrega complejidad sin necesariamente reducir el Error Tipo II en este contexto.
**Fundamento:** El problema no es la complejidad del modelo predictivo, sino la **regla de decisión** que se aplica sobre su salida. Un XGBoost que predice temperatura tiene el mismo trade-off FP/FN que una regla simple. La diferencia está en la calibración, no en la arquitectura.

### 6. ¿Cómo se maneja la incertidumbre del pronóstico a 24-48 horas?
**Respuesta:** Open-Meteo provee intervalos de confianza. El modelo actual usa el punto más probable, pero se podría extender para usar el percentil 10 (escenario pesimista) como umbral de decisión. Eso haría el sistema más conservador.
**Fundamento:** Los modelos numéricos proveen **ensemble forecasts** (múltiples corridas con condiciones iniciales perturbadas). La dispersión del ensemble es una medida de incertidumbre. Usar el percentil 10 del ensemble es equivalente a un umbral conservador bayesiano.

### 7. ¿Qué rol juega el cambio climático en todo esto?
**Respuesta:** El cambio climático aumenta la frecuencia de eventos extremos y hace que los patrones históricos sean menos confiables. Refuerza la necesidad de monitoreo en tiempo real y de modelos que se adapten, no de reglas estáticas basadas en promedios históricos.
**Fundamento:** El cambio climático afecta la distribución de temperaturas: colas más pesadas (eventos extremos más frecuentes) y mayor varianza. Esto hace que los umbrales estáticos basados en datos históricos pierdan calibración. Los modelos bayesianos con actualización continua son más robustos.

### 8. ¿El costo de US$ 53.500 es por hectárea o por toda la propiedad?
**Respuesta:** Es una estimación para el sector D completo. El costo por hectárea depende del cultivo, la etapa fenológica y el mercado. En fresa en floración, una helada puede significar pérdida del 100% de la producción de esa zona.
**Fundamento:** El costo se calcula como: `Rendimiento (kg/ha) × Precio (USD/kg) × Hectáreas × % Pérdida`. En fresa en floración, la pérdida es del 100% porque la flor muere y no produce fruta.

### 9. ¿Cómo se compara este enfoque con los sistemas de alerta temprana que ya existen?
**Respuesta:** Los sistemas existentes suelen dar una alerta genérica ("riesgo de helada"). Este enfoque va un paso más allá: quantifica el costo de cada decisión y optimiza el umbral. No es solo "¿hay riesgo?" sino "¿cuánto cuesta actuar vs. no actuar?".
**Fundamento:** Los sistemas tradicionales usan **reglas binarias** (umbral fijo). Este enfoque usa **optimización de decisión** (umbral dinámico basado en costos). Es la diferencia entre un semáforo y un GPS: uno te dice "pare", el otro te dice "cuánto cuesta llegar por cada ruta".

### 10. ¿Se podría automatizar la decisión de protección con aspersión?
**Respuesta:** Sí, y esa es la dirección natural. Un sistema que combine pronóstico + sensores en campo + activación automática de aspersión eliminaría el factor humano. Pero requiere inversión en infraestructura IoT y protocolos de seguridad.
**Fundamento:** Arquitectura típica: `Open-Meteo API → Gateway (LoRa/WiFi) → Sensores de temperatura → Edge computing → Actuador de aspersión`. El reto no es la automatización, sino la **robustez**: el sistema debe funcionar sin internet, sin electricidad, y con sensores fallando.

### 11. ¿Qué pasa si el modelo falla múltiples noches seguidas?
**Respuesta:** Es un escenario de "model drift". Si el modelo falla repetidamente, hay que recalibrarlo o cambiar la estrategia. El sistema actual monitorea la tasa de error acumulada y alerta si supera un umbral.
**Fundamento:** **Model drift** = la distribución de los datos cambia con el tiempo (cambio climático, urbanización, cambio de cultivo). Se detecta monitoreando la tasa de error rolling: si `Error_rate(t) > Error_rate(t-1) × (1 + τ)`, hay drift. Solución: recalibrar el modelo o actualizar los costos.

### 12. ¿Cómo se presenta esto a un gerente que solo quiere ver la factura de electricidad?
**Respuesta:** Con storytelling. En vez de mostrar métricas técnicas, se muestra la comparación: "Invertimos US$ 4.420 en prevención y ahorramos US$ 52.420 en pérdidas." El gerente entiende ROI, no F1-score.
**Fundamento:** **ROI de datos:** `(Ahorro - Inversión) / Inversión`. En nuestro caso: `(53,500 - 4,420) / 4,420 = 11.1×`. Un ROI de 11:1 se vende solo. El truco es no presentar la técnica, sino el resultado económico.

---

**Tiempo total estimado:** 25-30 minutos (P: 45-60 minutos con toda la teoría) + 15-20 minutos de preguntas.

**Nota para el presentador:** Los niveles (P/S) son guías, no reglas. Si la audiencia pregunta, profundiza. Si están aburridos, acelera. El storytelling importa más que la técnica.
