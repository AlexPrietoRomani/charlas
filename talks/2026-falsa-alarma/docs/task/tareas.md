# Tareas — Data_Wizard

> Tablero de ejecución con checkboxes. Cada Tarea se marca `[X]` solo cuando todos sus AC pasan y los tests son verdes.

## Fuentes de contexto obligatorias

- `docs/description_proyecto.md` — qué hace el sistema
- `docs/architecture/architecture.md` — arquitectura y flujos
- `docs/db/diseno_db.md` — esquema de datos
- `docs/plan/plan_maestro.md` — plan maestro
- `docs/logs/log.md` — bitácora de incidentes

## Convenciones de checkboxes

- `[ ]` pendiente
- `[/]` en progreso
- `[X]` completado

---

## Fase 1 — Setup del proyecto [X]

### SF1.1 Setup inicial [X]

#### T1.1.1 Inicializar proyecto Astro [X]

**Objetivo:** Crear el proyecto Astro con configuración básica.

**🧠 Explicación:** Astro genera HTML estático sin SSR; ideal para GitHub Pages. Se usa `pnpm` como package manager.

**💡 Cómo hacerlo:**
```bash
pnpm create astro@latest . -- --template minimal --no-install --no-git
pnpm install
```

**Entregable:** `package.json`, `astro.config.mjs`, `tsconfig.json`

**AC:**
- [X] `pnpm astro dev` arranca sin errores
- [X] `http://localhost:4321` muestra la página default

**Tests:**
- Unitario: `pnpm astro build` completa sin errores
- Simulación: página carga en navegador

---

#### T1.1.2 Configurar astro.config.mjs [X]

**Objetivo:** Output estático, CSS inlined, sin prefetch.

**💡 Cómo hacerlo:**
```js
// astro.config.mjs
import { defineConfig } from 'astro/config';
export default defineConfig({
  output: 'static',
  inlineStylesheets: 'always',
  prefetch: { prefetchAll: false }
});
```

**AC:**
- [X] `output: 'static'`
- [X] `inlineStylesheets: 'always'`

---

#### T1.1.3 Configurar tsconfig.json [X]

**Objetivo:** Extender el template de Astro.

**AC:**
- [X] `extends: 'astro/tsconfigs/strict'`

---

### SF1.2 Estructura de assets [X]

#### T1.2.1 Copiar CSVs [X]

**Objetivo:** Datos disponibles en `data/` (origen) y `public/data/` (servido por Astro).

**AC:**
- [X] `data/clima_valle_elqui.csv` existe (75 filas)
- [X] `data/rendimiento_fresa.csv` existe (6 filas)
- [X] `public/data/` tiene ambos CSVs

---

#### T1.2.2 Copiar imágenes [X]

**AC:**
- [X] `public/assets/strawberry_field_sprinklers_night.png`
- [X] `public/assets/strawberry_flower_frost_damage.png`

---

#### T1.2.3 Copiar artículos y referencias [X]

**AC:**
- [X] `articles/Storytelling-with-Data.md`
- [X] `reference/Brief.md`
- [X] `reference/estructura_presentacion.md`

---

## Fase 2 — Layout y estilos globales [X]

### SF2.1 Layout base [X]

#### T2.1.1 Layout.astro con CDN [X]

**Objetivo:** HTML shell que carga todas las dependencias externas.

**💡 Cómo hacerlo:**
```astro
---
// src/layouts/Layout.astro
---
<html lang="es">
<head>
  <meta charset="UTF-8">
  <link href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;600;700&family=IBM+Plex+Sans:wght@400;500;600&family=IBM+Plex+Mono:wght@400;500&display=swap" rel="stylesheet">
  <script src="https://cdn.jsdelivr.net/npm/papaparse@5.4.1/papaparse.min.js"></script>
  <script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.1/dist/chart.umd.min.js"></script>
  <link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" />
  <script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
</head>
<body>
  <slot />
</body>
</html>
```

**AC:**
- [X] Google Fonts cargan (Space Grotesk, IBM Plex Sans, IBM Plex Mono)
- [X] PapaParse, Chart.js, Leaflet cargan desde CDN

---

#### T2.1.2 Variables CSS [X]

**Objetivo:** Tema oscuro con colores canónicos.

**AC:**
- [X] Background: `#0B1120`
- [X] Paneles: `#0F1829`
- [X] Cian: `#67E8F9` (datos)
- [X] Ámbar: `#FBBF24` (FP)
- [X] Rojo: `#FB4A5A` (FN)
- [X] Verde: `#34D399` (acierto)

---

### SF2.2 Navegación [X]

#### T2.2.1 Navegación por teclado [X]

**AC:**
- [X] Flechas izquierda/derecha avanzan/retroceden
- [X] Espacio avanza
- [X] F entra en pantalla completa

---

#### T2.2.2 Barra de progreso [X]

**AC:**
- [X] Indicador de slide actual / total
- [X] Barra visual de progreso

---

## Fase 3 — Slides 1-7 [X]

### SF3.1 Apertura [X]

#### T3.1.1 Slide 1: Título [X]

**AC:**
- [X] Título: "Falsa alarma o amenaza real"
- [X] Subtítulo: "el dilema oculto detrás de cada dato"

---

#### T3.1.2 Slide 2: Mapa Leaflet [X]

**AC:**
- [X] Mapa centrado en −30.03, −70.71
- [X] Marcador con popup
- [X] Círculo punteado de 2.5 km
- [X] Requiere internet para tiles

---

#### T3.1.3 Slide 3: "Son las 2 de la madrugada" [X]

**AC:**
- [X] Gancho narrativo
- [X] Contexto: decisión nocturna de proteger o no

---

### SF3.2 Conceptos [X]

#### T3.2.1 Slide 4: Falsa alarma vs. amenaza [X]

**AC:**
- [X] 2 tarjetas: "barato" vs. "caro"
- [X] Sin jerga técnica

---

#### T3.2.2 Slide 5: Matriz 2×2 vacía [X]

**AC:**
- [X] Matriz con nombres cotidianos
- [X] Ancla visual de toda la charla

---

#### T3.2.3 Slide 6: Matriz con costos [X]

**AC:**
- [X] Misma matriz + precio por celda
- [X] Quiebre: la simetría se rompe con dinero

---

### SF3.3 Interactividad [X]

#### T3.3.1 Slide 7: Slider de umbral [X]

**Objetivo:** El error no se elimina, se elige su tipo.

**💡 Cómo hacerlo:**
```javascript
// Recálculo al mover slider
const umbral = parseFloat(slider.value);
const flagged = data.map(d => d.pronostico <= umbral);
const frost = data.map(d => d.observado <= UMBRAL_DANO);
const TP = flagged.filter((f, i) => f && frost[i]).length;
const FP = flagged.filter((f, i) => f && !frost[i]).length;
const FN = flagged.filter((f, i) => !f && frost[i]).length;
const TN = flagged.filter((f, i) => !f && !frost[i]).length;
```

**AC:**
- [X] Slider de −2 a +5 °C, paso 0.5
- [X] Recalcula TP/TN/FP/FN en vivo
- [X] Cambia mensaje según régimen (exigente / equilibrado / nervioso)

**Tests:**
- Unitario: mover slider a 2.0°C produce TP=6, FP=2, FN=1, TN=66
- Simulación: slider responde a input del usuario

---

## Fase 4 — Slides 8-12 [X]

### SF4.1 La trampa [X]

#### T4.1.1 Slide 8: Cuadrícula de 75 puntos [X]

**AC:**
- [X] 75 celdas (una por noche)
- [X] Coloreadas por resultado
- [X] FN con glow rojo

---

#### T4.1.2 Slide 9: Timeline [X]

**Objetivo:** "Miren qué bien pega el modelo…" (la trampa).

**AC:**
- [X] Chart.js line: observado vs. pronóstico
- [X] Líneas de umbrales (2.0°C y −0.5°C)
- [X] Punto rojo en 18-jul

**Tests:**
- Unitario: timeline renderiza con 75 puntos
- Simulación: gráfico visible en slide

---

### SF4.2 El clímax [X]

#### T4.2.1 Slide 10: 18 de julio [X]

**AC:**
- [X] Pronóstico: +3.4 °C ("seguro")
- [X] Observado: −1.6 °C (heló)
- [X] Error de 5.0 °C

---

#### T4.2.2 Slide 11: La cuenta [X]

**AC:**
- [X] Gráfico de barras por sector (Chart.js)
- [X] Sector D en rojo
- [X] Contador animado US$ 56.160
- [X] Ratio 83×

---

### SF4.3 Síntesis [X]

#### T4.3.1 Slide 12: Matriz llena [X]

**AC:**
- [X] Matriz completa con números y precios
- [X] Síntesis: el dial se sesga a propósito hacia FP

---

## Fase 5 — Slides 13-19 [X]

### SF5.1 Universalidad [X]

#### T5.1.1 Slide 13: Patrones universales [X]

**AC:**
- [X] Test médico, spam, fraude
- [X] Universalidad: esto no es de agrónomos

---

### SF5.2 Cierre [X]

#### T5.2.1 Slide 14: Cierre [X]

**AC:**
- [X] "Elegir con qué error puedes vivir"
- [X] Frase para llevar

---

### SF5.3 Extras [X]

#### T5.3.1 Slides 15-19 [X]

**AC:**
- [X] Diapositiva de storytelling (Made to Stick / SUCCESs)
- [X] Diapositiva de contramedidas
- [X] Conexión storytelling → predicción
- [X] Sidebar de navegación
- [X] KPI bar

---

## Fase 9 — Git y documentación [/]

### SF9.1 project-suite [/]

#### T9.1.1 Ejecutar /init [X]

**AC:**
- [X] `docs/description_proyecto.md`
- [X] `docs/architecture/architecture.md`
- [X] `docs/db/diseno_db.md`
- [X] `docs/plan/plan_maestro.md`
- [X] `docs/task/tareas.md`

---

#### T9.1.2 Crear AGENTS.md [ ]

**AC:**
- [ ] `AGENTS.md` con reglas project-suite

---

#### T9.1.3 Actualizar .gitignore [ ]

**AC:**
- [ ] Archivos de trabajo ignorados (`docs/task/`, `docs/plan/`, `docs/logs/`, `AGENTS.md`, `.project-suite/`)
- [ ] Spec compartible versionada (`docs/description_proyecto.md`, `docs/architecture/`, `docs/db/`, `docs/ejecucion.md`)

---

### SF9.2 Despliegue [ ]

#### T9.2.1 Configurar GitHub Pages [ ]

**AC:**
- [ ] Repo con GitHub Pages habilitado
- [ ] Build automático desde `main`/`master`

---

#### T9.2.2 Verificar build [ ]

**AC:**
- [ ] `pnpm astro build` completa sin errores
- [ ] `dist/` contiene HTML estático
- [ ] La URL de GitHub Pages carga correctamente
