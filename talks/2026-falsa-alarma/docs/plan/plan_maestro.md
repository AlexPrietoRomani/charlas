# Plan Maestro — Data_Wizard

> Presentación web interactiva sobre Storytelling en Data Science, usando el caso de la helada en fresa del Valle del Elqui.

---

## 1. Convenciones y Nomenclatura

- **Idioma:** español (es)
- **Identificadores:** `F{n}` (Fase), `SF{f}.{n}` (Sub fase), `T{f}.{sf}.{n}` (Tarea)
- **Arquitectura:** estática (Astro SSG → HTML), sin backend, sin BD relacional
- **Datos:** CSV parseados en navegador; cálculos en vivo via JS nativo
- **Color canónico:** cian `#67E8F9` (datos), ámbar `#FBBF24` (FP), rojo `#FB4A5A` (FN), verde `#34D399` (acierto)

---

## 2. Stack Tecnológico Definitivo

| Capa | Tecnología | Versión | Justificación |
|---|---|---|---|
| Build | Astro | 7.1.3 | SSG rápido, output estático para GitHub Pages |
| Presentación | HTML + CSS + JS | nativo | Sin framework de slides; control total del layout |
| Gráficos | Chart.js | 4.4.1 (CDN) | Timeline y barras; API declarativa |
| Mapa | Leaflet | 1.9.4 (CDN) + OSM tiles | Mapa interactivo con marcador |
| CSV parser | PapaParse | 5.4.1 (CDN) | Parseo robusto en navegador |
| Tipografía | Google Fonts | CDN | Space Grotesk + IBM Plex Sans + IBM Plex Mono |
| Despliegue | GitHub Pages | — | Gratis, estático, sin configuración |
| Desarrollo | pnpm + astro dev | — | Hot reload en localhost:4321 |

---

## 3. Estructura Objetivo del Repositorio

```
Data_Wizard/
├── docs/
│   ├── description_proyecto.md
│   ├── architecture/
│   │   └── architecture.md
│   ├── db/
│   │   └── diseno_db.md
│   ├── plan/
│   │   └── plan_maestro.md
│   ├── task/
│   │   └── tareas.md
│   └── logs/
│       └── log.md
├── src/
│   ├── pages/
│   │   └── index.astro          # 19 slides
│   ├── layouts/
│   │   └── Layout.astro         # HTML shell + CDN
│   ├── components/
│   │   └── Welcome.astro
│   └── assets/
│       ├── astro.svg
│       └── background.svg
├── public/
│   ├── data/
│   │   ├── clima_valle_elqui.csv
│   │   └── rendimiento_fresa.csv
│   └── assets/
│       ├── strawberry_field_sprinklers_night.png
│       └── strawberry_flower_frost_damage.png
├── data/
│   ├── clima_valle_elqui.csv
│   └── rendimiento_fresa.csv
├── assets/
│   ├── strawberry_field_sprinklers_night.png
│   └── strawberry_flower_frost_damage.png
├── reference/
│   ├── Brief.md
│   └── estructura_presentacion.md
├── articles/
│   ├── Storytelling-with-Data.md
│   └── Storytelling-with-Data.pdf
├── presentacion.html             # Versión standalone original
├── astro.config.mjs
├── package.json
├── tsconfig.json
├── .gitignore
├── AGENTS.md
└── README.md
```

---

## 4. Datos de Referencia (Golden Data)

| Dato | Valor esperado | Fuente |
|---|---|---|
| Total de noches | 75 | `clima_valle_elqui.csv` (1-jun a 14-ago 2025) |
| Night más fría | ~18-jul-2025 | `obtener_clima.py` (inyección) |
| TP (umbral 2.0°C) | 6 | Calculado desde CSV |
| FP (umbral 2.0°C) | 2 | Calculado desde CSV |
| FN (umbral 2.0°C) | 1 | Calculado desde CSV (la catástrofe) |
| TN (umbral 2.0°C) | 66 | Calculado desde CSV |
| Exactitud | 96% (72/75) | Calculado |
| Modelo tonto | 91% (68/75) | Calculado |
| Pérdida Sector D | US$ 56.160 | `rendimiento_fresa.csv` |
| Ratio FP vs FN | ~83× | Calculado |

---

## 5. Estrategia de Base de Datos

No aplica. Los datos viven en 2 archivos CSV parseados en el navegador. Ver `docs/db/diseno_db.md` para el esquema completo.

---

## 6. Fases de Ejecución

### Fase 1 — Setup del proyecto ✓

**Objetivo:** Inicializar el proyecto Astro con dependencias y configuración básica.

| Sub fase | Tarea | Estado |
|---|---|---|
| SF1.1 Setup inicial | T1.1.1 `pnpm create astro@latest` + config | [X] |
| | T1.1.2 Configurar `astro.config.mjs` (output: static, inlineStylesheets: always) | [X] |
| | T1.1.3 Configurar `tsconfig.json` | [X] |
| SF1.2 Estructura de assets | T1.2.1 Copiar CSVs a `data/` y `public/data/` | [X] |
| | T1.2.2 Copiar imágenes a `public/assets/` | [X] |
| | T1.2.3 Copiar artículos y referencias | [X] |

### Fase 2 — Layout y estilos globales ✓

**Objetivo:** HTML shell con CDN, tipografía, tema oscuro y estilos de slides.

| Sub fase | Tarea | Estado |
|---|---|---|
| SF2.1 Layout base | T2.1.1 Escribir `Layout.astro` con CDN (PapaParse, Chart.js, Leaflet, Google Fonts) | [X] |
| | T2.1.2 Definir variables CSS (colores canónicos, tipografía, espaciado) | [X] |
| SF2.2 Navegación | T2.2.1 Implementar navegación por teclado (flechas, espacio, F) | [X] |
| | T2.2.2 Barra de progreso + indicador de slide | [X] |

### Fase 3 — Slides 1-7 (Apertura → Slider) ✓

**Objetivo:** Construir las primeras 7 diapositivas del arco narrativo.

| Sub fase | Tarea | Estado |
|---|---|---|
| SF3.1 Apertura | T3.1.1 Slide 1: Título + subtítulo | [X] |
| | T3.1.2 Slide 2: Mapa Leaflet del Elqui | [X] |
| | T3.1.3 Slide 3: "Son las 2 de la madrugada" | [X] |
| SF3.2 Conceptos | T3.2.1 Slide 4: Falsa alarma vs. amenaza no detectada (2 tarjetas) | [X] |
| | T3.2.2 Slide 5: Matriz 2×2 vacía con nombres cotidianos | [X] |
| | T3.2.3 Slide 6: Misma matriz con costos | [X] |
| SF3.3 Interactividad | T3.3.1 Slide 7: Slider de umbral con recálculo en vivo | [X] |

### Fase 4 — Slides 8-12 (La trampa → La decisión) ✓

**Objetivo:** Construir el clímax narrativo con datos reales.

| Sub fase | Tarea | Estado |
|---|---|---|
| SF4.1 La trampa | T4.1.1 Slide 8: 96% gigante + cuadrícula de 75 puntos (1 rojo) | [X] |
| | T4.1.2 Slide 9: Timeline pronóstico vs. observado (Chart.js) | [X] |
| SF4.2 El clímax | T4.2.1 Slide 10: 18 de julio (+3.4 → −1.6) | [X] |
| | T4.2.2 Slide 11: Gráfico por sector + contador US$ 56.160 | [X] |
| SF4.3 Síntesis | T4.3.1 Slide 12: Matriz llena con números y precios | [X] |

### Fase 5 — Slides 13-19 (Universalidad → Cierre) ✓

**Objetivo:** Universalizar el concepto y cerrar con frase accionable.

| Sub fase | Tarea | Estado |
|---|---|---|
| SF5.1 Universalidad | T5.1.1 Slide 13: Test médico, spam, fraude | [X] |
| SF5.2 Cierre | T5.2.1 Slide 14: "Elegir con qué error puedes vivir" + frase | [X] |
| SF5.3 Extras | T5.3.1 Slides 15-19: storytelling, countermeasures, conexión | [X] |

### Fase 6 — Narrativa y storytelling ✓

**Objetivo:** Integrar los principios de Made to Stick / SUCCESs en la presentación.

| Sub fase | Tarea | Estado |
|---|---|---|
| SF6.1 Teoría | T6.1.1 Agregar diapositiva de storytelling (Made to Stick) | [X] |
| | T6.1.2 Agregar diapositiva de contramedidas para errores de modelo | [X] |
| | T6.1.3 Conectar storytelling → predicción | [X] |

### Fase 7 — Power BI styling ✓

**Objetivo:** Aplicar estilo Power BI con sidebar y KPI bar.

| Sub fase | Tarea | Estado |
|---|---|---|
| SF7.1 Sidebar | T7.1.1 Sidebar de navegación por secciones | [X] |
| SF7.2 KPI bar | T7.2.1 Barra de métricas en vivo | [X] |

### Fase 8 — Quality fixes ✓

**Objetivo:** Corregir issues de layout y superposición.

| Sub fase | Tarea | Estado |
|---|---|---|
| SF8.1 Chart overlap | T8.1.1 Fix: chart-box max-height para evitar superposición | [X] |
| | T8.1.2 Fix: slide padding-bottom para respirar sobre footer | [X] |

### Fase 9 — Git y documentación (EN PROGRESO)

**Objetivo:** Documentación project-suite, git limpio, despliegue.

| Sub fase | Tarea | Estado |
|---|---|---|
| SF9.1 project-suite | T9.1.1 Ejecutar `/init` → docs/ | [/] |
| | T9.1.2 Crear AGENTS.md | [ ] |
| | T9.1.3 Actualizar .gitignore | [ ] |
| SF9.2 Despliegue | T9.2.1 Configurar GitHub Pages | [ ] |
| | T9.2.2 Verificar build en producción | [ ] |

---

## 7. Apéndice A — Definition of Done global

Una Tarea se considera completada solo si:

- [ ] Todos sus AC (criterios de aceptación) están cumplidos
- [ ] Los tests unitarios pasan (si aplica lógica calculable)
- [ ] Los tests de simulación de usuario pasan (slide renderiza, interacciones funcionan)
- [ ] No hay errores en consola del navegador
- [ ] Los colores canónicos se respetan (cian, ámbar, rojo, verde)
- [ ] Los cálculos en vivo son correctos (TP/TN/FP/FN, exactitud, costos)
- [ ] La slide es navegable (teclado + táctil)
- [ ] El responsive funciona en desktop y móvil
