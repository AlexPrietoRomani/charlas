"""
Archivo: talks/2026-sdd-proyectos-reales/front/notes.py
Fecha de modificación: 17/11/2026
Autor: Alex Prieto <alexprieto1997@gmail.com>

Descripción:
Notas del orador de la charla `2026-sdd-proyectos-reales` (taller de 2 horas,
5 bloques). Cada entrada está indexada por el `id` de la diapositiva y contiene
su ventana de tiempo (`time`) y el cuerpo detallado (`body`) que se muestra en
el panel de notas (tecla `N`). Todas las cifras provienen del laboratorio real
`demos/sdd-churn-leakage/` (1,203 clientes, AUC 0.9593 vs 0.8318, brecha 0.1275).

Acciones Principales:
    - Define `NOTES`: dict slide_id -> {time, body} con guion detallado por
      diapositiva, tiempos acumulados por bloque y avisos de coreografía,
      incluidos los tres cortes a terminal (prácticas 1, 2 y 3).

Estructura Interna:
    - Constante `NOTES` sin lógica ni imports.

Entradas / Dependencias:
    - Los `id` de `front/slides_p1.py` y `front/slides_p2.py`.

Salidas / Efectos:
    - `back/build_deck.py` serializa `NOTES` en `window.SPEAKER_NOTES` ordenado
      por índice de diapositiva.

Ejemplo de Integración:
    from notes import NOTES  # vía importlib en build_deck
"""

NOTES = {
    "01-portada": {
        "time": "min 00–05 · Bloque 1 (0–25')",
        "body": (
            "<p><strong>[0:00] Bienvenida y encuadre (3').</strong> Preséntate y aclara el formato: "
            "taller de 2 horas, 5 bloques, con teclado: <strong>&larr;/&rarr;</strong> navegar, "
            "<strong>N</strong> notas, <strong>G</strong> índice, <strong>F</strong> pantalla completa.</p>"
            "<ul><li>Pregunta rompehielos: '¿cuántos han entregado un proyecto que solo el autor entiende?'</li>"
            "<li>Anticipa los DOS proyectos reales: uno <strong>Web Full-Stack</strong> (AgroVision: FastAPI + Astro, "
            "caso T10.4.1) y uno de <strong>Data Science</strong> (churn con leakage, AUC 0.9593 &rarr; 0.8318).</li>"
            "<li>[4:00] Pasa a la agenda cuando la sala esté enganchada con el rompehielos.</li></ul>"
        ),
    },
    "02-agenda": {
        "time": "min 05–07 · Bloque 1 (0–25')",
        "body": (
            "<p><strong>Mapa de la sesión con tiempos duros</strong> — úsalo como contrato con la audiencia.</p>"
            "<ul><li>Revela los 5 bloques con los fragmentos (tecla &rarr;). Cada bloque cierra con verificación: sin evidencia no avanza.</li>"
            "<li>Aviso práctico: <strong>habrá tres cortes a terminal</strong> (prácticas 1, 2 y 3); pide que abran la carpeta demos/sdd-churn-leakage.</li>"
            "<li>Subraya que el Bloque 3 compara DOS casos reales: Web (AgroVision) y Data Science (churn); el Bloque 4 es el coste de verificación.</li></ul>"
        ),
    },
    "03-vibe-dolor": {
        "time": "min 07–13 · Bloque 1 (0–25')",
        "body": (
            "<p><strong>[7:00] Síntomas (3').</strong> Pide manos: '¿quién ha vivido el chat perdido con la especificación?'. "
            "Los síntomas de la izquierda deben sonar a experiencia propia.</p>"
            "<p><strong>[10:00] La sesión típica (3').</strong> Lee el código en voz alta: la feature <strong>post_churn_cancellation_days</strong> "
            "y el scaler fitteado antes del split son las fugas reales del laboratorio.</p>"
            "<p><strong>[11:30] El mismo vibe rompe distinto (1.5').</strong> En <strong>Web</strong> el daño es visible: "
            "un 'regex de validación' en Astro deja la URL BYOK <strong>X-User-Supabase-Url</strong> abierta a <strong>SSRF</strong> "
            "y desincroniza la BD de la UI. En <strong>Data Science</strong> el daño calla: un AUC <strong>0.9593</strong> que miente. "
            "Remata: 'el problema no es la velocidad, es que no existe la definición de éxito'.</p>"
        ),
    },
    "04-que-es-sdd": {
        "time": "min 13–18 · Bloque 1 (0–25')",
        "body": (
            "<p><strong>[13:00] Definición (3').</strong> SDD: los docs describen el sistema ANTES del código y el código los sigue. "
            "Los tres documentos mínimos del repo: description_proyecto, architecture, diseno_db.</p>"
            "<p><strong>[16:00] Mentalidad (2').</strong> El asistente es compilador de specs, no oráculo. "
            "Cierra con el pipeline IDEA &rarr; SPEC &rarr; PLAN &rarr; TAREAS &rarr; CÓDIGO VERIFICADO.</p>"
        ),
    },
    "05-bento-dashboard": {
        "time": "min 18–21 · Bloque 1 (0–25')",
        "body": (
            "<p><strong>[18:00] Bento Dashboard (3').</strong> Carril carmesí: VIBE CODING &rarr; Prompt &rarr; Rezar &rarr; "
            "CÓDIGO FRÁGIL (AUC 0.9593, fuga oculta). Carril evolutivo: 1. SDD (contrato) &rarr; 2. ODD (proporcionalidad) &rarr; "
            "3. EGM (elefante/goldfish) &rarr; 4. EDD (golden data) &rarr; ENTREGA VERIFICADA (AUC 0.8318 honesto).</p>"
            "<ul><li>Revela los tres KPI con los fragmentos: 1&rarr;2 el doc se dimensiona por riesgo; 2&rarr;3 la auditoría es zero-context; "
            "3&rarr;4 la evidencia final es la métrica honesta.</li>"
            "<li>Frase de transición: 'esta progresión es exactamente lo que vamos a ejecutar en el terminal ahora mismo'.</li></ul>"
        ),
    },
    "06-practica-1": {
        "time": "min 21–25 · Bloque 1 (0–25')",
        "body": (
            "<p><strong>[21:00] ¡Cambio al terminal! Práctica 1 (4').</strong> Badge encendido: EJERCICIO EN VIVO.</p>"
            "<ol><li><strong>cd demos/sdd-churn-leakage</strong> y <strong>python src/train_baseline.py</strong>.</li>"
            "<li>Celebra el <strong>0.9593</strong> en pantalla; pregunta: '¿lo subiríamos a producción?' — alguien dirá que sí.</li>"
            "<li>Señala las dos líneas culpables: la columna <strong>post_churn_cancellation_days</strong> y el "
            "<strong>StandardScaler().fit_transform</strong> antes del split (y el split aleatorio como tercera fuga).</li>"
            "<li>Muestra el veredicto honesto: <strong>0.8318</strong>, brecha <strong>0.1275</strong>, con los 1,203 clientes del CSV (seed=42).</li></ol>"
            "<p><strong>[24:30] Cierra el bloque:</strong> 'el 0.9593 no es un bug del modelo: es un bug del proceso'.</p>"
        ),
    },
    "07-divider-b2": {
        "time": "min 25–27 · Bloque 2 (25–50')",
        "body": (
            "<p><strong>[25:00] Transición al Bloque 2.</strong> Pausa corta de preguntas (2'). "
            "Anuncia: 'ahora construimos el contrato: qué, cómo y dónde, y de ahí nacen fases y tareas'.</p>"
            "<ul><li>Check de reloj: si vas pasado de 27', recorta la demo del pipeline (slide 10), no la spec (slide 8).</li></ul>"
        ),
    },
    "08-la-spec": {
        "time": "min 27–33 · Bloque 2 (25–50')",
        "body": (
            "<p><strong>[27:00] Los tres documentos (4').</strong> Cada doc responde UNA pregunta: ¿QUÉ? (description), "
            "¿CÓMO fluye el dato? (architecture con ADRs), ¿DÓNDE vive? (diseno_db con ER y diccionario).</p>"
            "<p><strong>[31:00] Regla de oro (2').</strong> Los docs son la fuente de verdad: si el código diverge, se corrige uno de los dos "
            "— nunca conviven. Anécdota: el 0.9593 nació de un pipeline sin spec que exigía features disponibles al snapshot.</p>"
        ),
    },
    "09-plan-tareas": {
        "time": "min 33–39 · Bloque 2 (25–50')",
        "body": (
            "<p><strong>[33:00] Plan maestro (3').</strong> Fases &rarr; Sub fases &rarr; Tareas con DoD. Muestra el árbol: "
            "cada tarea es unit-testable y cerrable en una sesión.</p>"
            "<p><strong>[36:00] Tablero tareas.md (3').</strong> El [X] es un certificado, no un deseo: solo se marca cuando "
            "<strong>verificar-dod</strong> pasa en verde. Guarda este punto: vuelve en el Bloque 4.</p>"
        ),
    },
    "10-project-suite": {
        "time": "min 39–44 · Bloque 2 (25–50')",
        "body": (
            "<p><strong>[39:00] Pipeline animado (5').</strong> Recorre los nodos con el punto: especificar &rarr; planificar &rarr; "
            "construir (1 subagente por tarea, standards por lenguaje) &rarr; testear &rarr; verificar-dod.</p>"
            "<ul><li>Señala el bucle ámbar: DoD en rojo &rarr; vuelve a construir. Ese bucle es el seguro de calidad.</li>"
            "<li>Subraya la banda superior: auditar-coherencia + bitácora + semantic-commit cierran cada cambio.</li>"
            "<li>[43:00] Micro-ejercicio: 'piensen en su próximo cambio: ¿en qué nodo del pipeline está hoy?'</li></ul>"
        ),
    },
    "11-odd": {
        "time": "min 44–47 · Bloque 2 (25–50')",
        "body": (
            "<p><strong>[44:00] SDD &rarr; ODD (3').</strong> La tabla es la clave: reversible &rarr; comentario ligero; "
            "semi-reversible &rarr; spec + test; irreversible (DB, API pública, seguridad) &rarr; ADR + spec + auditoría.</p>"
            "<ul><li>Explica el salto: el SDD rígido documenta todo al máximo y muere por burocracia; ODD dimensiona el doc según la irreversibilidad.</li>"
            "<li><strong>Antecedente (cítalo con nombre):</strong> ODD la propuso <strong>Alan Buscaglia</strong> (<em>Gentleman Programming</em>) "
            "en su ecosistema <strong>Gentle-AI</strong>, que retiró el SDD clásico por burocrático y sumó <strong>Engram</strong> "
            "(memoria persistente SQLite + FTS5). project-suite hereda esa flexibilidad y le añade auditoría EGM + evidencia EDD.</li>"
            "<li>Pregunta para la sala: 'la tabla de precios de su producto, ¿qué fila de la tabla merece?'</li>"
            "<li>Cierra con el gancho: 'pero ¿quién verifica esta flexibilidad sin memoria de contexto? EGM, ya'.</li></ul>"
        ),
    },
    "12-egm-edd": {
        "time": "min 47–50 · Bloque 2 (25–50')",
        "body": (
            "<p><strong>[47:00] ODD &rarr; EGM (2').</strong> La flexibilidad necesita verificación zero-context: "
            "EGM audita con tests, DoD y docs contra el código — la evidencia no depende del equipo ni de la memoria de sesión. "
            "Contrasta el enfoque: Gentle-AI resuelve la memoria con <strong>Engram</strong> (SQLite + FTS5 persistente); "
            "EGM prefiere la auditoría zero-context, que funciona aunque la memoria falte.</p>"
            "<p><strong>[49:00] EGM &rarr; EDD (1').</strong> En Data Science la evidencia final es la métrica: Golden Data determinista (seed=42) "
            "+ split temporal. EDD registra 0.8318 con procedencia, no un 0.9593 recitado.</p>"
            "<ul><li>Frase puente: 'progresión completa: SDD (qué) &rarr; ODD (cuánto doc) &rarr; EGM (quién verifica) &rarr; EDD (qué evidencia)'.</li>"
            "<li>Check de reloj del bloque: debes cerrar en 50'.</li></ul>"
        ),
    },
    "13-divider-b3": {
        "time": "min 50–52 · Bloque 3 (50–75')",
        "body": (
            "<p><strong>[50:00] Transición a los casos reales.</strong> Pausa de preguntas (2'). "
            "Presenta los DOS casos en paralelo: <strong>AgroVision</strong> (Web: gateway FastAPI :8000 + Astro 5, "
            "Supabase PostGIS BYOK, 5 índices Sentinel-2, HF Spaces, 16 fases) y el laboratorio "
            "demos/sdd-churn-leakage (1,203 clientes, AUC 0.9593 vs 0.8318)."
        ),
    },
    "14-el-caso": {
        "time": "min 52–56 · Bloque 3 (50–75')",
        "body": (
            "<p><strong>[52:00] Los dos casos en paralelo (4').</strong> Columna izquierda: el laboratorio DS — "
            "mini-proyecto reproducible, Golden Data <strong>data/churn_events.csv</strong> (seed=42), contrato en "
            "<strong>tests/test_demo_seed.py</strong>, tensión 0.9593 vs 0.8318 (brecha 0.1275).</p>"
            "<ul><li>Columna derecha: <strong>AgroVision</strong> — gateway <strong>FastAPI :8000</strong> que sirve la SPA "
            "<strong>Astro 5 + Tailwind 4</strong>, Supabase <strong>PostGIS</strong> con credenciales efímeras BYOK "
            "(<strong>X-User-*</strong>), <strong>5 índices</strong> Sentinel-2, deploy en <strong>Hugging Face Spaces</strong> y "
            "<strong>16 fases</strong> en plan_agrovision.md.</li>"
            "<li>Recorre la fila de pills del flujo: especificar &rarr; planificar &rarr; construir (goldfish) &rarr; testear "
            "(Playwright / Golden Data) &rarr; verificar-dod &rarr; auditar-coherencia — el MISMO flujo en ambos dominios.</li>"
            "<li>Estándares por dominio: Web &rarr; backend-standards + astro-standards; DS &rarr; python-standards + EDD.</li></ul>"
        ),
    },
    "15-elefante-goldfish": {
        "time": "min 56–62 · Bloque 3 (50–75')",
        "body": (
            "<p><strong>[56:00] Diagrama animado (6').</strong> Elefante = el equipo con contexto rico (negocio, estacionalidad, contratos). "
            "Goldfish = el asistente con zero-context: solo ve filas del CSV y no recuerda la sesión anterior.</p>"
            "<ul><li>El puente entre ambos es la spec: 'lo que el elefante da por obvio, la goldfish lo lee del doc'.</li>"
            "<li>Ejemplo concreto: 'post_churn_cancellation_days parece innocua; el contexto del negocio la vuelve imposible a tiempo'.</li></ul>"
        ),
    },
    "16-la-fuga": {
        "time": "min 62–68 · Bloque 3 (50–75')",
        "body": (
            "<p><strong>[62:00] El código culpable (3').</strong> Lee las líneas marcadas en carmesí: "
            "<strong>FEATURES_FUGA</strong> suma la columna post-churn, el <strong>StandardScaler</strong> se fitea antes del split "
            "y el <strong>train_test_split</strong> es aleatorio: tres fugas en seis líneas.</p>"
            "<p><strong>[65:00] La lectura SDD (3').</strong> La spec ya lo prohibía: solo variables disponibles en el instante del "
            "snapshot_date. El chequeo ODD: '¿existiría esta feature el día que el modelo corre en producción?' Si no: fuga.</p>"
            "<p><strong>[66:30] Paralelo Web (1.5').</strong> La tarea pendiente <strong>T10.4.1</strong> de AgroVision: "
            "<strong>allowlist anti-SSRF</strong> para <strong>X-User-Supabase-Url</strong> y <strong>límite geométrico del polígono "
            "en servidor</strong>. El vibe pondría un regex en Astro y rompería prod o dev; project-suite la resuelve con "
            "backend-standards + astro-standards y E2E Playwright.</p>"
        ),
    },
    "17-honesto": {
        "time": "min 68–71 · Bloque 3 (50–75')",
        "body": (
            "<p><strong>[68:00] Comparativa animada (3').</strong> Barra carmesí 0.9593 (crece) vs barra esmeralda 0.8318 "
            "(crece con retardo) y la zona honesta marcada.</p>"
            "<ul><li>Frase central: 'bajar de 0.9593 a 0.8318 no fue pérdida: fue el momento en que el número dijo la verdad'.</li>"
            "<li>Deja pausa: la sala necesita asimilar que la brecha 0.1275 es la mentira cuantificada.</li></ul>"
        ),
    },
    "18-chart-caso": {
        "time": "min 71–75 · Bloque 3 (50–75')",
        "body": (
            "<p><strong>[71:00] Gráfica del caso (4').</strong> Dos barras: con fuga 0.9593 y honesto 0.8318 (1,203 clientes, seed=42). "
            "Los mismos valores que verán en el terminal de la práctica 1.</p>"
            "<ul><li>Lectura gerencial: el 0.9593 no predice churn, lo recuerda; EDD registró 0.8318 con procedencia.</li>"
            "<li>Lectura técnica: el baseline honesto (reg-log + split temporal) es la referencia; el contrato del laboratorio "
            "exige leaky_auc &ge; 0.93 &gt; honest_auc y lo verifica test_demo_seed.py.</li>"
            "<li>Cierra el bloque exactamente a los 75'.</li></ul>"
        ),
    },
    "19-divider-b4": {
        "time": "min 75–77 · Bloque 4 (75–100')",
        "body": (
            "<p><strong>[75:00] Transición al Bloque 4.</strong> Pausa de preguntas (2'). "
            "Tesis del bloque: 'el rework no avisado es la deuda más cara; la verificación planificada es la inversión más barata'. "
            "Anuncia las dos prácticas en terminal de este bloque (partes A y B).</p>"
        ),
    },
    "20-chart-coste": {
        "time": "min 77–82 · Bloque 4 (75–100')",
        "body": (
            "<p><strong>[77:00] Gráfica del coste (5').</strong> Horas acumuladas por semana: Vibe llega a 31h en la semana 6; "
            "SDD+ODD a 11h. El cruce de curvas ocurre hacia la semana 3.</p>"
            "<ul><li>Explica el arranque: SDD 'paga más' en semanas 1–2 (spec + tests) — ese es el punto que los gerentes deben ver.</li>"
            "<li>Pregunta: '¿dónde está la curva de su proyecto actual?' Deja 1' de discusión.</li></ul>"
        ),
    },
    "21-practica-2": {
        "time": "min 82–88 · Bloque 4 (75–100') · Parte A",
        "body": (
            "<p><strong>[82:00] ¡Cambio al terminal! Práctica 2 — Parte A (6').</strong> Badge encendido: EJERCICIO EN VIVO.</p>"
            "<ol><li><strong>cat AGENTS.md</strong>: la Constitución SDD del mini-proyecto (fuga temporal prohibida, Golden Data obligatorio).</li>"
            "<li><strong>/project-suite:especificar</strong>: contrato Pydantic + Golden Data en la spec; la regla anti-fuga se escribe ANTES del código.</li>"
            "<li><strong>/project-suite:planificar</strong>: Fases &rarr; Tareas con DoD, modo estricto.</li>"
            "<li><strong>/project-suite:auditar-coherencia</strong> en solo lectura: docs &harr; código, sin editar nada.</li>"
            "<li><strong>bitacora</strong>: registra el incidente de la fuga en docs/logs/log.md.</li></ol>"
            "<p>Enfatiza: esta parte NO construye nada — es auditoría y contrato puro (ODD + bitácora + Constitución).</p>"
        ),
    },
    "22-practica-3": {
        "time": "min 88–94 · Bloque 4 (75–100') · Parte B",
        "body": (
            "<p><strong>[88:00] ¡Cambio al terminal! Práctica 3 — Parte B (6').</strong> Ejecución aislada EGM.</p>"
            "<ol><li><strong>/project-suite:construir</strong>: 1 subagente por tarea con python-standards.</li>"
            "<li><strong>/project-suite:testear</strong>: unitarios + simulación de usuario.</li>"
            "<li><strong>python -m pytest tests -v</strong>: el Golden Data verifica leaky 0.9593 &gt; honest 0.8318 y brecha 0.1275.</li>"
            "<li><strong>/project-suite:verificar-dod</strong>: solo con verde se marca [X].</li>"
            "<li><strong>/semantic-commit</strong>: cierre ordenado, nunca push manual.</li></ol>"
            "<p>Contraste con la práctica 1: mismo dataset, pero ahora el proceso es verificable de punta a punta.</p>"
        ),
    },
    "23-dod": {
        "time": "min 94–97 · Bloque 4 (75–100')",
        "body": (
            "<p><strong>[94:00] El gate DoD (3').</strong> Tests en verde, cobertura vs umbral, lint limpio, cambios de DB/env documentados. "
            "Conecta con la práctica 3: verificar-dod fue el paso 4 del flujo que acaban de ver.</p>"
            "<p><strong>[96:00] El registro (1').</strong> Muestra el flujo: DoD OK &rarr; [X] marcado &rarr; sync del tablero. "
            "Martilla: 'un checkbox marcado sin DoD en verde es mentira documentada'.</p>"
        ),
    },
    "24-coherencia-bitacora": {
        "time": "min 97–100 · Bloque 4 (75–100')",
        "body": (
            "<p><strong>[97:00] auditar-coherencia (2').</strong> Compara docs vs código real y rankea divergencias: "
            "el drift se detecta en minutos, no en producción (ya lo ejecutaron read-only en la práctica 2).</p>"
            "<p><strong>[99:00] bitácora (1').</strong> Cierra el bloque registrando el incidente del laboratorio en formato forense: "
            "<strong>síntoma</strong> (AUC 0.9593), <strong>causa raíz</strong> (post_churn_cancellation_days + scaler antes del split + split aleatorio), "
            "<strong>lección</strong> (chequeo ODD de disponibilidad temporal en toda feature). En <strong>AgroVision</strong>, "
            "auditar-coherencia mantiene <strong>architecture_agrovision.md</strong> fiel al gateway FastAPI + Astro: "
            "la misma disciplina anti-drift, otro dominio.</p>"
        ),
    },
    "25-checklist": {
        "time": "min 100–110 · Bloque 5 (100–120')",
        "body": (
            "<p><strong>[100:00] Checklist accionable (6').</strong> 5 pasos: elegir el cambio &rarr; escribir la spec (¿qué/cómo/dónde?) &rarr; "
            "aplicar ODD &rarr; planificar tareas con DoD &rarr; verificar y registrar.</p>"
            "<ul><li>Métrica de la semana: 0 cambios de código sin spec en lo irreversible.</li>"
            "<li>Micro-compromiso: 'escribe hoy la spec de tu próximo cambio; mañana construyes con ella'.</li></ul>"
        ),
    },
    "26-recursos": {
        "time": "min 110–115 · Bloque 5 (100–120')",
        "body": (
            "<p><strong>[110:00] Recursos (5').</strong> Repo completo y comandos project-suite. "
            "Anima a abrir el repo durante la pausa final: la spec de este mismo taller vive en docs/.</p>"
            "<ul><li>Señala demos/sdd-churn-leakage para quien quiera reproducir las tres prácticas en casa.</li></ul>"
        ),
    },
    "27-cierre": {
        "time": "min 115–120 · Bloque 5 (100–120')",
        "body": (
            "<p><strong>[115:00] Cierre y Q&amp;A (5').</strong> Frase final: 'la especificación es el contrato; la verificación, la inversión; "
            "la evidencia, el informe final'.</p>"
            "<ul><li>Recoge 2–3 preguntas; si no surgen, lanza tú la de siempre: '¿qué decisión irreversible tomaste esta semana sin spec?'</li>"
            "<li>Recuerda los dos casos: AgroVision (Web) y el laboratorio de churn (Data Science) — mismo flujo, estándares distintos.</li>"
            "<li>Comparte contacto y repo. Fin a los 120' exactos.</li></ul>"
        ),
    },
}
