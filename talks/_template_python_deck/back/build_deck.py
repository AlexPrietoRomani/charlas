"""
Archivo: talks/_template_python_deck/back/build_deck.py
Fecha de modificación: 15/11/2026
Autor: Alex Prieto <alexprieto1997@gmail.com>

Descripción:
Generador base de presentaciones single-file para el motor `python-deck`.
Compila un deck interactivo mínimo de 3 diapositivas con Chart.js offline,
drawer de notas del orador `[N]`, navegación por teclado y marca personal
de Alex Prieto Romani sin dependencias ni logos de terceros.

Acciones Principales:
    - Lee metadatos de `talk.json` si está disponible en la carpeta de la charla.
    - Resuelve el bundle compartido `shared/python_deck/assets/chart.umd.min.js`.
    - Ensambla un HTML autónomo con 3 diapositivas, gráfico Chart.js y notas `[N]`.
    - Escribe `index.html` dentro de `output_dir` o en la raíz de la charla.

Estructura Interna:
    - `_resolve_chartjs_path`: Localiza `chart.umd.min.js` en el repositorio.
    - `_load_chartjs_bundle`: Lee el código JavaScript offline de Chart.js.
    - `_load_talk_metadata`: Carga título, subtítulo, evento y fecha de `talk.json`.
    - `_build_sample_data`: Construye el payload de datos de ejemplo para Chart.js.
    - `_build_speaker_notes`: Define el guion del orador por número de diapositiva.
    - `_get_deck_css`: Genera la hoja de estilos oscura característica de `python-deck`.
    - `_build_slides_html`: Renderiza las 3 diapositivas base del template.
    - `_render_html_document`: Compila el documento HTML final autocontenido.
    - `build_deck`: Ejecuta la compilación y retorna la ruta a `index.html`.
    - `main`: Punto de entrada CLI con soporte `--output-dir`.

Entradas / Dependencias:
    - `talk.json` de la charla (opcional; usa valores por defecto si falta).
    - `shared/python_deck/assets/chart.umd.min.js`.

Salidas / Efectos:
    - Escribe `index.html` en el directorio destino especificado.

Ejecución:
    python talks/_template_python_deck/back/build_deck.py [--output-dir RUTA]

Ejemplo de Uso:
    python talks/2027-mi-charla/back/build_deck.py --output-dir _site/2027-mi-charla

Argumentos:
    - --output-dir: Path | None - Directorio destino para el archivo `index.html`.
"""

import argparse
import html
import json
from pathlib import Path
from typing import Any

BASE_DIR: Path = Path(__file__).resolve().parent.parent
REPO_ROOT: Path = BASE_DIR.parent.parent
CHARTJS_RELATIVE_PATH: Path = Path("shared") / "python_deck" / "assets" / "chart.umd.min.js"
DEFAULT_OUTPUT_FILENAME: str = "index.html"
TOTAL_SLIDES: int = 3

DEFAULT_METADATA: dict[str, str] = {
    "title": "Título de tu nueva charla (Python Deck)",
    "subtitle": "Subtítulo conciso con el enfoque técnico, datos reales y aprendizaje clave",
    "event": "Conferencia o Meetup 2027",
    "date": "2027-01-15",
}


def _resolve_chartjs_path() -> Path:
    """
    Localiza `chart.umd.min.js` compartido en el monorepo o desde el directorio actual.

    Returns:
        Path: Ruta existente al archivo `chart.umd.min.js`.

    Raises:
        FileNotFoundError: Si no se encuentra el bundle compartido en ninguna ruta candidata.
    """
    candidates: list[Path] = [
        REPO_ROOT / CHARTJS_RELATIVE_PATH,
        Path.cwd() / CHARTJS_RELATIVE_PATH,
    ]
    # Permite ejecutar copias temporales del template desde cualquier subcarpeta del repo.
    candidates.extend(parent / CHARTJS_RELATIVE_PATH for parent in Path.cwd().resolve().parents)

    for candidate in candidates:
        if candidate.is_file():
            return candidate

    raise FileNotFoundError(
        f"No se encontró el bundle offline de Chart.js en '{CHARTJS_RELATIVE_PATH}'."
    )


def _load_chartjs_bundle() -> str:
    """
    Lee el código JavaScript offline de Chart.js para embeberlo en el deck.

    Returns:
        str: Contenido completo de `chart.umd.min.js`.
    """
    chartjs_path = _resolve_chartjs_path()
    return chartjs_path.read_text(encoding="utf-8")


def _load_talk_metadata() -> dict[str, str]:
    """
    Carga metadatos básicos desde `talk.json` aplicando valores por defecto seguros.

    Returns:
        dict[str, str]: Diccionario con claves `title`, `subtitle`, `event` y `date`.
    """
    metadata = dict(DEFAULT_METADATA)
    manifest_path = BASE_DIR / "talk.json"
    if not manifest_path.is_file():
        return metadata

    payload = json.loads(manifest_path.read_text(encoding="utf-8"))
    if isinstance(payload, dict):
        for key in ("title", "subtitle", "event", "date"):
            value = payload.get(key)
            if isinstance(value, str) and value.strip():
                metadata[key] = value.strip()
    return metadata


def _build_sample_data() -> dict[str, Any]:
    """
    Genera datos de ejemplo serializables para alimentar el gráfico Chart.js.

    Returns:
        dict[str, Any]: Diccionario con etiquetas, métricas comparativas y unidad.
    """
    return {
        "labels": ["Baseline", "Regresión", "Gradient Boosting", "Modelo Propuesto"],
        "baseline_error": [18.4, 14.2, 10.6, 8.9],
        "target_error": [15.0, 12.5, 9.8, 7.4],
        "unit": "RMSE (%)",
    }


def _build_speaker_notes() -> dict[int, str]:
    """
    Define las notas del orador por número de diapositiva para el drawer `[N]`.

    Returns:
        dict[int, str]: Mapeo de índice de diapositiva (1..3) a texto HTML de guion.
    """
    return {
        1: (
            "<strong>Apertura (1 min):</strong> Presenta el problema central de la charla "
            "y contextualiza por qué los datos reales exigen validar supuestos antes de modelar."
        ),
        2: (
            "<strong>Evidencia interactiva (2 min):</strong> Usa el gráfico Chart.js para "
            "comparar la línea base contra el enfoque propuesto y destaca la reducción de error."
        ),
        3: (
            "<strong>Cierre ejecutivo (1 min):</strong> Resume las tres decisiones prácticas "
            "que la audiencia puede aplicar mañana y abre espacio para preguntas."
        ),
    }


def _get_deck_css() -> str:
    """
    Retorna la hoja de estilos oscura propia del motor `python-deck`.

    Returns:
        str: Reglas CSS completas para layout, tarjetas, drawer `[N]` y barra inferior.
    """
    return """
  :root {
    --bg-dark: #03050F;
    --bg-panel: rgba(11, 22, 56, 0.88);
    --bg-sub: rgba(17, 29, 66, 0.78);
    --accent-cyan: #12C8FC;
    --accent-blue: #1E7BFF;
    --accent-purple: #9B5CFF;
    --accent-emerald: #2EE6A6;
    --accent-amber: #FFC857;
    --text-main: #FFFFFF;
    --text-sub: #CBD5E1;
    --text-faint: #94A3B8;
    --line-border: rgba(18, 200, 252, 0.28);
    --footer-h: 56px;
  }

  * { box-sizing: border-box; margin: 0; padding: 0; }

  body {
    font-family: "IBM Plex Sans", -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
    background: radial-gradient(circle at 85% 15%, rgba(155, 92, 255, 0.16), transparent 42%),
                radial-gradient(circle at 15% 85%, rgba(18, 200, 252, 0.14), transparent 40%),
                var(--bg-dark);
    color: var(--text-main);
    width: 100vw;
    height: 100vh;
    overflow: hidden;
    display: flex;
    flex-direction: column;
  }

  .mono { font-family: "IBM Plex Mono", ui-monospace, SFMono-Regular, Menlo, monospace; }

  .progress-container {
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    height: 4px;
    background: rgba(11, 22, 56, 0.9);
    z-index: 100;
  }

  .progress-bar {
    height: 100%;
    width: 33.33%;
    background: linear-gradient(90deg, var(--accent-cyan), var(--accent-blue), var(--accent-purple));
    transition: width 0.25s ease;
  }

  .deck-container {
    width: 100vw;
    height: calc(100vh - var(--footer-h));
    padding: clamp(20px, 3vh, 40px) clamp(24px, 4vw, 64px);
    display: flex;
    align-items: center;
    justify-content: center;
    position: relative;
  }

  .slide {
    display: none;
    width: 100%;
    max-width: 1180px;
    height: 100%;
    flex-direction: column;
    justify-content: center;
    gap: 20px;
    animation: fadeIn 0.22s ease-out;
  }

  .slide.active { display: flex; }

  @keyframes fadeIn {
    from { opacity: 0; transform: translateY(6px); }
    to { opacity: 1; transform: translateY(0); }
  }

  .badge {
    display: inline-flex;
    align-items: center;
    width: fit-content;
    padding: 6px 14px;
    border-radius: 999px;
    border: 1px solid var(--line-border);
    background: rgba(18, 200, 252, 0.12);
    color: var(--accent-cyan);
    font-size: 12px;
    font-weight: 600;
    letter-spacing: 0.06em;
    text-transform: uppercase;
  }

  h1 {
    font-size: clamp(2rem, 4.2vw, 3.3rem);
    line-height: 1.12;
    font-weight: 700;
    letter-spacing: -0.02em;
  }

  h2 {
    font-size: clamp(1.5rem, 2.8vw, 2.25rem);
    line-height: 1.2;
    font-weight: 700;
  }

  .subtitle {
    font-size: clamp(1rem, 1.5vw, 1.28rem);
    color: var(--text-sub);
    max-width: 78ch;
    line-height: 1.5;
  }

  .panel {
    background: var(--bg-panel);
    border: 1px solid var(--line-border);
    border-radius: 16px;
    padding: 22px 24px;
  }

  .grid-2 {
    display: grid;
    grid-template-columns: 1.6fr 1fr;
    gap: 20px;
    min-height: 360px;
    align-items: stretch;
  }

  .grid-3 {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 16px;
  }

  .chart-box {
    position: relative;
    height: 320px;
    width: 100%;
  }

  .kpi-card {
    background: var(--bg-sub);
    border: 1px solid rgba(148, 163, 184, 0.22);
    border-radius: 12px;
    padding: 16px 18px;
    display: flex;
    flex-direction: column;
    gap: 8px;
  }

  .kpi-value {
    font-size: 1.9rem;
    font-weight: 700;
    color: var(--accent-emerald);
  }

  .deck-footer {
    height: var(--footer-h);
    padding: 0 24px;
    border-top: 1px solid var(--line-border);
    background: rgba(3, 5, 15, 0.94);
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 12px;
    z-index: 40;
  }

  .footer-left, .footer-actions {
    display: flex;
    align-items: center;
    gap: 10px;
  }

  .divider {
    width: 1px;
    height: 18px;
    background: rgba(18, 200, 252, 0.28);
  }

  .nav-btn {
    background: rgba(17, 29, 66, 0.85);
    color: var(--text-main);
    border: 1px solid var(--line-border);
    border-radius: 8px;
    padding: 6px 12px;
    font-size: 12px;
    font-weight: 600;
    cursor: pointer;
    transition: border-color 0.15s ease, background 0.15s ease;
  }

  .nav-btn:hover {
    border-color: var(--accent-cyan);
    background: rgba(18, 200, 252, 0.16);
  }

  .speaker-drawer {
    position: fixed;
    left: 24px;
    right: 24px;
    bottom: calc(var(--footer-h) + 12px);
    max-width: 820px;
    margin: 0 auto;
    background: rgba(7, 13, 35, 0.97);
    border: 1px solid var(--accent-cyan);
    border-radius: 14px;
    padding: 16px 20px;
    box-shadow: 0 18px 48px rgba(0, 0, 0, 0.55);
    transform: translateY(20px);
    opacity: 0;
    pointer-events: none;
    transition: opacity 0.2s ease, transform 0.2s ease;
    z-index: 60;
  }

  .speaker-drawer.open {
    transform: translateY(0);
    opacity: 1;
    pointer-events: auto;
  }

  .speaker-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 10px;
    color: var(--accent-cyan);
    font-size: 12px;
    font-weight: 700;
  }

  .speaker-body {
    color: var(--text-sub);
    font-size: 14px;
    line-height: 1.55;
  }

  @media (max-width: 900px) {
    .grid-2, .grid-3 { grid-template-columns: 1fr; }
    .chart-box { height: 240px; }
  }
"""


def _build_slides_html(metadata: dict[str, str]) -> str:
    """
    Construye el HTML de las 3 diapositivas de demostración de la plantilla.

    Args:
        metadata (dict[str, str]): Metadatos escapados de la charla actual.

    Returns:
        str: Fragmento HTML con los 3 bloques `<section class="slide">`.
    """
    title = html.escape(metadata["title"])
    subtitle = html.escape(metadata["subtitle"])
    event = html.escape(metadata["event"])
    talk_date = html.escape(metadata["date"])

    return f"""
  <section class="slide active" data-index="1" data-act="Apertura · Portada" data-time="1.0 min">
    <span class="badge mono">Python-Deck · Plantilla Base</span>
    <h1>{title}</h1>
    <p class="subtitle">{subtitle}</p>
    <div class="panel" style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:12px;">
      <div>
        <div style="font-weight:700; font-size:1.05rem;">Alex Prieto Romani</div>
        <div class="mono" style="color:var(--text-faint); font-size:13px;">Data Science · Forecasting · Ingeniería de ML</div>
      </div>
      <div class="mono" style="color:var(--accent-cyan); font-size:13px;">{event} · {talk_date}</div>
    </div>
  </section>

  <section class="slide" data-index="2" data-act="Evidencia · Gráfico Chart.js" data-time="2.0 min">
    <span class="badge mono">Visualización Offline · Chart.js</span>
    <h2>Comparativa cuantitativa embebida en el deck</h2>
    <div class="grid-2">
      <div class="panel">
        <div class="chart-box">
          <canvas id="templateChart" aria-label="Gráfico comparativo de modelos"></canvas>
        </div>
      </div>
      <div style="display:flex; flex-direction:column; gap:12px;">
        <div class="kpi-card">
          <span class="mono" style="font-size:12px; color:var(--text-faint);">REDUCCIÓN DE ERROR</span>
          <span class="kpi-value">-51.6%</span>
          <span style="font-size:13px; color:var(--text-sub);">Comparación directa frente al baseline inicial en datos de ejemplo.</span>
        </div>
        <div class="kpi-card">
          <span class="mono" style="font-size:12px; color:var(--text-faint);">EJECUCIÓN OFFLINE</span>
          <span class="kpi-value" style="color:var(--accent-cyan);">100%</span>
          <span style="font-size:13px; color:var(--text-sub);">Chart.js inyectado desde shared/python_deck/assets sin CDN externo.</span>
        </div>
      </div>
    </div>
  </section>

  <section class="slide" data-index="3" data-act="Cierre · Conclusiones" data-time="1.0 min">
    <span class="badge mono">Resumen y Siguientes Pasos</span>
    <h2>Tres ideas clave para recordar</h2>
    <div class="grid-3">
      <div class="kpi-card">
        <span class="mono" style="color:var(--accent-cyan); font-size:12px;">01 · MANIFIESTO</span>
        <strong style="font-size:1.05rem;">Contrato `talk.json`</strong>
        <p style="font-size:14px; color:var(--text-sub);">Define slug, fecha, etiquetas y portada para integrarse al Hub.</p>
      </div>
      <div class="kpi-card">
        <span class="mono" style="color:var(--accent-purple); font-size:12px;">02 · DATOS REALES</span>
        <strong style="font-size:1.05rem;">Payload `DECK_DATA`</strong>
        <p style="font-size:14px; color:var(--text-sub);">Alimenta gráficos interactivos reproducibles directamente desde Python.</p>
      </div>
      <div class="kpi-card">
        <span class="mono" style="color:var(--accent-emerald); font-size:12px;">03 · PRESENTACIÓN</span>
        <strong style="font-size:1.05rem;">Notas `[N]` y `[F]`</strong>
        <p style="font-size:14px; color:var(--text-sub);">Navega con flechas, abre notas del orador y proyecta en pantalla completa.</p>
      </div>
    </div>
    <div class="panel" style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:10px;">
      <span style="font-weight:600;">Alex Prieto Romani</span>
      <span class="mono" style="color:var(--accent-cyan); font-size:13px;">github.com/AlexPrietoRomani/charlas</span>
    </div>
  </section>
"""


def _render_html_document(
    *,
    metadata: dict[str, str],
    data_json: str,
    notes_json: str,
    css_content: str,
    slides_html: str,
    chartjs_code: str,
) -> str:
    """
    Ensambla el documento HTML completo del deck con Chart.js embebido y controles.

    Args:
        metadata (dict[str, str]): Metadatos de título y contexto de la charla.
        data_json (str): Cadena JSON asignada a `window.DECK_DATA`.
        notes_json (str): Cadena JSON con notas indexadas por número de diapositiva.
        css_content (str): Hoja de estilos CSS del deck.
        slides_html (str): Markup HTML de las diapositivas.
        chartjs_code (str): Código JavaScript offline de Chart.js.

    Returns:
        str: Documento HTML5 listo para guardar como `index.html`.
    """
    page_title = html.escape(metadata["title"])

    return f"""<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{page_title} · Alex Prieto Romani</title>
<link rel="icon" href="data:,">
<script>{chartjs_code}</script>
<script>
  if (typeof Chart !== "undefined") {{
    Chart.defaults.color = "#CBD5E1";
    Chart.defaults.borderColor = "rgba(148, 163, 184, 0.16)";
  }}
</script>
<style>
{css_content}
</style>
</head>
<body>

<div class="progress-container">
  <div class="progress-bar" id="progressBar"></div>
</div>

<main class="deck-container">
{slides_html}
</main>

<footer class="deck-footer">
  <div class="footer-left">
    <span style="font-weight:700; font-size:13px;">Alex Prieto Romani</span>
    <div class="divider"></div>
    <span class="mono" id="slideIndicator" style="font-weight:700; font-size:13px; color:#12C8FC;">01 / 0{TOTAL_SLIDES}</span>
    <span class="mono" id="actIndicator" style="font-size:12px; color:var(--text-faint);">Apertura · Portada</span>
  </div>

  <div class="footer-actions">
    <button class="nav-btn" type="button" onclick="toggleSpeakerNotes()" title="Notas del orador (N)">[N] Notas</button>
    <button class="nav-btn" type="button" onclick="toggleFullscreen()" title="Pantalla completa (F)">[F] Fullscreen</button>
    <button class="nav-btn" type="button" onclick="prevSlide()" title="Diapositiva anterior">&larr; Prev</button>
    <button class="nav-btn" type="button" onclick="nextSlide()" title="Siguiente diapositiva">Next &rarr;</button>
  </div>
</footer>

<aside class="speaker-drawer" id="speakerDrawer" aria-hidden="true">
  <div class="speaker-header">
    <span class="mono">NOTAS DEL ORADOR · <span id="speakerTimer">1.0 min</span></span>
    <button class="nav-btn" type="button" onclick="toggleSpeakerNotes()">Cerrar [N]</button>
  </div>
  <div class="speaker-body" id="speakerNotesText"></div>
</aside>

<script>
  window.DECK_DATA = {data_json};
  const notesBySlide = {notes_json};
  const totalSlides = {TOTAL_SLIDES};
  let currentSlide = 1;
  let chartInstance = null;

  function renderChartIfNeeded(index) {{
    if (index !== 2 || chartInstance !== null || typeof Chart === "undefined") return;
    const canvas = document.getElementById("templateChart");
    if (!canvas) return;
    const payload = window.DECK_DATA;
    chartInstance = new Chart(canvas.getContext("2d"), {{
      type: "bar",
      data: {{
        labels: payload.labels,
        datasets: [
          {{
            label: "Serie Base (" + payload.unit + ")",
            data: payload.baseline_error,
            backgroundColor: "rgba(30, 123, 255, 0.72)",
            borderColor: "#12C8FC",
            borderWidth: 1.5,
            borderRadius: 6
          }},
          {{
            label: "Ajuste Validado (" + payload.unit + ")",
            data: payload.target_error,
            backgroundColor: "rgba(46, 230, 166, 0.75)",
            borderColor: "#2EE6A6",
            borderWidth: 1.5,
            borderRadius: 6
          }}
        ]
      }},
      options: {{
        responsive: true,
        maintainAspectRatio: false,
        plugins: {{
          legend: {{ position: "top" }}
        }},
        scales: {{
          y: {{ beginAtZero: true }}
        }}
      }}
    }});
  }}

  function updateSlide(index) {{
    const bounded = Math.max(1, Math.min(totalSlides, index));
    document.querySelectorAll(".slide").forEach((el) => el.classList.remove("active"));
    const target = document.querySelector('.slide[data-index="' + bounded + '"]');
    if (!target) return;

    target.classList.add("active");
    currentSlide = bounded;
    document.getElementById("slideIndicator").textContent =
      String(bounded).padStart(2, "0") + " / " + String(totalSlides).padStart(2, "0");
    document.getElementById("actIndicator").textContent = target.getAttribute("data-act") || "";
    document.getElementById("progressBar").style.width = ((bounded / totalSlides) * 100) + "%";
    document.getElementById("speakerTimer").textContent = target.getAttribute("data-time") || "1.0 min";
    document.getElementById("speakerNotesText").innerHTML = notesBySlide[bounded] || "Sin notas.";

    try {{
      if (window.location.hash !== "#" + bounded) {{
        history.replaceState(null, "", "#" + bounded);
      }}
    }} catch (err) {{}}

    renderChartIfNeeded(bounded);
  }}

  function nextSlide() {{ updateSlide(currentSlide + 1); }}
  function prevSlide() {{ updateSlide(currentSlide - 1); }}

  function toggleSpeakerNotes() {{
    const drawer = document.getElementById("speakerDrawer");
    const isOpen = drawer.classList.toggle("open");
    drawer.setAttribute("aria-hidden", String(!isOpen));
  }}

  function toggleFullscreen() {{
    if (!document.fullscreenElement) {{
      if (document.documentElement.requestFullscreen) {{
        document.documentElement.requestFullscreen().catch(() => {{}});
      }}
    }} else if (document.exitFullscreen) {{
      document.exitFullscreen().catch(() => {{}});
    }}
  }}

  window.addEventListener("keydown", (event) => {{
    if (event.key === "ArrowRight" || event.key === " " || event.key === "PageDown") {{
      event.preventDefault();
      nextSlide();
    }} else if (event.key === "ArrowLeft" || event.key === "PageUp") {{
      event.preventDefault();
      prevSlide();
    }} else if (event.key === "Home") {{
      event.preventDefault();
      updateSlide(1);
    }} else if (event.key === "End") {{
      event.preventDefault();
      updateSlide(totalSlides);
    }} else if (event.key.toLowerCase() === "n") {{
      event.preventDefault();
      toggleSpeakerNotes();
    }} else if (event.key.toLowerCase() === "f") {{
      event.preventDefault();
      toggleFullscreen();
    }} else if (event.key === "Escape") {{
      const drawer = document.getElementById("speakerDrawer");
      if (drawer.classList.contains("open")) {{
        toggleSpeakerNotes();
      }}
    }}
  }});

  window.addEventListener("DOMContentLoaded", () => {{
    const rawHash = parseInt(window.location.hash.replace("#", ""), 10);
    const initialSlide = (!Number.isNaN(rawHash) && rawHash >= 1 && rawHash <= totalSlides) ? rawHash : 1;
    updateSlide(initialSlide);
  }});
</script>
</body>
</html>
"""


def build_deck(output_dir: Path | None = None) -> Path:
    """
    Compila el deck base de 3 diapositivas y retorna la ruta al `index.html` generado.

    Args:
        output_dir (Path | None, opcional): Directorio destino de salida. Si es `None`,
            escribe en la raíz de la charla (`BASE_DIR`).

    Returns:
        Path: Ruta absoluta o relativa al archivo `index.html` compilado.
    """
    target_dir = Path(output_dir) if output_dir is not None else BASE_DIR
    target_dir.mkdir(parents=True, exist_ok=True)

    metadata = _load_talk_metadata()
    data_json = json.dumps(_build_sample_data(), ensure_ascii=False, allow_nan=False)
    notes_json = json.dumps(_build_speaker_notes(), ensure_ascii=False, allow_nan=False)
    chartjs_code = _load_chartjs_bundle()
    css_content = _get_deck_css()
    slides_html = _build_slides_html(metadata)

    html_document = _render_html_document(
        metadata=metadata,
        data_json=data_json,
        notes_json=notes_json,
        css_content=css_content,
        slides_html=slides_html,
        chartjs_code=chartjs_code,
    )

    index_path = target_dir / DEFAULT_OUTPUT_FILENAME
    index_path.write_text(html_document, encoding="utf-8")
    return index_path


def main() -> None:
    """
    Ejecuta la compilación del deck desde la línea de comandos aceptando `--output-dir`.
    """
    parser = argparse.ArgumentParser(
        description="Compila el deck HTML autocontenido basado en la plantilla python-deck."
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=None,
        help="Directorio destino donde escribir el archivo index.html compilado.",
    )
    args = parser.parse_args()
    generated_path = build_deck(output_dir=args.output_dir)
    print(f"Deck generado correctamente en: {generated_path}")


if __name__ == "__main__":
    main()
