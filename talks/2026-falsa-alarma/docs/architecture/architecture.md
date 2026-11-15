# Arquitectura — Data_Wizard

---

## 1. Visión General del Sistema (C4 – Nivel Contexto)

```mermaid
flowchart TB
    subgraph Actores["👥 Actores"]
        PON["👤 Ponente (Alex)"]
        PUBLIC["👥 Público\n(interactúa)"]
        VISIT["🌐 Visitante\n(GitHub Pages)"]
    end

    subgraph Sistema["🖥️ Data_Wizard"]
        APP["Presentación Astro\nHTML estático + JS"]
    end

    subgraph Externas["🌐 Fuentes externas"]
        OSM["OpenStreetMap\ntiles mapa"]
        GFONT["Google Fonts\n tipografías"]
        METEO["Open-Meteo API\n(datos históricos)"]
    end

    PON -->|"navega slides"| APP
    PUBLIC -->|"slider, clicks"| APP
    VISIT -->|"URL"| APP
    METEO -->|"obtener_clima.py"| APP
    APP <-->|"tiles"| OSM
    APP -->|"font files"| GFONT
```

**Decisiones arquitectónicas clave (Nivel Macro):**
- **Motor de presentación:** Astro 7 SSG → genera HTML estático sin runtime server. Se eligió por build rápido, output estático (GitHub Pages compatible) y soporte de Islands architecture.
- **Librerías via CDN:** PapaParse, Chart.js, Leaflet se cargan desde CDN sin bundler. Se descartó npm runtime porque el proyecto es una presentación, no una app — sin build step para JS, sin dependencias de Node en runtime.
- **Datos embebidos como fallback:** CSVs se incluyen en `<script type="text/csv">` para que funcione con `file://`. Se descartó solo fetch porque la presentación debe funcionar sin servidor local.

---

## 2. Componentes Internos (C4 – Nivel Contenedor)

```mermaid
flowchart LR
    subgraph BUILD["⚙️ Build time (Astro)"]
        SSG["Astro SSG\ngenera HTML"]
    end

    subgraph RUNTIME["🖥️ Runtime (navegador)"]
        PARSE["PapaParse\nlee CSV"]
        CALC["JS nativo\ncálculos TP/TN/FP/FN"]
        UI_CHART["Chart.js\ntimeline + barras"]
        UI_MAP["Leaflet\nmapa OSM"]
        UI_SLIDER["Slider JS\numbral interactivo"]
    end

    subgraph DATOS["🗄️ Datos"]
        CSV[("CSVs\nclima + rendimiento")]
    end

    SSG -->|"HTML embebido"| PARSE
    PARSE -->|"75 noches"| CALC
    CALC -->|"datos procesados"| UI_CHART
    CALC -->|"datos procesados"| UI_SLIDER
    CSV -->|"fetch / fallback"| PARSE
```

**Flujo de una interacción típica (runtime):**
1. El navegador carga el HTML estático generado por Astro
2. PapaParse lee los CSV (fetch o fallback embebido)
3. JS nativo clasifica cada noche (flagged vs. frost) con los umbrales
4. Se calculan TP/TN/FP/FN, exactitud, costos y ratio
5. Chart.js renderiza timeline y barras con los datos procesados
6. Al mover el slider → se recalcula todo → se actualizan gráficos y mensajes

---

## 🔄 Flujos de datos — mapa maestro

```mermaid
flowchart LR
    F1["1 · Ingesta climática\nOpen-Meteo → Python → CSV"]
    F2["2 · Datos estáticos\ncreación manual → CSV"]
    F3["3 · Build Astro\nCSVs + slides → HTML"]
    F4["4 · Visualización\nHTML → navegador → cálculos + gráficos"]

    F1 -->|"clima_valle_elqui.csv"| F3
    F2 -->|"rendimiento_fresa.csv"| F3
    F3 -->|"index.html"| F4
```

| # | Flujo | Entrada | Proceso | Salida | Detalle |
|---|---|---|---|---|---|
| **1** | Ingesta climática | Open-Meteo Archive API | `obtener_clima.py`: descarga, agrega error gaussiano σ=1.1°C, inyecta escenario crítico | `clima_valle_elqui.csv` (75 filas) | §3 |
| **2** | Datos estáticos | Cálculo manual del caso | Creación directa del CSV con rendimiento por sector | `rendimiento_fresa.csv` (6 sectores) | §4 |
| **3** | Build Astro | CSVs + componentes .astro | `astro build` → HTML estático con CSVs embebidos | `dist/index.html` + assets | §5 |
| **4** | Visualización | HTML en navegador | PapaParse → JS nativo → Chart.js + Leaflet | Slides interactivas | §6 |

---

## 3. Flujo 1 — Ingesta climática

**Entrada → Proceso → Salida:** Open-Meteo API → Python (obtener_clima.py) → clima_valle_elqui.csv.

Script: `obtener_clima.py`.

### 3.1 Diagrama de ingesta

```mermaid
flowchart TB
    IN(["Open-Meteo Archive API"]):::fuente
    DL["Descarga mínimas\ndiarias 1-jun a 14-ago 2025"]:::proc
    SIM["Simula pronóstico\nmínima observada + N(0, 1.1°C)"]:::proc
    INJ["Inyecta escenario\nfuerza pronóstico > umbral\nen la noche más fría"]:::riesgo
    OUT[("clima_valle_elqui.csv\n75 filas")]:::model

    IN --> DL --> SIM --> INJ --> OUT

    classDef fuente fill:#EAB308,stroke:#A16207,color:#1F2937;
    classDef proc   fill:#3B82F6,stroke:#1D4ED8,color:#FFFFFF;
    classDef model  fill:#22C55E,stroke:#15803D,color:#06310F;
    classDef riesgo fill:#EF4444,stroke:#B91C1C,color:#FFFFFF;
```

### 3.2 Reglas e invariantes

| Regla | Descripción |
|---|---|
| **Idempotencia** | El script genera el CSV completo cada vez; no append ni incrementales |
| **Inyección controlada** | La noche más fría recibe pronóstico forzado; desactivable con `--sin-escenario` |
| **Semilla gaussiana** | σ = 1.1°C imita error realista de modelos meteorológicos |

---

## 4. Flujo 2 — Datos estáticos de sectores

**Entrada → Proceso → Salida:** Cálculo manual del caso → rendimiento_fresa.csv.

### 4.1 Contenido

6 sectores (A–F) con: superficie, fenología al 18-jul, protección, rendimiento esperado/real, daño, pérdida.

Sector D (caso crítico): 1.2 ha, plena floración, NO protegido, 65% daño, US$ 56.160 pérdida.

### 4.2 Reglas

| Regla | Descripción |
|---|---|
| **Datos fijos** | El CSV no se regenera; es parte del caso narrativo |
| **Sector D es el villano** | Siempre sin proteger en la noche crítica; su pérdida es el clímax de la charla |

---

## 5. Flujo 3 — Build Astro

**Entrada → Proceso → Salida:** Componentes .astro + CSVs → `astro build` → HTML estático.

### 5.1 Diagrama

```mermaid
flowchart LR
    IN(["src/pages/index.astro\n+ data/*.csv"]):::fuente
    BUILD["astro build\nSSG"]:::proc
    OUT[("dist/index.html\n+ assets")]:::model

    IN --> BUILD --> OUT

    classDef fuente fill:#EAB308,stroke:#A16207,color:#1F2937;
    classDef proc   fill:#3B82F6,stroke:#1D4ED8,color:#FFFFFF;
    classDef model  fill:#22C55E,stroke:#15803D,color:#06310F;
```

### 5.2 Reglas

| Regla | Descripción |
|---|---|
| **inlineStylesheets: always** | CSS inlined en el HTML; sin requests externos para estilos |
| **Output estático** | No hay SSR ni server; todo se resuelve en build time |
| **CSVs embebidos** | Se incluyen como `<script type="text/csv">` para fallback sin servidor |

---

## 6. Flujo 4 — Visualización (runtime)

**Entrada → Proceso → Salida:** HTML en navegador → PapaParse + JS nativo → gráficos interactivos.

### 6.1 Diagrama

```mermaid
flowchart TB
    IN(["HTML estático"]):::fuente
    PARSE["PapaParse\nparsea CSV"]:::proc
    CLASS["JS: clasifica noches\nflagged = pron ≤ 2.0\nfrost = obs ≤ -0.5"]:::proc
    CALC["JS: calcula\nTP/TN/FP/FN\nexactitud, costos, ratio"]:::proc
    RENDER["Chart.js + Leaflet\nrenderiza gráficos"]:::out
    SLIDER["Slider interactivo\nrecalcula al mover"]:::ui

    IN --> PARSE --> CLASS --> CALC --> RENDER
    CALC --> SLIDER

    classDef fuente fill:#EAB308,stroke:#A16207,color:#1F2937;
    classDef proc   fill:#3B82F6,stroke:#1D4ED8,color:#FFFFFF;
    classDef out    fill:#8B5CF6,stroke:#6D28D9,color:#FFFFFF;
    classDef ui     fill:#64748B,stroke:#334155,color:#FFFFFF;
```

### 6.2 Reglas e invariantes

| Regla | Descripción |
|---|---|
| **Cálculo en vivo** | TP/TN/FP/FN se recalculan en cada movimiento del slider; nada hardcodeado |
| **Sin dependencias de servidor** | Todo corre en el navegador; los CSVs pueden venir de fetch o fallback embebido |
| **Colores canónicos** | cian `#67E8F9` (datos), ámbar `#FBBF24` (FP), rojo `#FB4A5A` (FN), verde `#34D399` (acierto) |

---

## 7. Arquitectura de despliegue

```mermaid
flowchart LR
    subgraph LOCAL["🖥️ Desarrollo"]
        DEV["npx astro dev\nlocalhost:4321"]
        DATA[("data/*.csv\nlocales")]
    end

    subgraph CI["⚙️ GitHub Actions"]
        BUILD["astro build"]
    end

    subgraph PAGES["☁️ GitHub Pages"]
        DIST["dist/\nHTML estático"]
    end

    DEV -.->|"push a master"| CI
    CI -->|"build + deploy"| PAGES
    DATA -->|"commit"| CI

    style LOCAL fill:#1a1a3a,stroke:#8888aa,color:#dddddd
    style PAGES fill:#081a08,stroke:#69db7c,color:#a9e34b
    style CI fill:#091827,stroke:#4dabf7,color:#74c0fc
```

**Notas de despliegue:**
- **Bundle:** HTML estático + assets (CSS inlined, JS de CDN) ~small size
- **Credenciales:** Ninguna; todo es público
- **GitHub Pages:** sirve desde `https://<usuario>.github.io/<repo>/`
- **Restricciones:** OpenStreetMap tiles y Google Fonts requieren internet

---

## 8. Decisiones arquitectónicas (ADRs)

| Decisión Tomada | Alternativa Descartada | Razón Principal |
|---|---|---|
| **Astro 7 SSG** | Next.js, HTML puro, reveal.js | Astro genera HTML estático sin SSR; output ligero para GitHub Pages; Islands architecture permite interactividad sin hydrate completo |
| **CDN para librerías** | npm bundle (Vite, Webpack) | Proyecto es presentación, no app; CDN evita build step para JS; PapaParse/Chart.js/Leaflet son estables y no cambian frecuentemente |
| **Datos embebidos como fallback** | Solo fetch de CSVs | La presentación debe funcionar con `file://` (doble clic en HTML); fallback garantiza que los datos estén siempre disponibles |
| **Cálculo en navegador** | Pre-cálculo en Python/build time | El slider interactivo requiere recálculo en vivo; mover la perilla debe recalcula TP/TN/FP/FN instantáneamente |
| **GitHub Pages** | Vercel, Netlify, hosting propio | Gratis, sin configuración, suficiente para HTML estático; el repo ya existe en GitHub |
