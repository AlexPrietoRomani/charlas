"""
Archivo: talks/2026-sdd-proyectos-reales/front/slides_p1.py
Fecha de modificación: 15/11/2026
Autor: Alex Prieto <alexprieto1997@gmail.com>

Descripción:
Diapositivas 1 a 13 de la charla `2026-sdd-proyectos-reales` (Bloques 1 y 2,
más el divisor del Bloque 3) con estética Bento gerencial. Cada entrada es un
dict de datos puros: id, bloque, kicker, título, subtítulo, layout y cuerpo
HTML con fragmentos progresivos (`data-step`).

Acciones Principales:
    - Define `SLIDES_P1`: lista ordenada de diapositivas en formato de datos.
    - Incluye el Bento Dashboard a ancho completo `SDD -> ODD -> EGM -> EDD`
      (slide 5) y la lámina `EJERCICIO EN VIVO · IR AL TERMINAL` del antiejemplo
      `demos/sdd-churn-leakage/` (slide 6).

Estructura Interna:
    - Constantes `SLIDES_P1` sin lógica ni imports: consumidas por `back/build_deck.py`.

Entradas / Dependencias:
    - Ninguna (módulo puro de datos; cifras del laboratorio: 1,203 clientes,
      AUC 0.9593 con fuga vs 0.8318 honesto, brecha 0.1275).

Salidas / Efectos:
    - Cuerpos HTML renderizados dentro de `<section class="slide">`.

Ejemplo de Integración:
    from slides_p1 import SLIDES_P1  # vía importlib en build_deck
"""

SLIDES_P1 = [
    # ------------------------------------------------------------------ B1
    {
        "id": "01-portada",
        "block": 1,
        "layout": "cover",
        "kicker": "TALLER · MASTERCLASS · 2 HORAS",
        "title": "Aplicación de SDD en proyectos reales",
        "sub": ("SDD + flexibilidad ODD + rigor EGM (+ EDD) con project-suite "
                "en un proyecto real de Data Science"),
        "body": """
<div class="c-meta">
  <span class="pill cobalt">SDD</span>
  <span class="pill amber">ODD</span>
  <span class="pill emerald">EGM</span>
  <span class="pill emerald">EDD</span>
  <span class="pill">project-suite</span>
  <span class="pill">Data Science</span>
</div>
<p class="c-author">Alex Prieto Romani · 2026-11-14 · 5 bloques · 120 minutos · 27 diapositivas</p>
""",
    },
    {
        "id": "02-agenda",
        "block": 1,
        "kicker": "Bloque 1 · min 5–7",
        "title": "Ruta del taller: cinco actos en dos horas",
        "sub": "Cada bloque cierra con una verificación: sin evidencia, no avanza.",
        "body": """
<div class="grid5">
  <div class="card accent-cobalt frag" data-step="1">
    <div class="num">Bloque 1 · 0–25'</div>
    <h3>El problema</h3>
    <p>Vibe Coding en producción y <strong>práctica 1 en el terminal</strong>.</p>
  </div>
  <div class="card accent-cobalt frag" data-step="2">
    <div class="num">Bloque 2 · 25–50'</div>
    <h3>Especificar y planificar</h3>
    <p>Spec, plan maestro, tareas y el flujo project-suite.</p>
  </div>
  <div class="card accent-amber frag" data-step="3">
    <div class="num">Bloque 3 · 50–75'</div>
    <h3>Caso real</h3>
    <p>Churn con leakage: AUC 0.9593 &rarr; 0.8318 honesto.</p>
  </div>
  <div class="card accent-emerald frag" data-step="4">
    <div class="num">Bloque 4 · 75–100'</div>
    <h3>Verificar es invertir</h3>
    <p>Coste de verificación y <strong>prácticas 2 y 3</strong> en el terminal.</p>
  </div>
  <div class="card accent-emerald frag" data-step="5">
    <div class="num">Bloque 5 · 100–120'</div>
    <h3>Adoptarlo mañana</h3>
    <p>Checklist accionable, recursos y preguntas.</p>
  </div>
</div>
""",
    },
    {
        "id": "03-vibe-dolor",
        "block": 1,
        "kicker": "Bloque 1 · min 7–13",
        "title": "Vibe Coding: rápido hasta que no",
        "sub": "Prompt, código, deploy, rezar. Funciona… hasta el primer cambio de requisitos.",
        "body": """
<div class="grid2">
  <div class="card accent-carmine frag" data-step="1">
    <h3>Síntomas en proyectos reales</h3>
    <ul>
      <li>La especificación vive en un chat que ya nadie encuentra.</li>
      <li>Cada "arreglo rápido" rompe dos cosas que funcionaban.</li>
      <li>Nadie sabe qué verificar para dar el proyecto por terminado.</li>
      <li>El onboarding de un compañero toma semanas, no días.</li>
    </ul>
  </div>
  <div class="card frag" data-step="2">
    <h3>La sesión típica</h3>
    <div class="code"><span class="cm"># 09:14 — prompt al asistente</span>
"hazme un pipeline de churn, algo moderno"
<span class="cm"># 09:41 — código generado</span>
<span class="bad">X = df[[..., "post_churn_cancellation_days"]]</span>
<span class="bad">X = StandardScaler().fit_transform(X)  # antes del split</span>
<span class="cm"># 11:02 — demo al gerente</span>
"¡AUC de 0.9593! listo para producción 🎉"
<span class="cm"># 14:30 — producción explota en silencio</span></div>
  </div>
</div>
<p style="margin-top:18px" class="frag" data-step="3">El problema no es la velocidad: es que <strong>nada define qué es "terminado"</strong> y qué evidencia lo prueba.</p>
""",
    },
    {
        "id": "04-que-es-sdd",
        "block": 1,
        "kicker": "Bloque 1 · min 13–18",
        "title": "SDD: la especificación como fuente de verdad",
        "sub": "Spec-Driven Development: los documentos describen el sistema antes de escribir código, y el código los sigue.",
        "body": """
<div class="grid2">
  <div class="card accent-cobalt frag" data-step="1">
    <h3>Tres documentos mínimos</h3>
    <ul>
      <li><strong>description_proyecto.md</strong> — qué hace y para quién.</li>
      <li><strong>architecture.md</strong> — cómo fluye el dato, decisiones (ADR).</li>
      <li><strong>diseno_db.md</strong> — dónde vive el dato, esquema y contratos.</li>
    </ul>
  </div>
  <div class="card frag" data-step="2">
    <h3>El cambio de mentalidad</h3>
    <ul>
      <li>El asistente es un <strong>compilador de especificaciones</strong>, no un oráculo.</li>
      <li>El plan se discute en docs baratos, no en reescrituras caras.</li>
      <li>Cada cambio nuevo es una <strong>decisión de planificación</strong> primero.</li>
    </ul>
  </div>
</div>
<div style="margin-top:20px" class="frag" data-step="3">
  <span class="pill cobalt">IDEA</span>&rarr;<span class="pill cobalt">SPEC</span>&rarr;<span class="pill cobalt">PLAN</span>&rarr;<span class="pill cobalt">TAREAS</span>&rarr;<span class="pill emerald">CÓDIGO VERIFICADO</span>
</div>
""",
    },
    {
        "id": "05-bento-dashboard",
        "block": 1,
        "kicker": "Bloque 1 · min 18–21",
        "title": "Del Vibe Coding a SDD → ODD → EGM + EDD",
        "sub": "Dos carriles hacia el mismo entregable: uno improvisa; el otro evoluciona con contrato, proporcionalidad, auditoría y evidencia.",
        "body": """
<div class="frag" data-step="1" style="margin-bottom:12px">
  <div class="lane-label" style="color:var(--carmine)">Carril 1 · Vibe Coding · el antiejemplo</div>
  <div class="lane">
    <div class="node" style="background:var(--carmine-soft); border-color:#FECACA">
      <div class="n-title" style="color:var(--carmine)">VIBE CODING</div>
      <div class="n-sub">sin spec · sin tests</div>
    </div>
    <div class="conn" style="color:var(--carmine)">&rarr;</div>
    <div class="node">
      <div class="n-title">Prompt &rarr; Rezar</div>
      <div class="n-sub">la spec vive en el chat</div>
    </div>
    <div class="conn" style="color:var(--carmine)">&rarr;</div>
    <div class="node" style="border-color:#FECACA">
      <div class="n-title">Código frágil</div>
      <div class="n-sub" style="color:var(--carmine); font-weight:700">AUC 0.9593 · fuga oculta</div>
    </div>
  </div>
</div>

<div class="frag" data-step="2" style="margin-bottom:14px">
  <div class="lane-label" style="color:var(--cobalt)">Carril 2 · Evolutivo · conectado y verificado</div>
  <div class="lane">
    <div class="node" style="background:var(--cobalt-soft); border-color:#BFDBFE">
      <div class="n-title" style="color:var(--cobalt)">1. SDD</div>
      <div class="n-sub">contrato</div>
    </div>
    <div class="conn" style="color:var(--cobalt)">&rarr;</div>
    <div class="node" style="background:var(--amber-soft); border-color:#FDE68A">
      <div class="n-title" style="color:var(--amber)">2. ODD</div>
      <div class="n-sub">proporcionalidad</div>
    </div>
    <div class="conn" style="color:var(--amber)">&rarr;</div>
    <div class="node">
      <div class="n-title">3. EGM</div>
      <div class="n-sub">elefante / goldfish</div>
    </div>
    <div class="conn" style="color:var(--sub)">&rarr;</div>
    <div class="node" style="background:var(--emerald-soft); border-color:#A7F3D0">
      <div class="n-title" style="color:var(--emerald)">4. EDD</div>
      <div class="n-sub">golden data</div>
    </div>
    <div class="conn" style="color:var(--emerald)">&rarr;</div>
    <div class="node" style="border:2px solid var(--emerald)">
      <div class="n-title" style="color:var(--emerald)">Entrega verificada</div>
      <div class="n-sub" style="color:var(--emerald); font-weight:700">AUC 0.8318 honesto</div>
    </div>
  </div>
</div>

<div class="grid3">
  <div class="card accent-cobalt frag" data-step="3">
    <span class="num">El salto 1 &rarr; 2</span>
    <h3>De contrato a proporcionalidad</h3>
    <p>El SDD rígido muere por burocracia ante cambios reales: <strong>ODD</strong> dimensiona cada documento según la irreversibilidad de la decisión.</p>
  </div>
  <div class="card accent-amber frag" data-step="4">
    <span class="num">El salto 2 &rarr; 3</span>
    <h3>De decidir a auditar</h3>
    <p>La flexibilidad exige verificar sin memoria de sesión: <strong>EGM</strong> audita zero-context con tests y DoD, no con impresiones del equipo.</p>
  </div>
  <div class="card accent-emerald frag" data-step="5">
    <div style="display:flex; align-items:center; justify-content:space-between">
      <div>
        <span class="num">El salto 3 &rarr; 4</span>
        <h3>De auditoría a evidencia</h3>
      </div>
      <svg viewBox="0 0 40 40" width="56" height="56" role="img" aria-label="Anillo: AUC honesto 0.8318">
        <circle cx="20" cy="20" r="16" fill="none" stroke="#E2E8F0" stroke-width="5"/>
        <circle cx="20" cy="20" r="16" fill="none" stroke="#047857" stroke-width="5"
                stroke-dasharray="83.6 100.5" stroke-linecap="round" transform="rotate(-90 20 20)"/>
        <text x="20" y="24" text-anchor="middle" font-size="10.5" font-weight="700" fill="#047857" font-family="'IBM Plex Mono',monospace">83%</text>
      </svg>
    </div>
    <p>En Data Science la prueba final es la métrica: <strong>EDD</strong> cierra el ciclo con Golden Data y el AUC honesto <strong>0.8318</strong>.</p>
  </div>
</div>
""",
    },
    {
        "id": "06-practica-1",
        "block": 1,
        "kicker": "Bloque 1 · Ejercicio en vivo · min 21–25",
        "title": "Práctica 1: el antiejemplo Vibe Coding, en vivo",
        "sub": "Cambio al terminal: el laboratorio demos/sdd-churn-leakage ejecuta el mismo pipeline que acabas de ver en el dashboard.",
        "body": """
<div class="grid2" style="grid-template-columns: 1.08fr 1fr">
  <div class="card accent-carmine frag" data-step="1">
    <span class="live-badge"><span class="dot-live"></span>💻 EJERCICIO EN VIVO · IR AL TERMINAL</span>
    <h3 style="margin-top:14px">demos/sdd-churn-leakage/</h3>
    <ol class="steps">
      <li>Entra al laboratorio: <strong>cd demos/sdd-churn-leakage</strong></li>
      <li>Ejecuta el antiejemplo: <strong>python src/train_baseline.py</strong></li>
      <li>Celebra el AUC <strong>0.9593</strong>… y pregunta a la sala: ¿lo subiríamos a producción?</li>
      <li>Encuentra la fuga: <strong>post_churn_cancellation_days</strong> + scaler fitteado antes del split.</li>
      <li>Lee el veredicto honesto del mismo script: <strong>0.8318</strong>.</li>
    </ol>
    <p style="margin-top:8px"><strong>Prompt sin spec:</strong> "Necesito un modelo de churn. Pásame los datos y pide el AUC al chat."</p>
  </div>
  <div class="card frag" data-step="2">
    <div class="terminal">
      <div class="t-head"><span class="t-dot r"></span><span class="t-dot y"></span><span class="t-dot g"></span><span style="margin-left:8px">demos/sdd-churn-leakage — bash</span></div>
      <div class="t-body"><span class="t-cmd">$ python src/train_baseline.py</span>
<span class="t-out">==============================================================</span>
<span class="t-out">DEMO: El modelo de 0.96 AUC que miente en producción</span>
<span class="t-out">==============================================================</span>
<span class="t-bad">AUC con fuga (split aleatorio + post_churn): 0.9593</span>
<span class="t-good">AUC honesto (split temporal, sin fuga):      0.8318</span>
<span class="t-out">Brecha: 0.1275</span></div>
    </div>
    <p style="margin-top:14px"><strong>Resultado esperado:</strong> el mismo dataset (<strong>1,203 clientes</strong> en <strong>data/churn_events.csv</strong>, seed=42) promete <strong>0.9593</strong> y vale <strong>0.8318</strong>.</p>
  </div>
</div>
""",
    },
    # ------------------------------------------------------------------ B2
    {
        "id": "07-divider-b2",
        "block": 2,
        "layout": "divider",
        "kicker": "BLOQUE 2 · 25–50 MIN",
        "title": "Especificar y planificar: el contrato antes del código",
        "sub": "",
        "body": """
<p class="d-meta">
  <span class="pill cobalt">description_proyecto.md</span>
  <span class="pill cobalt">architecture.md</span>
  <span class="pill cobalt">diseno_db.md</span>
  <span class="pill cobalt">plan_maestro.md</span>
  <span class="pill cobalt">tareas.md</span>
</p>
<p class="d-time">Entrevista de diseño &rarr; spec &rarr; plan &rarr; tablero de tareas ejecutables.</p>
""",
    },
    {
        "id": "08-la-spec",
        "block": 2,
        "kicker": "Bloque 2 · min 27–33",
        "title": "La especificación: tres documentos, tres preguntas",
        "sub": "Nace de una entrevista de diseño tipo brainstorming; cada doc responde una pregunta distinta.",
        "body": """
<div class="grid3">
  <div class="card accent-cobalt frag" data-step="1">
    <div class="num">¿Qué?</div>
    <h3>description_proyecto.md</h3>
    <p>Alcance, usuarios, éxitos y límites. Si no está aquí, no está en el proyecto.</p>
  </div>
  <div class="card accent-cobalt frag" data-step="2">
    <div class="num">¿Cómo?</div>
    <h3>architecture.md</h3>
    <p>Capas, flujos de dato, ADRs y scripts por flujo. El mapa del dato de punta a punta.</p>
  </div>
  <div class="card accent-cobalt frag" data-step="3">
    <div class="num">¿Dónde?</div>
    <h3>diseno_db.md</h3>
    <p>ER, diccionario de columnas, significado de PK y políticas de escritura.</p>
  </div>
</div>
<p style="margin-top:20px" class="frag" data-step="4">Regla de oro: <strong>los docs son la fuente de verdad</strong>. Si el código diverge, se corrige el código o el doc — nunca se conviven los dos.</p>
""",
    },
    {
        "id": "09-plan-tareas",
        "block": 2,
        "kicker": "Bloque 2 · min 33–39",
        "title": "Del plan maestro al tablero de tareas",
        "sub": "Fases → Sub fases → Tareas: cada tarea con Definition of Done y sus dos niveles de test.",
        "body": """
<div class="grid2">
  <div class="card accent-cobalt frag" data-step="1">
    <h3>plan_maestro.md</h3>
    <p style="margin-bottom:10px">Jerarquía ejecutable:</p>
    <div class="code"><span class="good">FASE 2</span> Especificar y planificar
 ├── <span class="good">Sub fase 2.1</span> Spec técnica
 │    ├── <span class="good">Tarea 2.1.1</span> description_proyecto
 │    ├── <span class="good">Tarea 2.1.2</span> architecture + ADRs
 │    └── <span class="good">Tarea 2.1.3</span> diseno_db + ER
 └── <span class="good">Sub fase 2.2</span> Plan y tablero</div>
  </div>
  <div class="card frag" data-step="2">
    <h3>tareas.md (tablero)</h3>
    <div class="code"><span class="good">[X]</span> T2.1.1 — spec con entrevistas <span class="cm">(DoD: revisión OK)</span>
<span class="good">[X]</span> T2.1.2 — ADRs de gateway y despliegue
<span class="cm">[ ]</span> T2.2.1 — derivar Fases → Tareas
<span class="cm">[ ]</span> T2.2.2 — cargar tablero tareas.md</div>
    <p style="margin-top:12px">Un checkbox <strong>[X]</strong> solo se marca cuando <strong>verificar-dod</strong> pasa en verde.</p>
  </div>
</div>
""",
    },
    {
        "id": "10-project-suite",
        "block": 2,
        "kicker": "Bloque 2 · min 39–44",
        "title": "project-suite: el flujo completo con guardarraíles",
        "sub": "Cada comando produce un artefacto verificable; ninguno deja código sin plan ni plan sin verificación.",
        "body": """
<svg viewBox="0 0 1080 250" style="max-width:1080px; width:100%" role="img" aria-label="Pipeline animado de project-suite">
  <defs>
    <marker id="arrow-g" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">
      <path d="M 0 0 L 10 5 L 0 10 z" fill="#1E40AF"/>
    </marker>
  </defs>

  <!-- Nodos -->
  <g font-family="'IBM Plex Mono',monospace" font-size="14" font-weight="600" text-anchor="middle">
    <rect x="30"  y="60" width="150" height="66" rx="12" fill="#EFF6FF" stroke="#1E40AF" stroke-width="1.5"/>
    <text x="105" y="88"  fill="#1E40AF">especificar</text>
    <text x="105" y="110" fill="#475569" font-size="12" font-weight="400">spec técnica</text>

    <rect x="235" y="60" width="150" height="66" rx="12" fill="#EFF6FF" stroke="#1E40AF" stroke-width="1.5"/>
    <text x="310" y="88"  fill="#1E40AF">planificar</text>
    <text x="310" y="110" fill="#475569" font-size="12" font-weight="400">fases y tareas</text>

    <rect x="440" y="60" width="170" height="66" rx="12" fill="#FFFBEB" stroke="#B45309" stroke-width="1.5"/>
    <text x="525" y="88"  fill="#B45309">construir</text>
    <text x="525" y="110" fill="#475569" font-size="12" font-weight="400">1 subagente por tarea</text>

    <rect x="665" y="60" width="140" height="66" rx="12" fill="#ECFDF5" stroke="#047857" stroke-width="1.5"/>
    <text x="735" y="88"  fill="#047857">testear</text>
    <text x="735" y="110" fill="#475569" font-size="12" font-weight="400">unit + simulación</text>

    <rect x="860" y="60" width="180" height="66" rx="12" fill="#ECFDF5" stroke="#047857" stroke-width="2"/>
    <text x="950" y="88"  fill="#047857">verificar-dod</text>
    <text x="950" y="110" fill="#475569" font-size="12" font-weight="400">gate antes del [X]</text>
  </g>

  <!-- Flechas animadas -->
  <path d="M 180 93 H 230" fill="none" stroke="#1E40AF" stroke-width="2.5" class="flow-dash" marker-end="url(#arrow-g)"/>
  <path d="M 385 93 H 435" fill="none" stroke="#1E40AF" stroke-width="2.5" class="flow-dash" marker-end="url(#arrow-g)"/>
  <path d="M 610 93 H 660" fill="none" stroke="#B45309" stroke-width="2.5" class="flow-dash" marker-end="url(#arrow-g)"/>
  <path d="M 805 93 H 855" fill="none" stroke="#047857" stroke-width="2.5" class="flow-dash" marker-end="url(#arrow-g)"/>

  <!-- Bucle de retroalimentación: verificar-dod -> construir -->
  <path d="M 950 126 C 950 190, 560 190, 540 130" fill="none" stroke="#B45309" stroke-width="2" class="flow-dash-rev" marker-end="url(#arrow-g)"/>
  <text x="740" y="205" text-anchor="middle" fill="#B45309" font-size="13" font-family="'IBM Plex Mono',monospace">DoD en rojo &rarr; vuelve a construir</text>

  <!-- Punto animado -->
  <circle r="5" fill="#1E40AF">
    <animateMotion dur="7s" repeatCount="indefinite" path="M 30 93 H 1040"/>
  </circle>

  <!-- Auditoría final -->
  <rect x="30" y="20" width="240" height="24" rx="12" fill="#FFFFFF" stroke="#E2E8F0" stroke-width="1.5"/>
  <text x="150" y="37" text-anchor="middle" fill="#475569" font-size="13" font-family="'IBM Plex Mono',monospace">auditar-coherencia + bitácora + semantic-commit</text>
</svg>
""",
    },
    {
        "id": "11-odd",
        "block": 2,
        "kicker": "Bloque 2 · min 44–47",
        "title": "ODD: por qué el SDD rígido necesita flexibilidad proporcional",
        "sub": "Outcome-Driven Development: el peso del documento crece con la irreversibilidad de la decisión.",
        "body": """
<table class="cmp frag" data-step="1">
  <tr><th>Decisión</th><th>Ejemplo real</th><th>Documento exigido</th></tr>
  <tr><td class="k">Reversible</td><td>Renombrar una función interna, copy de la UI</td><td>Comentario <span class="pill amber">ligero</span></td></tr>
  <tr><td class="k">Semi-reversible</td><td>Nuevo endpoint, cambio de esquema menor</td><td>Spec + test de simulación</td></tr>
  <tr><td class="k">Irreversible</td><td>Modelo de datos, API pública, seguridad</td><td>ADR + spec completa + auditoría</td></tr>
</table>
<div class="grid2" style="margin-top:20px">
  <div class="card accent-amber frag" data-step="2">
    <h3>Por qué SDD solo no basta</h3>
    <p>SDD estricto y rígido muere por burocracia: documentar todo al máximo bloquea el proyecto real. <strong>ODD evita el boicot</strong>: doc mínimo para riesgo mínimo, doc máximo para riesgo máximo.</p>
  </div>
  <div class="card frag" data-step="3">
    <h3>En la práctica</h3>
    <p>Antes de pedir el cambio al asistente, pregúntate: <strong>¿si me equivoco, cuánto cuesta revertirlo?</strong> Esa respuesta elige el formato del doc… y abre la pregunta siguiente: ¿quién verifica sin contexto?</p>
  </div>
</div>
""",
    },
    {
        "id": "12-egm-edd",
        "block": 2,
        "kicker": "Bloque 2 · min 47–50",
        "title": "EGM y EDD: auditoría zero-context y el ciclo de la evidencia",
        "sub": "ODD necesita verificación sin memoria; en Data Science la evidencia final es una métrica honesta.",
        "body": """
<div class="grid2">
  <div class="card accent-emerald frag" data-step="1">
    <span class="num">3 · EGM</span>
    <h3>Por qué ODD necesita auditoría zero-context</h3>
    <p>Decidir cuánto documentar es letra muerta si nadie lo verifica <strong>sin memoria de sesión</strong> (la goldfish). EGM audita con tests, DoD y docs contra el código: la evidencia no depende del equipo.</p>
  </div>
  <div class="card accent-emerald frag" data-step="2">
    <span class="num">4 · EDD</span>
    <h3>Cómo EDD cierra el ciclo en Data Science</h3>
    <p>La evidencia final es una métrica: <strong>Golden Data determinista</strong> (seed=42) + split temporal. EDD registra <strong>0.8318</strong> con procedencia, no un <strong>0.9593</strong> recitado de memoria.</p>
  </div>
</div>
<p style="margin-top:20px" class="frag" data-step="3">Progresión completa: <strong>SDD</strong> (qué construir) &rarr; <strong>ODD</strong> (cuánto documentar) &rarr; <strong>EGM</strong> (quién verifica) &rarr; <strong>EDD</strong> (qué evidencia cierra el ciclo).</p>
""",
    },
    # ------------------------------------------------------------------ B3
    {
        "id": "13-divider-b3",
        "block": 3,
        "layout": "divider",
        "kicker": "BLOQUE 3 · 50–75 MIN",
        "title": "Caso real: churn con leakage, del elefante a la goldfish",
        "sub": "",
        "body": """
<p class="d-meta">
  <span class="pill amber">demos/sdd-churn-leakage</span>
  <span class="pill carmine">AUC 0.9593 → sospecha</span>
  <span class="pill emerald">AUC 0.8318 → honesto</span>
</p>
<p class="d-time">Un pipeline de churn real donde SDD detectó lo que el entusiasmo había escondido.</p>
""",
    },
]
