# Brief completo de la ponencia
## "Falsa alarma o amenaza real: el dilema oculto detrás de cada dato"

Documento de traspaso: todo lo necesario para reconstruir, mejorar o portar esta
charla a otra plataforma (OpenCode u otra) sin perder el diseño narrativo ni la
coherencia de los datos.

---

## 1. Qué es esta charla (en una línea)

Una ponencia de ~30 minutos, estrictamente de datos pero para público general,
que enseña **la asimetría entre tipos de error** (falso positivo vs. falso
negativo) a través de una historia agrícola real y visceral: una helada no
detectada en un campo de fresa del Valle del Elqui.

**Tesis central:** decidir con datos no es acertar siempre; es elegir con qué
error puedes vivir. Un modelo que casi siempre acierta puede arruinarte si su
único error cae donde no puedes pagarlo.

**El villano de la charla no es el modelo, es la métrica.** El modelo hizo lo
que todo modelo hace (fallar a veces); el error humano fue medir su calidad con
un número —la exactitud— que trata todos los errores como iguales cuando el
negocio no lo hace.

---

## 2. El caso (escenario semi-simulado)

### Contexto físico
- **Lugar:** campo de fresa de 6,1 ha, Valle del Elqui, Región de Coquimbo,
  Norte Chico de Chile. Coordenadas: **30,03° S · 70,71° O** (~700 m s. n. m.,
  cerca de Vicuña).
- **Por qué hiela ahí:** valle interior encajonado; en noches despejadas de
  invierno el aire frío drena desde los cerros y se estanca en el fondo
  (helada radiativa). Detalle narrativo bonito: el mismo cielo despejado que
  hace famoso al Elqui para la astronomía es el que deja escapar el calor del
  suelo por la noche.
- **La decisión recurrente:** cada noche de invierno, con el pronóstico de
  mínima en mano, decidir si se activa la protección antihelada (aspersión:
  agua, energía, personal) o no.

### Reglas de decisión (constantes del sistema)
| Parámetro | Valor | Significado |
|---|---|---|
| `UMBRAL_ACTIVACION` | **2,0 °C** | Se protege si el pronóstico de mínima ≤ 2 °C |
| `UMBRAL_DANO` | **−0,5 °C** | Hay daño si la mínima observada ≤ −0,5 °C |
| `COSTO_NOCHE` | **US$ 340** | Costo de una noche de protección |
| Precio fruta | **US$ 1,6/kg** | Para valorizar la pérdida |

### Los datos (temporada: 75 noches, 1-jun a 14-ago 2025)
- Fuente real: mínimas diarias de **Open-Meteo** (archive API) para ese punto.
- El **pronóstico es semi-simulado**: mínima observada + error gaussiano
  realista (σ = 1,1 °C) — imita lo que un modelo habría dicho la noche anterior.
- **Inyección del escenario:** en la noche más fría se fuerza el pronóstico por
  encima del umbral de activación → nace la "amenaza no detectada".

### Matriz de confusión resultante (umbral 2,0 °C)
| | Ocurrió helada | No ocurrió |
|---|---|---|
| **Predije riesgo** | TP = 6 (protegí a tiempo) | FP = 2 (falsas alarmas) |
| **Predije seguro** | **FN = 1 (la catástrofe)** | TN = 66 (noches tranquilas) |

### Los números que arman el golpe
- **Exactitud: 96 %** (72/75). Suena excelente.
- Modelo tonto que siempre dice "no habrá helada": **91 %** de exactitud (68/75).
  → la exactitud casi no distingue el modelo real del modelo inútil.
- **La noche crítica: 18 de julio 2025.** Pronóstico **+3,4 °C** ("seguro, no
  protejas") → observado **−1,6 °C** (heló sobre la flor). Error de 5,0 °C.
- **Sector D**: 1,2 ha, en plena floración (fenología más vulnerable), sin
  proteger esa noche → **65 % de daño** → 35.100 kg perdidos →
  **US$ 56.160 de pérdida**.
- Todas las falsas alarmas de la temporada: 2 × US$ 340 = **US$ 680**.
- **Ratio: un solo falso negativo costó ~83× más que todas las falsas alarmas juntas.**

### La sutileza en tres capas (el corazón conceptual)
1. **El promedio esconde.** Error medio de pronóstico ±1 °C: normal. El error
   del 18-jul parece "una noche mala del modelo". Nada salta en un reporte.
2. **No importa cuánto te equivocas, sino dónde.** El error de 5 °C fue grave
   por su *ubicación*: cruzó a la vez el umbral de activación (hacia arriba) y
   el de daño (hacia abajo). El mismo error de 5 °C en una noche de 9 °C
   pronosticados habría costado cero. El costo del error no es función de su
   magnitud sino de dónde cae respecto a los umbrales de decisión.
3. **Las métricas estándar no avisan.** La exactitud premia acertar las noches
   fáciles y castiga igual un error de US$ 340 que uno de US$ 56.160. Con la
   métrica equivocada, el error grave es matemáticamente invisible: el
   dashboard en verde mientras el negocio sangra.

---

## 3. Arco narrativo (14 diapositivas, ~30 min)

Estructura de emboscada deliberada: dejar que el público apruebe el modelo
antes de revelar el desastre.

| # | Sección | Contenido | Función narrativa |
|---|---|---|---|
| 1 | Apertura | Título + subtítulo | Promesa: hay un dilema oculto |
| 2 | El lugar | Mapa real (Leaflet/OSM) del Elqui + por qué hiela | Anclar la historia en un lugar físico y real |
| 3 | El gancho | "Son las 2 de la madrugada" — la decisión nocturna | Tensión humana; el público *es* quien decide |
| 4 | El concepto | Falsa alarma vs. amenaza no detectada (2 tarjetas) | Vocabulario sin jerga; "barato" vs. "caro" |
| 5 | Los 4 desenlaces | Matriz 2×2 vacía, con nombres cotidianos | El ancla visual de toda la charla |
| 6 | Ponle precio | La misma matriz con costos | Quiebre: la simetría se rompe con dinero |
| 7 | El dial | Slider interactivo de umbral con datos reales | El error no se elimina, se elige su tipo |
| 8 | La trampa | 96 % gigante + cuadrícula de 75 puntos (1 rojo) | Anti-clímax: el número bueno esconde al asesino |
| 9 | Los datos | Timeline pronóstico vs. observado + umbrales | "Miren qué bien pega el modelo…" (la trampa) |
| 10 | 18 de julio | +3,4 °C → no proteger → −1,6 °C | El clímax; decisión razonable y equivocada |
| 11 | La cuenta | Gráfico por sector + contador US$ 56.160 + 83× | El costo hecho visceral |
| 12 | La decisión | Matriz llena con números y precios | Síntesis: el dial se sesga a propósito hacia FP |
| 13 | El patrón | Test médico, spam, fraude | Universalidad: esto no es de agrónomos |
| 14 | Cierre | "Elegir con qué error puedes vivir" + frase para llevar | El mensaje que se van repitiendo |

**Frase de cierre:** *"La próxima vez que un dato te dé una respuesta, no
preguntes solo si es correcta. Pregunta cuánto cuesta que se equivoque."*

**Momentos clave de la puesta en escena:**
- En la diapositiva 8-9, pausar y preguntar al público: *"¿buen modelo,
  verdad?"* — dejar que asientan antes de revelar el punto rojo.
- En la 10, subrayar que **nadie fue negligente**: actuar según el dato era lo
  sensato. Eso hace el error sistémico, no personal.
- En la 7 (slider), mover el dial en vivo: exigente → se escapan heladas;
  nervioso → llueven falsas alarmas. No hay punto sin error.

---

## 4. Principios de storytelling aplicados (y por qué le sirven a un Data Scientist, no solo a un Data Analyst)

Estos son los principios de diseño narrativo que esta charla usa deliberadamente.
Sirven igual para presentar cualquier modelo a negocio:

1. **Empieza con una persona y una decisión, no con un dataset.** La charla
   abre a las 2 AM con alguien que debe decidir, no con "tenemos 75 registros
   de temperatura". El dato importa porque hay una decisión colgando de él.
   *Para un DS: todo modelo existe para mover una decisión; preséntalo desde
   la decisión.*

2. **Una sola idea, un solo ancla visual.** Toda la charla es UNA idea (la
   asimetría de errores) y UN gráfico ancla (la matriz 2×2) que aparece vacía,
   luego con precios, luego con datos. La repetición con variación fija el
   concepto. *Para un DS: resiste la tentación de mostrar las 12 métricas;
   elige la vista que carga el mensaje.*

3. **La emboscada (setup → subversión).** Primero dejas que el público apruebe
   el 96 % y el gráfico bonito; luego revelas que ese juicio era la trampa.
   El "aha" es más fuerte cuando el público se equivoca primero en su cabeza.
   *Para un DS: mostrar la métrica agregada y luego romperla es más persuasivo
   que empezar por la crítica.*

4. **Ponle precio, no probabilidad.** "FN = 1" no mueve a nadie; "US$ 56.160,
   83 veces más que todas las falsas alarmas" sí. Convertir errores a unidades
   de negocio (dinero, kilos, horas) es lo que hace que la audiencia no técnica
   *sienta* la asimetría. *Para un DS: la función de pérdida real de tu modelo
   está en la moneda del negocio, no en el log-loss.*

5. **Un villano concreto y visible.** El punto rojo único en la cuadrícula de
   75 puntos. Un solo pixel con nombre y fecha (18 de julio, Sector D) vale más
   que una distribución de errores. *Para un DS: los casos individuales bien
   elegidos comunican lo que los agregados esconden.*

6. **Interactividad = agencia del público.** El slider del umbral deja que la
   audiencia "sienta" el trade-off en sus manos: mover la perilla no elimina el
   error, cambia su tipo. *Para un DS: si puedes dejar que negocio toque el
   umbral, la conversación de precision/recall se vuelve suya.*

7. **Exonerar a las personas, culpar al sistema de medición.** "Nadie fue
   negligente" es clave: el público se defiende si se siente acusado. El
   antagonista es la métrica mal elegida. *Para un DS: al presentar fallos de
   modelo, culpar al proceso de evaluación abre puertas; culpar a usuarios las
   cierra.*

8. **Universalizar al final, no al principio.** Solo después de que la historia
   agrícola caló, se muestra que el patrón es idéntico en medicina, spam y
   fraude. Primero lo concreto, luego la abstracción. *Regla general: historia
   → concepto → generalización, nunca al revés.*

9. **Cierre accionable y repetible.** La última frase es corta, en segunda
   persona y se puede recitar. Si el público sale repitiendo una frase, la
   charla funcionó.

**El punto meta (dilo explícitamente al cerrar si el público es de datos):**
el storytelling no es maquillaje para dashboards de un Data Analyst; es la
diferencia entre un modelo técnicamente correcto que nadie adopta y uno que
cambia decisiones. La matriz de confusión de esta charla es la misma que en
cualquier curso; lo que la hace memorable es la helada, el sector D y los
US$ 56.160.

---

## 5. Especificación técnica de la versión actual (HTML)

Para portar/reconstruir en otra plataforma:

### Archivos y flujo de datos
- `presentacion.html` — deck completo, 14 diapositivas. Lee 2 CSV por `fetch`
  (si se sirve la carpeta) con **respaldo incrustado** en `<script type="text/csv">`
  (si se abre con doble clic, `file://`).
- `clima_valle_elqui.csv` — 75 filas: `fecha, temp_min_obs_c, temp_max_obs_c,
  precipitacion_mm, radiacion_mj_m2, temp_min_pronostico_c`.
- `rendimiento_fresa.csv` — 6 sectores (A–F): `sector, superficie_ha,
  fenologia_18jul, protegido_18jul, rendimiento_esperado_kg,
  rendimiento_real_kg, dano_helada_pct, perdida_usd`. Sector D:
  `1.2, plena floracion, no, 54000, 18900, 65, 56160`.
- `obtener_clima.py` — regenera el CSV de clima con datos reales de Open-Meteo
  (`archive-api.open-meteo.com/v1/archive`), pronóstico semi-simulado
  (σ = 1,1 °C) e inyección de la noche crítica en la noche más fría
  (desactivable con `--sin-escenario`). Args: `--lat --lon --inicio --fin
  --salida`. Nota: Open-Meteo requiere licencia comercial para uso empresarial.

### Cálculo en vivo (nada hardcodeado en la lógica)
La matriz TP/TN/FP/FN, la exactitud, los costos, el ratio 83× y el modelo tonto
(91 %) se calculan en el navegador desde los CSV con las constantes:
`UMBRAL_ACTIVACION = 2.0`, `UMBRAL_DANO = -0.5`, `COSTO_NOCHE = 340`.
Clasificación por noche: `flagged = pronostico <= UMBRAL_ACTIVACION`;
`frost = observado <= UMBRAL_DANO`.

### Componentes interactivos a replicar
1. **Slider de umbral** (−2 a +5 °C, paso 0,5): recalcula los 4 conteos en vivo
   y cambia el mensaje según el régimen (exigente / equilibrado / nervioso).
2. **Cuadrícula de 75 puntos** (una celda por noche, coloreada por resultado;
   el FN con glow rojo).
3. **Timeline** (Chart.js): observado vs. pronóstico + líneas de ambos umbrales
   + punto rojo el 18-jul.
4. **Barras por sector** (esperado vs. real; Sector D en rojo).
5. **Contador animado** de US$ 56.160 al entrar a "La cuenta".
6. **Mapa real** (Leaflet + OpenStreetMap): marcador en −30.03, −70.71, popup
   con la noche crítica, círculo punteado de 2,5 km. Requiere internet.

### Diseño (identidad visual)
- Tema "noche fría": fondo `#0B1120`, paneles `#0F1829`.
- Semáforo de significado: **cian** `#67E8F9` (frío/datos), **ámbar** `#FBBF24`
  (falsa alarma), **rojo** `#FB4A5A` (amenaza no detectada), **verde** `#34D399`
  (acierto). Mantener este mapeo de color en cualquier plataforma: es parte del
  lenguaje de la charla.
- Tipografías: Space Grotesk (títulos), IBM Plex Sans (texto), IBM Plex Mono
  (números/datos, tabular).
- Navegación: flechas/espacio/PageUp-Down, Home/End, `F` pantalla completa,
  swipe táctil. Respeta `prefers-reduced-motion`.

### Librerías (CDN)
PapaParse 5.4.1 (CSV), Chart.js 4.4.1 (gráficos), Leaflet 1.9.4 + tiles OSM
(mapa), Google Fonts. Todo necesita internet la primera vez; los datos no.

---

## 6. Ideas de mejora para la siguiente iteración

- **Diapositiva "el mismo error, dos noches"** (entre timeline y 18-jul): el
  error de 5 °C lado a lado en una noche inofensiva (9 °C → 4 °C, costo cero) y
  en la crítica (+3,4 → −1,6, US$ 56.160). Hace explícita la capa 2.
- Modo presentador con notas por diapositiva (los "beats" de la sección 3).
- Precalcular una captura estática del mapa como fallback sin internet.
- Versión en vivo del slider proyectando también el costo total esperado por
  umbral (curva de costo vs. umbral, con su mínimo en función de los precios).
- Si la plataforma destino soporta escenas/steps dentro de una diapositiva:
  revelar la matriz 2×2 celda por celda (acierto → falsa alarma → amenaza no
  detectada) para controlar el ritmo.