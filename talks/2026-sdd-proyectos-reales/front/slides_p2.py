"""
Archivo: talks/2026-sdd-proyectos-reales/front/slides_p2.py
Fecha de modificación: 17/11/2026
Autor: Alex Prieto <alexprieto1997@gmail.com>

Descripción:
Diapositivas 14 a 27 de la charla `2026-sdd-proyectos-reales` (Bloques 3, 4 y 5)
con estética Bento gerencial, más las especificaciones Chart.js de las dos
gráficas de la sesión. Todas las cifras provienen del laboratorio real
`demos/sdd-churn-leakage/`: 1,203 clientes en `data/churn_events.csv` (seed=42),
AUC 0.9593 con fuga vs AUC 0.8318 honesto (split temporal), brecha 0.1275.

Acciones Principales:
    - Define `SLIDES_P2`: lista ordenada de diapositivas en formato de datos.
    - Incluye el diagrama animado Elefante vs Goldfish, la comparativa animada
      AUC 0.9593 -> 0.8318 y las láminas `EJERCICIO EN VIVO · IR AL TERMINAL`
      de las prácticas 2 y 3 (Bloque 4, partes A y B).
    - Define `CHART_SPECS` con las gráficas `caso_auc` y `coste_verificacion`.

Estructura Interna:
    - Constantes `SLIDES_P2` y `CHART_SPECS` sin lógica ni imports.

Entradas / Dependencias:
    - Ninguna (módulo puro de datos; Chart.js se inyecta desde `build_deck.py`).

Salidas / Efectos:
    - Cuerpos HTML y configuraciones JSON serializables para el motor del deck.

Ejemplo de Integración:
    from slides_p2 import SLIDES_P2, CHART_SPECS  # vía importlib en build_deck
"""

SLIDES_P2 = [
    {
        "id": "14-el-caso",
        "block": 3,
        "kicker": "Bloque 3 · min 52–56",
        "title": "Los casos reales, en paralelo: Web y Data Science",
        "sub": "Dos dominios distintos, el mismo proceso de especificación, construcción aislada y verificación.",
        "body": """
<div class="grid2">
  <div class="card accent-cobalt frag" data-step="1">
    <span class="num">Caso Data Science</span>
    <h3>demos/sdd-churn-leakage</h3>
    <p><strong>1,203 clientes</strong> en <strong>data/churn_events.csv</strong> (Golden Data determinista, <strong>seed=42</strong>) y contrato de tests en <strong>tests/test_demo_seed.py</strong>. Tensión: AUC <strong>0.9593</strong> con fuga vs <strong>0.8318</strong> honesto (brecha <strong>0.1275</strong>).</p>
  </div>
  <div class="card accent-amber frag" data-step="2">
    <span class="num">Caso Web Full-Stack</span>
    <h3>AgroVision</h3>
    <p>Gateway <strong>FastAPI :8000</strong> + SPA estática <strong>Astro 5 + Tailwind 4</strong>, Supabase <strong>PostGIS</strong> con credenciales efímeras BYOK (<code>X-User-*</code>), <strong>5 índices</strong> espectrales Sentinel-2 y deploy en <strong>Hugging Face Spaces</strong>: <strong>16 fases</strong> en <strong>plan_agrovision.md</strong>.</p>
  </div>
</div>
<p style="margin-top:16px" class="frag" data-step="3"><span class="pill cobalt">especificar</span><span class="pill cobalt">planificar</span><span class="pill amber">construir · goldfish</span><span class="pill emerald">testear · Playwright / Golden Data</span><span class="pill emerald">verificar-dod</span><span class="pill cobalt">auditar-coherencia</span></p>
<p style="margin-top:4px" class="frag" data-step="4">Mismo flujo, estándares por dominio: <strong>Web</strong> &rarr; <strong>backend-standards + astro-standards</strong>; <strong>Data Science</strong> &rarr; <strong>python-standards + EDD</strong> (Golden Data).</p>
""",
    },
    {
        "id": "15-elefante-goldfish",
        "block": 3,
        "kicker": "Bloque 3 · min 56–62",
        "title": "Elefante vs Goldfish: quién lleva el contexto",
        "sub": "El equipo conoce el negocio (contexto rico); el asistente parte de cero en cada sesión (zero-context).",
        "body": """
<svg viewBox="0 0 1080 320" style="max-width:1080px; width:100%" role="img" aria-label="Diagrama animado Elefante con contexto rico frente a Goldfish con contexto cero">
  <!-- Elefante: contexto rico -->
  <g class="pulse">
    <rect x="60" y="50" width="380" height="200" rx="18" fill="#EFF6FF" stroke="#1E40AF" stroke-width="2"/>
    <path d="M 150 190 q 10 -70 80 -70 q 70 0 80 55 l 12 0 q 25 0 28 -35 q 3 -20 -12 -22 l -8 0 q 5 -18 -6 -20 q -10 -2 -12 14 l -6 40 q -2 12 -14 12 l -96 0 q -20 0 -26 26 z"
          fill="none" stroke="#1E40AF" stroke-width="4" stroke-linecap="round"/>
    <text x="250" y="105" text-anchor="middle" class="node-label" fill="#1E40AF" font-size="18">ELEFANTE</text>
  </g>
  <text x="250" y="284" text-anchor="middle" fill="#475569" font-size="15">Contexto rico: negocio, estacionalidad, contratos, incidencias</text>
  <text x="250" y="308" text-anchor="middle" fill="#1E40AF" font-size="14" font-family="'IBM Plex Mono',monospace">la spec escribe lo que el elefante da por obvio</text>

  <!-- Goldfish: zero-context -->
  <g class="pulse" style="animation-delay:.6s">
    <rect x="620" y="50" width="400" height="200" rx="18" fill="#FFFBEB" stroke="#B45309" stroke-width="2"/>
    <path d="M 770 150 q 30 -26 60 0 q -30 26 -60 0 z" fill="none" stroke="#B45309" stroke-width="4" stroke-linecap="round"/>
    <path d="M 830 150 l 26 -18 l 0 36 z" fill="none" stroke="#B45309" stroke-width="4" stroke-linejoin="round"/>
    <circle cx="786" cy="144" r="3.5" fill="#B45309"/>
    <text x="820" y="105" text-anchor="middle" class="node-label" fill="#B45309" font-size="18">GOLDFISH</text>
  </g>
  <text x="820" y="284" text-anchor="middle" fill="#475569" font-size="15">Zero-context: solo ve filas del CSV, sin memoria de sesión</text>
  <text x="820" y="308" text-anchor="middle" fill="#B45309" font-size="14" font-family="'IBM Plex Mono',monospace">lo que no está en la spec, no existe</text>

  <!-- Conector animado -->
  <path d="M 440 150 H 620" fill="none" stroke="#94A3B8" stroke-width="2.5" class="flow-dash"/>
  <text x="530" y="138" text-anchor="middle" fill="#475569" font-size="14" font-family="'IBM Plex Mono',monospace">spec = puente</text>
</svg>
""",
    },
    {
        "id": "16-la-fuga",
        "block": 3,
        "kicker": "Bloque 3 · min 62–68",
        "title": "La fuga: cuando 0.9593 es demasiado bueno",
        "sub": "Tres fugas conviven en el antiejemplo: temporal, de preprocesamiento y de split.",
        "body": """
<div class="grid2">
  <div class="card accent-carmine frag" data-step="1">
    <h3>El código culpable (src/train_baseline.py)</h3>
    <div class="code"><span class="cm"># Features legítimas: conocidas EN el snapshot</span>
FEATURES_HONESTAS = [tenure_months, monthly_spend,
    support_tickets_30d, usage_drop_pct]
<span class="cm"># Antiejemplo: se suma la columna post-churn</span>
<span class="bad">FEATURES_FUGA = FEATURES_HONESTAS + [
    "post_churn_cancellation_days"]</span>
<span class="bad">X = StandardScaler().fit_transform(X_fuga)  # BUG: antes del split</span>
<span class="bad">train_test_split(X, ..., random_state=42)   # BUG: split aleatorio</span>
<span class="cm"># AUC: 0.9593 — "increíble" 🎉</span></div>
  </div>
  <div class="card frag" data-step="2">
    <h3>La lectura SDD</h3>
    <ul>
      <li><strong>post_churn_cancellation_days</strong> solo existe cuando el churn ya ocurrió: fuga temporal directa.</li>
      <li>El <strong>StandardScaler</strong> aprende media/desviación de TODO el dataset antes del split: fuga de preprocesamiento.</li>
      <li>El <strong>split aleatorio</strong> mete snapshots del futuro en el train: tercera fuga.</li>
    </ul>
  </div>
</div>
<p style="margin-top:16px" class="frag" data-step="3">Chequeo ODD: <strong>"¿existiría esta feature en el instante del snapshot_date?"</strong> Si no: fuga. <br><strong>Paralelo Web</strong> (AgroVision · <strong>T10.4.1</strong>): el vibe pondría un regex en Astro y rompería prod; la tarea real pide <strong>allowlist anti-SSRF</strong> en <code>X-User-Supabase-Url</code> y <strong>límite geométrico del polígono en servidor</strong>, resuelta con backend-standards + astro-standards y E2E Playwright.</p>
""",
    },
    {
        "id": "17-honesto",
        "block": 3,
        "kicker": "Bloque 3 · min 68–71",
        "title": "Honestidad: bajar la métrica para subir la verdad",
        "sub": "Split temporal (pasado → train, futuro → test) y solo features disponibles al momento de predecir.",
        "body": """
<svg viewBox="0 0 1080 330" style="max-width:1080px; width:100%" role="img" aria-label="Comparativa animada: AUC 0.9593 con fuga frente a AUC 0.8318 honesto">
  <text x="120" y="30" fill="#0F172A" font-size="17" font-family="'Space Grotesk','IBM Plex Sans',sans-serif" font-weight="600">
    Bajar de 0.9593 a 0.8318 no fue una pérdida: fue el momento en que el número empezó a decir la verdad.
  </text>

  <!-- Eje de valores (escala horizontal: 0.75 -> x=120 · 0.96 -> x=860) -->
  <line x1="120" y1="270" x2="1000" y2="270" stroke="#94A3B8" stroke-width="2"/>
  <g font-family="'IBM Plex Mono',monospace" font-size="14" fill="#94A3B8">
    <text x="120" y="296">0.75</text>
    <text x="472" y="296" text-anchor="middle">0.85</text>
    <text x="648" y="296" text-anchor="middle">0.90</text>
    <text x="860" y="296" text-anchor="middle">0.96</text>
  </g>

  <!-- Referencia honesta: línea vertical en ~0.80 (x = 296) -->
  <line x1="296" y1="50" x2="296" y2="270" stroke="#047857" stroke-width="2" stroke-dasharray="8 8"/>
  <text x="304" y="52" fill="#047857" font-size="13" font-family="'IBM Plex Mono',monospace">zona honesta &le; 0.80</text>

  <!-- Barra 1: 0.9593 con fuga (120 -> 858 px) -->
  <g>
    <rect x="120" y="80" width="738" height="56" rx="10" fill="#FEF2F2" stroke="#B91C1C" stroke-width="2" class="grow-bar" style="transform-origin:120px center"/>
    <text x="142" y="115" fill="#B91C1C" font-size="20" font-family="'IBM Plex Mono',monospace" font-weight="700">AUC 0.9593</text>
    <text x="440" y="115" fill="#B91C1C" font-size="15" font-family="'IBM Plex Mono',monospace">CON FUGA · engañoso</text>
    <circle cx="820" cy="108" r="7" fill="#B91C1C" class="pulse"/>
  </g>

  <!-- Barra 2: 0.8318 honesto (120 -> 408 px) -->
  <g>
    <rect x="120" y="180" width="288" height="56" rx="10" fill="#ECFDF5" stroke="#047857" stroke-width="2" class="grow-bar" style="transform-origin:120px center; animation-delay:.9s"/>
    <text x="142" y="215" fill="#047857" font-size="20" font-family="'IBM Plex Mono',monospace" font-weight="700">AUC 0.8318</text>
    <text x="418" y="215" fill="#047857" font-size="15" font-family="'IBM Plex Mono',monospace">HONESTO · split temporal</text>
  </g>
</svg>
""",
    },
    {
        "id": "18-chart-caso",
        "block": 3,
        "kicker": "Bloque 3 · min 71–75",
        "title": "El caso en números: fuga, honestidad y brecha",
        "sub": "Valores exactos y reproducibles del laboratorio (seed=42): los mismos que verás en el terminal de la práctica 1.",
        "body": """
<div class="grid2">
  <div class="chart-box frag" data-step="1">
    <h3>AUC por evaluación — churn_events.csv</h3>
    <div class="cwrap"><canvas data-chart="caso_auc"></canvas></div>
    <p class="chart-note">Brecha real: <strong>0.9593 &minus; 0.8318 = 0.1275</strong>. No es ruido: es la diferencia entre dashboard bonito y decisión de negocio.</p>
    <p class="chart-fallback">Chart.js no disponible — valores: 0.9593 / 0.8318 (brecha 0.1275).</p>
  </div>
  <div style="display:flex; flex-direction:column; gap:18px">
    <div class="card accent-emerald frag" data-step="2">
      <h3>Lectura gerencial</h3>
      <p>La brecha <strong>0.1275</strong> es la mentira cuantificada: el 0.9593 no predice churn, lo <strong>recuerda</strong>. EDD registró 0.8318 con procedencia (Golden Data, seed=42).</p>
    </div>
    <div class="card accent-cobalt frag" data-step="3">
      <h3>Lectura técnica</h3>
      <p>El <strong>baseline honesto</strong> (reg-log + split temporal) es la referencia: sin baseline no hay narrativa. El contrato del laboratorio exige <strong>leaky_auc &ge; 0.93 &gt; honest_auc</strong> y lo verifica <strong>test_demo_seed.py</strong>.</p>
    </div>
  </div>
</div>
""",
    },
    # ------------------------------------------------------------------ B4
    {
        "id": "19-divider-b4",
        "block": 4,
        "layout": "divider",
        "kicker": "BLOQUE 4 · 75–100 MIN",
        "title": "Verificar es invertir: el coste que sí sale en la hoja de cálculo",
        "sub": "",
        "body": """
<p class="d-meta">
  <span class="pill emerald">testear</span>
  <span class="pill emerald">verificar-dod</span>
  <span class="pill cobalt">auditar-coherencia</span>
  <span class="pill carmine">💻 Prácticas 2 y 3 en el terminal</span>
</p>
<p class="d-time">El rework no avisado es la deuda más cara del proyecto real.</p>
""",
    },
    {
        "id": "20-chart-coste",
        "block": 4,
        "kicker": "Bloque 4 · min 77–82",
        "title": "Coste de verificación: Vibe Coding vs SDD + ODD",
        "sub": "Horas acumuladas de rework + verificación por semana del proyecto (mismo alcance, mismo equipo).",
        "body": """
<div class="grid2">
  <div class="chart-box frag" data-step="1">
    <h3>Horas acumuladas por semana</h3>
    <div class="cwrap"><canvas data-chart="coste_verificacion"></canvas></div>
    <p class="chart-note">SDD paga más al inicio (spec + tests) y desploma la curva de rework desde la semana 3.</p>
    <p class="chart-fallback">Chart.js no disponible — series: 31h vs 11h a la semana 6.</p>
  </div>
  <div style="display:flex; flex-direction:column; gap:18px">
    <div class="card accent-carmine frag" data-step="2">
      <h3>Vibe Coding: barato al principio</h3>
      <p>Semana 1: 1 hora. Semana 6: <strong>31 horas</strong> de cazar regresiones que nadie especificó y nadie testea.</p>
    </div>
    <div class="card accent-emerald frag" data-step="3">
      <h3>SDD + ODD: inversión con pendiente positiva</h3>
      <p>La verificación es parte del trabajo planificado: <strong>11 horas acumuladas</strong> y el sistema sigue entregando.</p>
    </div>
  </div>
</div>
""",
    },
    {
        "id": "21-practica-2",
        "block": 4,
        "kicker": "Bloque 4 · Parte A · Ejercicio en vivo · min 82–88",
        "title": "Práctica 2: auditoría ODD + bitácora + Constitución SDD",
        "sub": "Cambio al terminal: especificamos con contrato Pydantic + Golden Data y auditamos sin editar nada (read-only).",
        "body": """
<div class="grid2" style="grid-template-columns: 1.08fr 1fr">
  <div class="card accent-cobalt frag" data-step="1">
    <span class="live-badge"><span class="dot-live"></span>💻 EJERCICIO EN VIVO · IR AL TERMINAL</span>
    <h3 style="margin-top:14px">demos/sdd-churn-leakage/ · Parte A</h3>
    <ol class="steps">
      <li>Lee la Constitución SDD del mini-proyecto: <strong>cat AGENTS.md</strong></li>
      <li>Especifica con contrato: <strong>/project-suite:especificar</strong> &rarr; regla anti-fuga y Golden Data en la spec.</li>
      <li>Planifica en modo estricto: <strong>/project-suite:planificar</strong> &rarr; Fases &rarr; Tareas con DoD.</li>
      <li>Audita en solo lectura: <strong>/project-suite:auditar-coherencia</strong> (docs &harr; código).</li>
      <li>Registra la fuga en la bitácora: <strong>docs/logs/log.md</strong> (síntoma &rarr; causa raíz &rarr; lecciones).</li>
    </ol>
    <p style="margin-top:8px"><strong>Resultado esperado:</strong> la regla "features disponibles al snapshot" queda escrita en la spec <strong>antes</strong> del código.</p>
  </div>
  <div class="card frag" data-step="2">
    <div class="terminal">
      <div class="t-head"><span class="t-dot r"></span><span class="t-dot y"></span><span class="t-dot g"></span><span style="margin-left:8px">demos/sdd-churn-leakage — bash</span></div>
      <div class="t-body"><span class="t-cmd">$ cat AGENTS.md</span>
<span class="t-out"># Reglas: prohibida la fuga temporal ·</span>
<span class="t-out"># Golden Data obligatorio · modo estricto</span>
<span class="t-cmd">$ /project-suite:especificar</span>
<span class="t-good">[OK] Contrato Pydantic + Golden Data (seed=42)</span>
<span class="t-cmd">$ /project-suite:planificar</span>
<span class="t-good">[OK] Fases → Sub fases → Tareas con DoD</span>
<span class="t-cmd">$ /project-suite:auditar-coherencia  <span class="t-out"># read-only</span></span>
<span class="t-good">[OK] 0 divergencias docs ↔ código</span></div>
    </div>
    <p style="margin-top:14px"><strong>Auditoría ODD:</strong> pesa cada decisión (¿reversible?) y dimensiona su doc — sin escribir código todavía.</p>
  </div>
</div>
""",
    },
    {
        "id": "22-practica-3",
        "block": 4,
        "kicker": "Bloque 4 · Parte B · Ejercicio en vivo · min 88–94",
        "title": "Práctica 3: ejecución aislada EGM, de construir a commit",
        "sub": "Cambio al terminal: un subagente por tarea, tests del Golden Data, gate de DoD y commit semántico.",
        "body": """
<div class="grid2" style="grid-template-columns: 1.08fr 1fr">
  <div class="card accent-emerald frag" data-step="1">
    <span class="live-badge"><span class="dot-live"></span>💻 EJERCICIO EN VIVO · IR AL TERMINAL</span>
    <h3 style="margin-top:14px">demos/sdd-churn-leakage/ · Parte B</h3>
    <ol class="steps">
      <li>Construye aislado: <strong>/project-suite:construir</strong> (1 subagente por tarea, python-standards).</li>
      <li>Testea: <strong>/project-suite:testear</strong> (unitarios + simulación de usuario).</li>
      <li>Verifica el Golden Data: <strong>python -m pytest tests -v</strong></li>
      <li>Gate de cierre: <strong>/project-suite:verificar-dod</strong> &rarr; recién ahí se marca <strong>[X]</strong>.</li>
      <li>Ordena el cierre: <strong>/semantic-commit</strong> (nunca push manual).</li>
    </ol>
    <p style="margin-top:8px"><strong>Resultado esperado:</strong> el pipeline honesto queda construido, testado contra el contrato y commiteado con evidencia.</p>
  </div>
  <div class="card frag" data-step="2">
    <div class="terminal">
      <div class="t-head"><span class="t-dot r"></span><span class="t-dot y"></span><span class="t-dot g"></span><span style="margin-left:8px">demos/sdd-churn-leakage — bash</span></div>
      <div class="t-body"><span class="t-cmd">$ /project-suite:construir</span>
<span class="t-good">[OK] 1 subagente por tarea · python-standards</span>
<span class="t-cmd">$ python -m pytest tests -v</span>
<span class="t-good">test_demo_seed.py · leaky 0.9593 &gt; honest 0.8318</span>
<span class="t-out">brecha reproducida: 0.1275 · CLI código 0</span>
<span class="t-cmd">$ /project-suite:verificar-dod</span>
<span class="t-good">[OK] DoD verde → [X] marcado en tareas.md</span>
<span class="t-cmd">$ /semantic-commit</span>
<span class="t-good">[OK] commit semántico · sin push</span></div>
    </div>
    <p style="margin-top:14px"><strong>EGM aislado:</strong> cada comando deja un artefacto verificable; el ciclo evolutivo del dashboard se ejecuta completo.</p>
  </div>
</div>
""",
    },
    {
        "id": "23-dod",
        "block": 4,
        "kicker": "Bloque 4 · min 94–97",
        "title": "DoD: la puerta de salida de cada tarea",
        "sub": "verificar-dod corre el gate completo antes de marcar cualquier [X] en el tablero.",
        "body": """
<div class="grid2">
  <div class="card accent-emerald frag" data-step="1">
    <h3>El gate</h3>
    <ul>
      <li><strong>Tests declarados en verde</strong>: unitarios + simulación de usuario.</li>
      <li><strong>Cobertura vs umbral</strong> definido en el plan, no negociado a último minuto.</li>
      <li><strong>Lint/format sin warnings</strong> en los archivos tocados.</li>
      <li><strong>Cambios de DB/env documentados</strong>: diseno_db.md, .env.example, architecture.md.</li>
    </ul>
  </div>
  <div class="card frag" data-step="2">
    <h3>El registro</h3>
    <div class="code"><span class="cm"># tests/ — test_demo_seed.py · 6 passed</span>
<span class="cm"># lint: 0 warnings</span>
<span class="good">DoD OK</span> &rarr; <span class="good">[X]</span> marcado en tareas.md
<span class="cm"># sync del tablero + índice de sub fase</span></div>
    <p style="margin-top:12px">Un checkbox marcado sin DoD en verde es <strong>mentira documentada</strong>.</p>
  </div>
</div>
""",
    },
    {
        "id": "24-coherencia-bitacora",
        "block": 4,
        "kicker": "Bloque 4 · min 97–100",
        "title": "Coherencia y bitácora: el proyecto que se explica solo",
        "sub": "Docs fieles al código e incidentes con autopsia completa.",
        "body": """
<div class="grid2">
  <div class="card accent-cobalt frag" data-step="1">
    <h3>auditar-coherencia</h3>
    <p>Compara architecture.md y diseno_db.md contra el código real (migraciones, modelos, repos) y <strong>rankea las divergencias</strong>. El drift se detecta en minutos, no en producción.</p>
  </div>
  <div class="card accent-carmine frag" data-step="2">
    <h3>bitácora (log.md)</h3>
    <p>Formato forense por incidente:</p>
    <div class="code" style="margin-top:10px">síntoma &rarr; hipótesis &rarr; <span class="bad">causa raíz</span>
&rarr; resolución &rarr; verificación &rarr; <span class="good">lecciones</span></div>
  </div>
</div>
<p style="margin-top:18px" class="frag" data-step="3">El leakage del laboratorio quedó registrado así: <strong>síntoma</strong> (AUC 0.9593), <strong>causa raíz</strong> (post_churn_cancellation_days + scaler antes del split + split aleatorio), <strong>lección</strong> (chequeo ODD de disponibilidad temporal en toda feature). En <strong>AgroVision</strong>, auditar-coherencia mantiene <strong>architecture_agrovision.md</strong> fiel al gateway FastAPI + Astro: la misma disciplina, otro dominio.</p>
""",
    },
    # ------------------------------------------------------------------ B5
    {
        "id": "25-checklist",
        "block": 5,
        "kicker": "Bloque 5 · min 100–110",
        "title": "Adoptar SDD mañana: checklist de 5 pasos",
        "sub": "No necesitas migrar todo el repositorio: necesitas el próximo cambio bien nacido.",
        "body": """
<div class="grid5">
  <div class="card accent-cobalt frag" data-step="1">
    <div class="num">Paso 1</div>
    <h3>Elige el cambio</h3>
    <p>Un feature real, no un toy. Idealmente irreversible (datos, API).</p>
  </div>
  <div class="card accent-cobalt frag" data-step="2">
    <div class="num">Paso 2</div>
    <h3>Escribe la spec</h3>
    <p>Tres preguntas: ¿qué?, ¿cómo fluye el dato?, ¿dónde vive?</p>
  </div>
  <div class="card accent-amber frag" data-step="3">
    <div class="num">Paso 3</div>
    <h3>Aplica ODD</h3>
    <p>Pesa la irreversibilidad y dimensiona el doc.</p>
  </div>
  <div class="card accent-cobalt frag" data-step="4">
    <div class="num">Paso 4</div>
    <h3>Planifica tareas</h3>
    <p>Fases con DoD y dos niveles de test por tarea.</p>
  </div>
  <div class="card accent-emerald frag" data-step="5">
    <div class="num">Paso 5</div>
    <h3>Verifica y registra</h3>
    <p>DoD en verde antes del [X]; incidentes a bitácora.</p>
  </div>
</div>
<p style="margin-top:20px" class="frag" data-step="6">Métrica de éxito de la semana: <strong>0 cambios de código sin spec</strong> en lo irreversible.</p>
""",
    },
    {
        "id": "26-recursos",
        "block": 5,
        "kicker": "Bloque 5 · min 110–115",
        "title": "Recursos: el repo y el flujo completo",
        "sub": "Todo lo mostrado vive documentado y ejecutable en el repositorio de charlas.",
        "body": """
<div class="grid2">
  <div class="card accent-cobalt frag" data-step="1">
    <h3>Repositorio</h3>
    <div class="code">github.com/AlexPrietoRomani/charlas
<span class="cm">├── docs/</span>              spec viva del repo
<span class="cm">├── talks/2026-sdd-proyectos-reales/</span>  esta charla
<span class="cm">├── demos/sdd-churn-leakage/</span>  laboratorio en vivo
<span class="cm">└── scripts/</span>           build_all + tablero</div>
  </div>
  <div class="card frag" data-step="2">
    <h3>Comandos project-suite</h3>
    <div class="code">/project-suite:especificar   <span class="cm"># spec técnica</span>
/project-suite:planificar    <span class="cm"># fases y tareas</span>
/project-suite:construir     <span class="cm"># 1 subagente por tarea</span>
/project-suite:testear       <span class="cm"># unit + simulación</span>
/project-suite:verificar-dod <span class="cm"># gate del [X]</span>
/project-suite:auditar-coherencia <span class="cm"># docs &harr; código</span></div>
  </div>
</div>
""",
    },
    {
        "id": "27-cierre",
        "block": 5,
        "layout": "divider",
        "kicker": "BLOQUE 5 · CIERRE · 115–120 MIN",
        "title": "La especificación es el contrato; la verificación, la inversión; la evidencia, el informe final.",
        "sub": "",
        "body": """
<p class="d-meta">
  <span class="pill cobalt">SDD</span>
  <span class="pill amber">ODD</span>
  <span class="pill emerald">EGM</span>
  <span class="pill emerald">EDD</span>
  <span class="pill cobalt">Web · AgroVision</span>
  <span class="pill amber">Data Science · churn</span>
</p>
<p class="d-time">Gracias — preguntas y discusión. · Alex Prieto Romani · alexprieto1997@gmail.com</p>
""",
    },
]

CHART_SPECS = {
    "caso_auc": {
        "type": "bar",
        "data": {
            "labels": [
                "Con fuga (split aleatorio + post_churn)",
                "Honesto (split temporal, sin fuga)",
            ],
            "datasets": [
                {
                    "label": "AUC",
                    "data": [0.9593, 0.8318],
                    "backgroundColor": ["#B91C1C", "#047857"],
                    "borderColor": ["#B91C1C", "#047857"],
                    "borderWidth": 1.5,
                    "borderRadius": 8,
                    "maxBarThickness": 90,
                }
            ],
        },
        "options": {
            "responsive": True,
            "maintainAspectRatio": False,
            "plugins": {
                "legend": {"display": False},
                "title": {
                    "display": True,
                    "text": "AUC del clasificador de churn — 1,203 clientes (seed=42)",
                },
            },
            "scales": {
                "y": {
                    "min": 0.6,
                    "max": 1.0,
                    "title": {"display": True, "text": "AUC"},
                }
            },
        },
    },
    "coste_verificacion": {
        "type": "line",
        "data": {
            "labels": ["S1", "S2", "S3", "S4", "S5", "S6"],
            "datasets": [
                {
                    "label": "SDD + ODD",
                    "data": [2, 4, 6, 8, 10, 11],
                    "borderColor": "#047857",
                    "backgroundColor": "#ECFDF5",
                    "tension": 0.35,
                    "fill": True,
                    "borderWidth": 2.5,
                    "pointRadius": 4,
                },
                {
                    "label": "Vibe Coding",
                    "data": [1, 3, 7, 13, 21, 31],
                    "borderColor": "#B91C1C",
                    "backgroundColor": "rgba(185, 28, 28, 0.07)",
                    "tension": 0.35,
                    "fill": True,
                    "borderWidth": 2.5,
                    "pointRadius": 4,
                },
            ],
        },
        "options": {
            "responsive": True,
            "maintainAspectRatio": False,
            "plugins": {
                "legend": {"position": "bottom"},
                "title": {
                    "display": True,
                    "text": "Coste acumulado de rework + verificación (horas)",
                },
            },
            "scales": {
                "y": {
                    "min": 0,
                    "max": 36,
                    "title": {"display": True, "text": "Horas acumuladas"},
                }
            },
        },
    },
}
