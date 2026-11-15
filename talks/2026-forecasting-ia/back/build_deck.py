"""
Archivo: talks/2026-forecasting-ia/back/build_deck.py
Fecha de modificación: 15/11/2026
Autor: Alex Prieto <alexprieto1997@gmail.com>

Descripción:
Motor de compilación autónomo para el deck interactivo de la charla
`2026-forecasting-ia` (`python-deck`). Ensambla estilos, diapositivas,
notas del orador, branding institucional, prototipos embebidos, librería
Chart.js offline y payloads reales de Caso 1 (SENAMHI Punchana) y Caso 2
(Café Jaén) en un archivo HTML autocontenido.

Acciones Principales:
    - Carga y sanitiza (`clean_nans`) los CSV y JSON reales de `data/`.
    - Embebe prototipos HTML interactivos, SVGs anatómicos y branding Base64.
    - Resuelve `chart.umd.min.js` desde `shared/python_deck/assets/` con
      respaldo local en `front/assets/`.
    - Genera `presentacion.html` e `index.html` en `output_dir` o `BASE_DIR`.
    - Copia los datasets procesados (`data/caso_1`, `data/caso_2`) cuando
      `output_dir` difiere de `BASE_DIR`.

Estructura Interna:
    - `clean_nans`: Sanitiza recursivamente `NaN` e infinitos hacia `None`.
    - `_load_deck_data`: Lee y transforma los CSV/JSON de ambos casos.
    - `_encode_first_existing`: Codifica en Base64 el primer prototipo existente.
    - `_load_chartjs_bundle`: Carga Chart.js compartido o local como fallback.
    - `_sync_runtime_assets`: Copia los datasets procesados hacia `target_dir`.
    - `_render_html_document`: Renderiza el documento HTML completo del deck.
    - `build_deck`: Orquesta la compilación hacia `output_dir` o `BASE_DIR`.
    - `main`: Punto de entrada CLI con soporte `--output-dir`.

Entradas / Dependencias:
    - `front/` (`deck_styles`, `deck_slides_p1`, `deck_slides_p2`, `deck_notes`, `deck_branding`).
    - `data/caso_1/*`, `data/caso_2/*`, `docs/notebooklm/*`, `docs/images/front/*`.
    - `shared/python_deck/assets/chart.umd.min.js` y `pandas`.

Salidas / Efectos:
    - Escribe `presentacion.html` e `index.html` en el directorio destino.

Ejecución:
    python talks/2026-forecasting-ia/back/build_deck.py [--output-dir RUTA]

Ejemplo de Uso:
    python talks/2026-forecasting-ia/back/build_deck.py --output-dir _site/2026-forecasting-ia

Argumentos:
    - --output-dir: Path | None - Directorio destino de compilación (opcional).
"""

import argparse
import base64
import json
import math
import shutil
import sys
from pathlib import Path
from typing import Any

import pandas as pd

BASE_DIR: Path = Path(__file__).resolve().parent.parent
REPO_ROOT: Path = BASE_DIR.parent.parent
FRONT_DIR: Path = BASE_DIR / "front"

# Prioriza los módulos de `front/` propios de esta charla frente a cualquier ruta previa.
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))
if str(FRONT_DIR) not in sys.path:
    sys.path.insert(0, str(FRONT_DIR))

from deck_branding import get_branding  # noqa: E402
from deck_notes import get_speaker_notes  # noqa: E402
from deck_slides_p1 import get_slides_part1  # noqa: E402
from deck_slides_p2 import get_slides_part2  # noqa: E402
from deck_styles import get_deck_css  # noqa: E402

SHARED_CHARTJS_PATH: Path = REPO_ROOT / "shared" / "python_deck" / "assets" / "chart.umd.min.js"
LOCAL_CHARTJS_FALLBACK_PATH: Path = BASE_DIR / "front" / "assets" / "chart.umd.min.js"

PROTOTYPE_CANDIDATES: dict[str, tuple[str, ...]] = {
    "b64_sim_html": (
        "docs/notebooklm/seccion_1/prototipos/5_Anatomia_de_la_senal_temporal_v3.html",
        "docs/notebooklm/seccion_1/5_Anatomia_de_la_senal_temporal_v3.html",
        "docs/notebooklm/seccion_1/prototipos/5_anatomia_senal_temporal_mejorada.html",
        "docs/notebooklm/seccion_1/5_anatomia_senal_temporal_mejorada.html",
        "docs/notebooklm/seccion_1/anatomia_senal_temporal_mejorada.html",
        "docs/notebooklm/seccion_1/5_anatom_a_ontol_gica_f_sica_vs_ruido.html",
        "docs/notebooklm/seccion_1/anatom_a_ontol_gica_f_sica_vs_ruido.html",
    ),
    "b64_era1_html": (
        "docs/notebooklm/seccion_1/prototipos/6_Era_1_La_parsimonia_lineal_v3.html",
        "docs/notebooklm/seccion_1/6_Era_1_La_parsimonia_lineal_v3.html",
        "docs/notebooklm/seccion_1/prototipos/6_Era_1_La_parsimonia_lineal.html",
        "docs/notebooklm/seccion_1/6_Era_1_La_parsimonia_lineal.html",
    ),
    "b64_era2_html": (
        "docs/notebooklm/seccion_1/prototipos/7_Era_2_El_puente_tabular.html",
        "docs/notebooklm/seccion_1/7_Era_2_El_puente_tabular.html",
    ),
    "b64_era3_html": (
        "docs/notebooklm/seccion_1/prototipos/8_Era_3_Deep_Learning_y_Parches.html",
        "docs/notebooklm/seccion_1/8_Era_3_Deep_Learning_y_Parches.html",
    ),
    "b64_era4_html": (
        "docs/notebooklm/seccion_1/prototipos/9_Era_4_Modelos_Fundacionales_Zero_Shot.html",
        "docs/notebooklm/seccion_1/9_Era_4_Modelos_Fundacionales_Zero_Shot.html",
    ),
    "b64_cono_html": (
        "docs/notebooklm/seccion_1/prototipos/10_El_Cono_de_Incertidumbre_y_Prediccion_Conforme.html",
        "docs/notebooklm/seccion_1/10_El_Cono_de_Incertidumbre_y_Prediccion_Conforme.html",
    ),
    "b64_decision_html": (
        "docs/notebooklm/seccion_1/prototipos/11_Arquitectura_de_Decision_y_Cierre_Ejecutivo.html",
        "docs/notebooklm/seccion_1/11_Arquitectura_de_Decision_y_Cierre_Ejecutivo.html",
    ),
    "b64_p19_html": (
        "docs/notebooklm/seccion_3/prototipos/19_c_mo_el_agro_invent_el_forecasting.html",
    ),
    "b64_p20_html": (
        "docs/notebooklm/seccion_3/prototipos/20_del_almanaque_al_sat_lite.html",
    ),
    "b64_p21_html": (
        "docs/notebooklm/seccion_3/prototipos/21_f_sica_biol_gica_y_el_l_mite_algor_tmico.html",
    ),
    "b64_p22_html": (
        "docs/notebooklm/seccion_3/prototipos/22_reloj_fenol_gico_del_caf.html",
    ),
    "b64_p23_html": (
        "docs/notebooklm/seccion_3/prototipos/23_precisi_n_actual_y_las_tres_trampas.html",
    ),
    "b64_p13_html": (
        "docs/notebooklm/seccion_2/prototipos/13_Datos_SENAMHI_Punchana.html",
    ),
    "b64_p14_html": (
        "docs/notebooklm/seccion_2/prototipos/14_Trampa_Arboles_Meseta_vs_Diferencias.html",
    ),
    "b64_p15_html": (
        "docs/notebooklm/seccion_2/prototipos/15_Benchmark_14_Modelos_Tierra_vs_Supercomputo.html",
    ),
    "b64_p16_html": (
        "docs/notebooklm/seccion_2/prototipos/16_Pronostico_7_Dias_Cono_P10_P90.html",
    ),
    "b64_p17_html": (
        "docs/notebooklm/seccion_2/prototipos/17_Pipeline_Codigo_Diferencias_ExtraTrees.html",
    ),
}


def clean_nans(obj: Any) -> Any:
    """
    Reemplaza recursivamente valores `NaN` o infinitos por `None` para serializar JSON válido.

    Args:
        obj (Any): Estructura arbitraria compuesta por diccionarios, listas o escalares.

    Returns:
        Any: Estructura equivalente libre de `NaN` e infinitos no válidos en JSON.
    """
    if isinstance(obj, float) and (pd.isna(obj) or math.isnan(obj) or math.isinf(obj)):
        return None
    if isinstance(obj, dict):
        return {key: clean_nans(value) for key, value in obj.items()}
    if isinstance(obj, list):
        return [clean_nans(item) for item in obj]
    return obj


def _load_deck_data() -> dict[str, Any]:
    """
    Carga y sanitiza los datasets auditados de Caso 1 y Caso 2 desde `BASE_DIR / "data"`.

    Returns:
        dict[str, Any]: Diccionario listo para inyectar en `window.DECK_DATA`.
    """
    bench_df = pd.read_csv(BASE_DIR / "data/caso_1/benchmark_punchana.csv")
    forecast_7d_df = pd.read_csv(BASE_DIR / "data/caso_1/senamhi_forecast_7d.csv")
    extrap_df = pd.read_csv(BASE_DIR / "data/caso_1/experimento_extrapolacion.csv")
    cafe_camp_df = pd.read_csv(BASE_DIR / "data/caso_2/cafe_jaen_campanias.csv")
    cafe_res_df = pd.read_csv(BASE_DIR / "data/caso_2/cafe_jaen_resultados.csv")
    cafe_bm_df = pd.read_csv(BASE_DIR / "data/caso_2/benchmark_cafe.csv")
    cafe_preds_df = pd.read_csv(BASE_DIR / "data/caso_2/cafe_jaen_predicciones_modelos.csv")
    noaa_ecmwf_df = pd.read_csv(BASE_DIR / "data/caso_1/noaa_ecmwf_forecast.csv")
    senamhi_diario_df = pd.read_csv(BASE_DIR / "data/caso_1/senamhi_diario.csv")

    hypothesis_path = BASE_DIR / "data/caso_2/cafe_jaen_hipotesis.json"
    hipotesis_cafe = json.loads(hypothesis_path.read_text(encoding="utf-8"))

    raw_payload: dict[str, Any] = {
        "benchmark": bench_df.to_dict(orient="records"),
        "forecast_7d": forecast_7d_df.to_dict(orient="records"),
        "extrapolacion": extrap_df.to_dict(orient="records"),
        "cafe_campanias": cafe_camp_df.to_dict(orient="records"),
        "cafe_resultados": cafe_res_df.to_dict(orient="records"),
        "cafe_benchmark": cafe_bm_df.to_dict(orient="records"),
        "cafe_predicciones": cafe_preds_df.to_dict(orient="records"),
        "hipotesis_cafe": hipotesis_cafe,
        "noaa_ecmwf": noaa_ecmwf_df.to_dict(orient="records"),
        "senamhi_reciente": senamhi_diario_df.tail(180).to_dict(orient="records"),
    }
    return clean_nans(raw_payload)


def _encode_first_existing(candidates: tuple[str, ...]) -> str:
    """
    Codifica en Base64 ASCII el primer archivo candidato existente bajo `BASE_DIR`.

    Args:
        candidates (tuple[str, ...]): Rutas relativas ordenadas por prioridad.

    Returns:
        str: Cadena Base64 del archivo encontrado, o cadena vacía si ninguno existe.
    """
    for rel_path in candidates:
        candidate_path = BASE_DIR / rel_path
        if candidate_path.is_file():
            return base64.b64encode(candidate_path.read_bytes()).decode("ascii")
    return ""


def _load_chartjs_bundle() -> str:
    """
    Lee el bundle UMD de Chart.js compartido, usando la copia local como respaldo.

    Returns:
        str: Código fuente de `chart.umd.min.js` o cadena vacía si no existe ninguno.
    """
    for candidate_path in (SHARED_CHARTJS_PATH, LOCAL_CHARTJS_FALLBACK_PATH):
        if candidate_path.is_file():
            return candidate_path.read_text(encoding="utf-8")
    return ""


def _sync_runtime_assets(target_dir: Path) -> None:
    """
    Copia los datasets procesados de `data/` hacia `target_dir` excluyendo `raw/`.

    Args:
        target_dir (Path): Directorio de salida distinto de `BASE_DIR`.
    """
    if target_dir.resolve() == BASE_DIR.resolve():
        return

    for case_name in ("caso_1", "caso_2"):
        src_case_dir = BASE_DIR / "data" / case_name
        if not src_case_dir.is_dir():
            continue
        dst_case_dir = target_dir / "data" / case_name
        dst_case_dir.mkdir(parents=True, exist_ok=True)
        for item in src_case_dir.iterdir():
            if item.is_file():
                shutil.copy2(item, dst_case_dir / item.name)


def _render_html_document(
    *,
    data_json: str,
    notes_json: str,
    branding: dict[str, str],
    css_content: str,
    slides_p1: str,
    slides_p2: str,
    chartjs_local_code: str,
) -> str:
    """
    Ensambla el documento HTML completo del deck con estilos, datos y scripts interactivos.

    Args:
        data_json (str): JSON serializado para `window.DECK_DATA`.
        notes_json (str): JSON serializado con las notas del orador por diapositiva.
        branding (dict[str, str]): Diccionario con recursos gráficos en Base64 y SVGs.
        css_content (str): Hoja de estilos CSS completa del deck.
        slides_p1 (str): Markup HTML de la primera mitad de diapositivas (1-14).
        slides_p2 (str): Markup HTML de la segunda mitad de diapositivas (15-30).
        chartjs_local_code (str): Bundle offline de Chart.js como fallback del CDN.

    Returns:
        str: Contenido HTML completo listo para escribir en disco.
    """
    b64_header_logo = branding["b64_header"]

    return f"""<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>¿Puede la IA predecir el futuro? Lecciones de forecasting desde el mundo real</title>
<link rel="icon" href="data:,">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;600;700&family=IBM+Plex+Sans:ital,wght@0,300;0,400;0,500;0,600;0,700;1,400&family=IBM+Plex+Mono:wght@400;500;600&display=swap" rel="stylesheet">
<script src="https://cdnjs.cloudflare.com/ajax/libs/Chart.js/4.4.1/chart.umd.min.js"></script>
<script>
  if (typeof Chart === 'undefined') {{
    {chartjs_local_code}
  }}
  if (typeof Chart !== 'undefined') {{
    Chart.defaults.color = '#CBD5E1';
    Chart.defaults.borderColor = 'rgba(169, 184, 218, 0.15)';
    Chart.defaults.font.family = '"IBM Plex Sans", sans-serif';
  }}
</script>
<style>
{css_content}
</style>
</head>
<body>

<!-- BARRA DE PROGRESO SUPERIOR -->
<div class="progress-container">
  <div class="progress-bar" id="progressBar"></div>
</div>

<!-- CONTENEDOR PRINCIPAL DE DIAPOSITIVAS -->
<main class="deck-container">
{slides_p1}
{slides_p2}
</main>

<!-- BARRA INFERIOR DE ESTADO Y CONTROL CON BRANDING IQUITOS DATA FEST 2026 -->
<footer class="deck-footer">
  <div style="display:flex; align-items:center; gap:16px;">
    <!-- LOGOS INSTITUCIONALES DEL EVENTO -->
    <div style="display:flex; align-items:center; gap:12px;">
      <img src="data:image/png;base64,{b64_header_logo}" alt="UNAP · Neo Kernel · Grupo de Datos & IA" style="height:26px; filter:drop-shadow(0 1px 2px rgba(0,0,0,0.6)); opacity:0.95;">
      <span style="font-size:11px; font-weight:700; color:var(--text-faint); letter-spacing:0.04em;" class="mono hidden-mobile">
        IQUITOS <span style="color:#12C8FC;">DATA FEST 2026</span> · 30 de octubre · Aula Magna UNAP
      </span>
    </div>
    <div style="width:1px; height:18px; background:rgba(18, 200, 252, 0.25); margin:0 4px;"></div>
    <div style="font-weight:700; font-size:13px; color:#12C8FC;" class="mono" id="slideIndicator">01 / 30</div>
    <div style="font-size:12px; color:var(--text-faint);" class="mono" id="actIndicator">Apertura · Portada</div>
  </div>

  <div style="display:flex; align-items:center; gap:8px;">
    <button class="nav-btn" onclick="toggleSpeakerNotes()" title="Ver notas y guion del orador (N)">[N] Notas</button>
    <button class="nav-btn" onclick="prevSlide()" title="Diapositiva anterior (&larr; / PageUp)">&larr; Prev</button>
    <button class="nav-btn" onclick="nextSlide()" title="Siguiente diapositiva (&rarr; / Espacio)">Next &rarr;</button>
  </div>
</footer>

<!-- DRAWER DE NOTAS DEL ORADOR (ACCESIBLE CON 'N') -->
<aside class="speaker-drawer" id="speakerDrawer">
  <div class="speaker-header">
    <div style="display:flex; align-items:center; gap:12px;">
      <span style="font-weight:700; font-size:12px;" class="mono">🎙️ NOTAS DEL ORADOR & GUION CONVERSACIONAL</span>
      <span id="speakerTimer" style="font-size:11.5px; color:#60A5FA;" class="mono">⏱️ 1.5 min</span>
    </div>
    <button class="nav-btn" style="padding:2px 8px;" onclick="toggleSpeakerNotes()">Cerrar [N]</button>
  </div>
  <div class="speaker-body" id="speakerNotesText">
    Notas cargando...
  </div>
</aside>

<!-- MODAL LIGHTBOX PARA AMPLIAR INFOGRAFÍAS NOTEBOOKLM -->
<div class="lightbox-modal" id="lightboxModal" onclick="closeLightbox()">
  <div class="lightbox-close" onclick="closeLightbox()">&times;</div>
  <img class="lightbox-img" id="lightboxImg" src="" alt="Infografía Ampliada" onclick="event.stopPropagation()">
</div>

<!-- INYECCIÓN DE DATOS REALES -->
<script>
  window.DECK_DATA = {data_json};
</script>

<!-- SCRIPTS DE NAVEGACIÓN Y VISUALES -->
<script>
  let currentSlide = 1;
  const totalSlides = 30;

  const notesBySlide = {notes_json};

  function updateSlide(index) {{
    if (index < 1) index = 1;
    if (index > totalSlides) index = totalSlides;

    document.querySelectorAll(".slide").forEach(s => s.classList.remove("active"));
    const target = document.querySelector(`.slide[data-index="${{index}}"]`);
    if (target) {{
      target.classList.add("active");
      currentSlide = index;
      document.getElementById("slideIndicator").textContent = `${{String(index).padStart(2, '0')}} / ${{totalSlides}}`;
      document.getElementById("actIndicator").textContent = target.getAttribute("data-act");
      document.getElementById("progressBar").style.width = `${{(index / totalSlides) * 100}}%`;
      
      document.getElementById("speakerTimer").textContent = `⏱️ ${{target.getAttribute("data-time")}}`;
      document.getElementById("speakerNotesText").innerHTML = notesBySlide[index] || "Notas en preparación.";

      try {{
        if (window.location.hash !== "#" + index) {{
          history.replaceState(null, "", "#" + index);
        }}
      }} catch (e) {{}}

      const ifr = target.querySelector("iframe");
      if (ifr && ifr.contentWindow) {{
        try {{
          ifr.contentWindow.postMessage({{ type: "activate" }}, "*");
        }} catch (err) {{}}
      }}

      initSlideVisuals(index);
    }}
  }}

  function nextSlide() {{ updateSlide(currentSlide + 1); }}
  function prevSlide() {{ updateSlide(currentSlide - 1); }}

  function toggleSpeakerNotes() {{
    document.getElementById("speakerDrawer").classList.toggle("open");
  }}

  function toggleDarkMode() {{
    document.body.classList.toggle("dark-mode");
  }}

  function openLightbox(src) {{
    const modal = document.getElementById("lightboxModal");
    const img = document.getElementById("lightboxImg");
    if (modal && img) {{
      img.src = src;
      modal.classList.add("active");
    }}
  }}

  function closeLightbox() {{
    const modal = document.getElementById("lightboxModal");
    if (modal) {{
      modal.classList.remove("active");
    }}
  }}

  window.addEventListener("message", (e) => {{
    if (e.data && e.data.type === "deck_key") {{
      const key = e.data.key;
      if (key === "ArrowRight" || key === "PageDown") {{
        nextSlide();
      }} else if (key === "ArrowLeft" || key === "PageUp") {{
        prevSlide();
      }} else if (key === "Home") {{
        updateSlide(1);
      }} else if (key === "End") {{
        updateSlide(totalSlides);
      }} else if (key.toLowerCase() === "n") {{
        toggleSpeakerNotes();
      }} else if (key.toLowerCase() === "d") {{
        toggleDarkMode();
      }} else if (key.toLowerCase() === "f") {{
        if (!document.fullscreenElement) {{
          document.documentElement.requestFullscreen();
        }} else {{
          document.exitFullscreen();
        }}
      }} else if (key === "Escape") {{
        closeLightbox();
      }}
    }}
  }});

  window.addEventListener("resize", () => {{
    document.querySelectorAll(".slide.active iframe").forEach(ifr => {{
      try {{
        ifr.contentWindow.postMessage({{ type: "resize" }}, "*");
      }} catch (err) {{}}
    }});
  }});

  window.addEventListener("keydown", (e) => {{
    if (e.key === "Escape") {{
      closeLightbox();
      return;
    }}
    if (e.key === "ArrowRight" || e.key === " " || e.key === "PageDown") {{
      e.preventDefault();
      nextSlide();
    }} else if (e.key === "ArrowLeft" || e.key === "PageUp") {{
      e.preventDefault();
      prevSlide();
    }} else if (e.key === "Home") {{
      e.preventDefault();
      updateSlide(1);
    }} else if (e.key === "End") {{
      e.preventDefault();
      updateSlide(totalSlides);
    }} else if (e.key.toLowerCase() === "n") {{
      e.preventDefault();
      toggleSpeakerNotes();
    }} else if (e.key.toLowerCase() === "d") {{
      e.preventDefault();
      toggleDarkMode();
    }} else if (e.key.toLowerCase() === "f") {{
      if (!document.fullscreenElement) {{
        document.documentElement.requestFullscreen();
      }} else {{
        document.exitFullscreen();
      }}
    }}
  }});

  function updateAlpha(val) {{
    document.getElementById("alphaVal").textContent = parseFloat(val).toFixed(2);
    renderAlphaBars(parseFloat(val));
  }}

  function renderAlphaBars(alpha) {{
    const container = document.getElementById("alphaBars");
    if (!container) return;
    container.innerHTML = "";
    for (let k = 0; k < 5; k++) {{
      const weight = alpha * Math.pow(1 - alpha, k);
      const pct = (weight * 100).toFixed(1);
      const bar = document.createElement("div");
      bar.style.flex = "1";
      bar.style.height = `${{weight * 200}}px`;
      bar.style.background = k === 0 ? "#2563EB" : "#94A3B8";
      bar.style.borderRadius = "4px 4px 0 0";
      bar.style.display = "flex";
      bar.style.alignItems = "flex-start";
      bar.style.justifyContent = "center";
      bar.style.paddingTop = "4px";
      bar.style.color = "#FFF";
      bar.style.fontSize = "10px";
      bar.style.fontFamily = "IBM Plex Mono";
      bar.textContent = `${{pct}}%`;
      container.appendChild(bar);
    }}
  }}

  // Procedural Ontological Signal Simulator (Slide 02)
  const signalLayers = {{ T: true, S: true, C: true, E: true }};
  let waveAnimId = null;
  let wavePhase = 0;

  function toggleSignalLayer(layer) {{
    signalLayers[layer] = !signalLayers[layer];
    const btn = document.getElementById("btnToggle" + layer);
    if (btn) {{
      if (signalLayers[layer]) {{
        btn.classList.add("active");
        btn.textContent = btn.textContent.replace("✗", "✓");
      }} else {{
        btn.classList.remove("active");
        btn.textContent = btn.textContent.replace("✓", "✗");
      }}
    }}
    const count = Object.values(signalLayers).filter(Boolean).length;
    const status = document.getElementById("simLayerStatus");
    if (status) {{
      status.textContent = `${{count}} / 4 Capas Físicas`;
    }}
  }}

  function startOntologicalWaveSimulation() {{
    const canvas = document.getElementById("ontologicalWaveCanvas");
    if (!canvas) return;
    const ctx = canvas.getContext("2d");

    function resize() {{
      const rect = canvas.getBoundingClientRect();
      if (rect.width > 0 && rect.height > 0) {{
        canvas.width = rect.width * (window.devicePixelRatio || 1);
        canvas.height = rect.height * (window.devicePixelRatio || 1);
      }}
    }}
    resize();

    function draw() {{
      if (currentSlide !== 2) {{
        if (waveAnimId) cancelAnimationFrame(waveAnimId);
        return;
      }}
      wavePhase += 0.025;
      const w = canvas.width;
      const h = canvas.height;
      if (w === 0 || h === 0) {{
        resize();
      }}
      ctx.clearRect(0, 0, w, h);

      const isDark = document.body.classList.contains("dark-mode");
      const gridColor = isDark ? "rgba(255,255,255,0.05)" : "rgba(0,0,0,0.05)";
      const axisColor = isDark ? "rgba(255,255,255,0.2)" : "rgba(0,0,0,0.15)";
      
      // Grid lines
      ctx.strokeStyle = gridColor;
      ctx.lineWidth = 1;
      for (let x = 0; x < w; x += 40) {{
        ctx.beginPath();
        ctx.moveTo(x, 0);
        ctx.lineTo(x, h);
        ctx.stroke();
      }}
      for (let y = 0; y < h; y += 28) {{
        ctx.beginPath();
        ctx.moveTo(0, y);
        ctx.lineTo(w, y);
        ctx.stroke();
      }}

      // Zero axis
      const midY = h * 0.52;
      ctx.strokeStyle = axisColor;
      ctx.setLineDash([4, 4]);
      ctx.beginPath();
      ctx.moveTo(0, midY);
      ctx.lineTo(w, midY);
      ctx.stroke();
      ctx.setLineDash([]);

      const numPts = 260;
      const points = [];
      for (let i = 0; i < numPts; i++) {{
        const t = (i / numPts) * 10;
        let val = 0;
        if (signalLayers.T) val += (t - 5) * 3.8;
        if (signalLayers.S) val += Math.sin(t * 3.6 + wavePhase) * 22;
        if (signalLayers.C) val += Math.sin(t * 0.85 + wavePhase * 0.35) * 14;
        if (signalLayers.E) {{
          const pseudoNoise = Math.sin(i * 123.4 + Math.floor(wavePhase * 3)) * Math.cos(i * 56.7);
          val += pseudoNoise * 6.5;
          if (i === 160) val -= 32; // Friaje spike
          if (i === 65) val += 24;  // Heat wave spike
        }}
        const px = (i / (numPts - 1)) * w;
        const py = midY - val * (h / 120);
        points.push({{ x: px, y: py }});
      }}

      // Gradient fill
      const grad = ctx.createLinearGradient(0, 0, 0, h);
      grad.addColorStop(0, "rgba(37, 99, 235, 0.22)");
      grad.addColorStop(1, "rgba(37, 99, 235, 0.0)");
      ctx.fillStyle = grad;
      ctx.beginPath();
      ctx.moveTo(points[0].x, points[0].y);
      for (let i = 1; i < points.length; i++) {{
        ctx.lineTo(points[i].x, points[i].y);
      }}
      ctx.lineTo(w, h);
      ctx.lineTo(0, h);
      ctx.closePath();
      ctx.fill();

      // Signal line
      ctx.strokeStyle = isDark ? "#60A5FA" : "#2563EB";
      ctx.lineWidth = 2.4;
      ctx.beginPath();
      ctx.moveTo(points[0].x, points[0].y);
      for (let i = 1; i < points.length; i++) {{
        ctx.lineTo(points[i].x, points[i].y);
      }}
      ctx.stroke();

      // Highlight Friaje extreme spike if noise enabled
      if (signalLayers.E && points[160]) {{
        const fp = points[160];
        ctx.fillStyle = "#DC2626";
        ctx.beginPath();
        ctx.arc(fp.x, fp.y, 4.5, 0, Math.PI * 2);
        ctx.fill();
        ctx.fillStyle = isDark ? "#FCA5A5" : "#DC2626";
        ctx.font = "9.5px 'IBM Plex Mono'";
        ctx.fillText("Anomalía Friaje > 2.5σ (-19.2°C)", fp.x - 70, fp.y + 16);
      }}

      waveAnimId = requestAnimationFrame(draw);
    }}

    if (waveAnimId) cancelAnimationFrame(waveAnimId);
    draw();
  }}

  let charts = {{}};

  function initSlideVisuals(idx) {{
    try {{
      if (idx === 2) {{
        startOntologicalWaveSimulation();
      }}

      if (idx === 4) {{
        renderAlphaBars(0.35);
      }}

      // Slide 14: Experimento Extrapolación (Antes diapo 10)
      if (idx === 14 && !charts["extrap"]) {{
        const canvas = document.getElementById("chartExtrap") || document.getElementById("chartExtrapolacion");
        if (canvas) {{
          const ctx = canvas.getContext("2d");
          const d = window.DECK_DATA.extrapolacion;
          charts["extrap"] = new Chart(ctx, {{
            type: "line",
            data: {{
              labels: d.map(r => r.fecha.slice(5)),
              datasets: [
                {{
                  label: "Temperatura Real Observada (°C)",
                  data: d.map(r => r.tmax_real),
                  borderColor: "#FFFFFF",
                  borderWidth: 2.8,
                  pointRadius: 3
                }},
                {{
                  label: "Random Forest Directo (Meseta 31.5°C)",
                  data: d.map(r => r.pred_arbol_niveles),
                  borderColor: "#DC2626",
                  borderWidth: 2.5,
                  borderDash: [5, 4],
                  pointRadius: 2.5
                }},
                {{
                  label: "Modelo sobre Diferencias Δy (Sube a 35.45°C)",
                  data: d.map(r => r.pred_arbol_diferencias),
                  borderColor: "#059669",
                  borderWidth: 2.5,
                  pointRadius: 2.5
                }},
                {{
                  label: "Tope Entrenamiento (34.0°C)",
                  data: d.map(r => r.tope_entrenamiento),
                  borderColor: "#94A3B8",
                  borderWidth: 1.5,
                  borderDash: [3, 3],
                  pointRadius: 0
                }}
              ]
            }},
            options: {{
              responsive: true,
              maintainAspectRatio: false,
              plugins: {{
                legend: {{ position: "top", labels: {{ font: {{ family: "IBM Plex Mono", size: 10.5 }} }} }}
              }},
              scales: {{
                y: {{ min: 28, max: 39, title: {{ display: true, text: "Tmax (°C)" }} }}
              }}
            }}
          }});
        }}
      }}

      // Slide 14: Discrepancia NOAA vs ECMWF (Antes diapo 10)
      if (idx === 14 && !charts["noaaEcmwf"]) {{
        const canvas = document.getElementById("chartNoaaEcmwf");
        if (canvas) {{
          const ctx = canvas.getContext("2d");
          const d = window.DECK_DATA.noaa_ecmwf;
          charts["noaaEcmwf"] = new Chart(ctx, {{
            type: "bar",
            data: {{
              labels: d.map(r => r.fecha.slice(5)),
              datasets: [
                {{
                  label: "NOAA GFS Tmax (°C)",
                  data: d.map(r => r.tmax_noaa_gfs),
                  backgroundColor: "rgba(37, 99, 235, 0.75)"
                }},
                {{
                  label: "ECMWF IFS Tmax (°C)",
                  data: d.map(r => r.tmax_ecmwf),
                  backgroundColor: "rgba(217, 119, 6, 0.75)"
                }}
              ]
            }},
            options: {{
              responsive: true,
              maintainAspectRatio: false,
              plugins: {{
                legend: {{ position: "top", labels: {{ font: {{ family: "IBM Plex Mono", size: 11 }} }} }}
              }},
              scales: {{
                y: {{ min: 24, max: 38, title: {{ display: true, text: "Tmax (°C)" }} }}
              }}
            }}
          }});
        }}
      }}

      // Slide 16: Serie histórica reciente SENAMHI (Antes diapo 12)
      if (idx === 16 && !charts["senamhiReciente"]) {{
        const canvas = document.getElementById("chartSenamhiReciente");
        if (canvas) {{
          const ctx = canvas.getContext("2d");
          const d = window.DECK_DATA.senamhi_reciente;
          charts["senamhiReciente"] = new Chart(ctx, {{
            type: "line",
            data: {{
              labels: d.map(r => r.fecha.slice(5)),
              datasets: [
                {{
                  label: "Tmax Punchana (°C)",
                  data: d.map(r => r.tmax),
                  borderColor: "#2563EB",
                  borderWidth: 2,
                  pointRadius: 0
                }},
                {{
                  label: "Tmin Punchana (°C)",
                  data: d.map(r => r.tmin),
                  borderColor: "#0891B2",
                  borderDash: [2, 2],
                  borderWidth: 1.5,
                  pointRadius: 0
                }}
              ]
            }},
            options: {{
              responsive: true,
              maintainAspectRatio: false,
              plugins: {{
                legend: {{ position: "top", labels: {{ font: {{ family: "IBM Plex Mono", size: 10.5 }} }} }}
              }},
              scales: {{
                y: {{ min: 18, max: 38, title: {{ display: true, text: "Temperatura (°C)" }} }}
              }}
            }}
          }});
        }}
      }}

      // Slide 15: Benchmark Punchana (Antes diapo 11)
      if (idx === 15 && !charts["benchmark"]) {{
        const canvas = document.getElementById("chartBenchmark");
        if (canvas) {{
          const ctx = canvas.getContext("2d");
          const d = window.DECK_DATA.benchmark;
          charts["benchmark"] = new Chart(ctx, {{
            type: "bar",
            data: {{
              labels: d.map(r => r.modelo),
              datasets: [{{
                label: "RMSE (°C) en Holdout de 90 Días",
                data: d.map(r => r.rmse_1d),
                extraData: d,
                backgroundColor: d.map(r => {{
                  if (r.modelo && r.modelo.includes("ExtraTrees")) return "#059669";
                  if (r.familia && r.familia.includes("Física Global")) return "#8B5CF6";
                  if (r.p_valor_vs_mejor >= 0.05) return "#10B981";
                  if (r.familia && r.familia.includes("Baseline")) return "#EF4444";
                  return "#F59E0B";
                }})
              }}]
            }},
            options: {{
              indexAxis: "y",
              responsive: true,
              maintainAspectRatio: false,
              plugins: {{
                legend: {{ display: false }},
                tooltip: {{
                  callbacks: {{
                    label: (context) => {{
                      const row = context.dataset.extraData ? context.dataset.extraData[context.dataIndex] : null;
                      if (!row) return `${{context.dataset.label}}: ${{context.raw}} °C`;
                      return [
                        `RMSE (1D): ${{row.rmse_1d}} °C | MAE (1D): ${{row.mae_1d}} °C`,
                        `RMSE (7D): ${{row.rmse_7d}} °C | MAE (7D): ${{row.mae_7d}} °C`,
                        `Hardware: ${{row.hardware}} | Tiempo: ${{row.tiempo_s}}s`,
                        `p-valor vs ExtraTrees: ${{row.p_valor_vs_mejor >= 0.05 ? row.p_valor_vs_mejor + ' (Empate estadístico)' : row.p_valor_vs_mejor + ' (Diferencia significativa)'}}`
                      ];
                    }}
                  }}
                }}
              }},
              scales: {{
                x: {{ min: 1.6, max: 3.1, title: {{ display: true, text: "RMSE (°C) en Holdout de 90 Días — Menor es mejor" }} }}
              }}
            }}
          }});
        }}
      }}

      // Slide 16: Demo Pronóstico 7 Días con Bandas (Antes diapo 12)
      if (idx === 16 && !charts["demo7d"]) {{
        const canvas = document.getElementById("chartDemo7d");
        if (canvas) {{
          const ctx = canvas.getContext("2d");
          const d = window.DECK_DATA.forecast_7d;
          charts["demo7d"] = new Chart(ctx, {{
            type: "line",
            data: {{
              labels: d.map(r => r.fecha.slice(5)),
              datasets: [
                {{
                  label: "Observado SENAMHI",
                  data: d.map(r => r.tmax_observada),
                  borderColor: "#FFFFFF",
                  borderWidth: 3,
                  pointRadius: 4,
                  fill: false
                }},
                {{
                  label: "ExtraTrees (Ganador)",
                  data: d.map(r => r.pred_extratrees),
                  borderColor: "#059669",
                  borderWidth: 2.5,
                  pointRadius: 3,
                  fill: false
                }},
                {{
                  label: "P90 Incertidumbre",
                  data: d.map(r => r.ci_upper_p90),
                  borderColor: "rgba(5, 150, 105, 0.4)",
                  borderDash: [3, 3],
                  borderWidth: 1.5,
                  pointRadius: 0,
                  fill: false
                }},
                {{
                  label: "P10 Incertidumbre",
                  data: d.map(r => r.ci_lower_p10),
                  borderColor: "rgba(5, 150, 105, 0.4)",
                  borderDash: [3, 3],
                  borderWidth: 1.5,
                  pointRadius: 0,
                  fill: "-1",
                  backgroundColor: "rgba(5, 150, 105, 0.1)"
                }},
                {{
                  label: "TimesFM 200M Zero-Shot",
                  data: d.map(r => r.pred_timesfm),
                  borderColor: "#6366F1",
                  borderWidth: 2,
                  pointRadius: 2.5,
                  hidden: false
                }},
                {{
                  label: "ECMWF IFS (~9km)",
                  data: d.map(r => r.pred_ecmwf),
                  borderColor: "#8B5CF6",
                  borderWidth: 1.8,
                  borderDash: [4, 3],
                  pointRadius: 2.5,
                  hidden: false
                }},
                {{
                  label: "NOAA GFS (~28km)",
                  data: d.map(r => r.pred_noaa_gfs),
                  borderColor: "#F97316",
                  borderWidth: 1.8,
                  borderDash: [2, 2],
                  pointRadius: 2.5,
                  hidden: false
                }},
                {{
                  label: "Chronos T5 Zero-Shot",
                  data: d.map(r => r.pred_chronos),
                  borderColor: "#D97706",
                  borderWidth: 2,
                  borderDash: [4, 4],
                  pointRadius: 2.5,
                  hidden: true
                }},
                {{
                  label: "ARIMA (2,0,1)",
                  data: d.map(r => r.pred_arima),
                  borderColor: "#0284C7",
                  borderWidth: 1.8,
                  borderDash: [2, 2],
                  pointRadius: 2,
                  hidden: true
                }}
              ]
            }},
            options: {{
              responsive: true,
              maintainAspectRatio: false,
              plugins: {{
                legend: {{ position: "top", labels: {{ font: {{ family: "IBM Plex Mono", size: 10.5 }} }} }},
                tooltip: {{
                  callbacks: {{
                    label: (ctx) => {{
                      const obs = d[ctx.dataIndex].tmax_observada;
                      if (ctx.datasetIndex === 0) {{
                        return `SENAMHI Observado: ${{ctx.raw.toFixed(2)}} °C`;
                      }}
                      const diff = (ctx.raw - obs).toFixed(2);
                      const sign = diff > 0 ? "+" : "";
                      return `${{ctx.dataset.label}}: ${{ctx.raw.toFixed(2)}} °C (Error: ${{sign}}${{diff}} °C)`;
                    }}
                  }}
                }}
              }},
              scales: {{
                y: {{ min: 22, max: 38, title: {{ display: true, text: "Tmax (°C)" }} }}
              }}
            }}
          }});
        }}
      }}

      // Slide 19: Jaén Histórico (Antes diapo 15)
      if (idx === 19 && !charts["jaenHist"]) {{
        const canvas = document.getElementById("chartJaenHistorico");
        if (canvas) {{
          const ctx = canvas.getContext("2d");
          const d = window.DECK_DATA.cafe_campanias;
          const valid = d.filter(r => r.rendimiento_qq_ha !== null);
          charts["jaenHist"] = new Chart(ctx, {{
            type: "line",
            data: {{
              labels: valid.map(r => r.campania),
              datasets: [{{
                label: "Rendimiento Oficial SIEA (qq/ha)",
                data: valid.map(r => r.rendimiento_qq_ha),
                borderColor: "#059669",
                backgroundColor: "rgba(5, 150, 105, 0.08)",
                fill: true,
                borderWidth: 2.5,
                pointRadius: 5,
                pointBackgroundColor: valid.map(r => (r.campania === 2013 || r.campania === 2014) ? "#DC2626" : "#059669")
              }}]
            }},
            options: {{
              responsive: true,
              maintainAspectRatio: false,
              plugins: {{
                legend: {{ display: false }},
                tooltip: {{
                  callbacks: {{
                    afterLabel: (ctx) => ctx.label === "2014" ? "⚠️ CRISIS DE LA ROYA AMARILLA (-56%)" : ""
                  }}
                }}
              }},
              scales: {{
                y: {{ min: 8, max: 38, title: {{ display: true, text: "Rendimiento (qq/ha)" }} }}
              }}
            }}
          }});
        }}
      }}

      // Slide 26: Scatter NDVI vs Rendimiento
      if (idx === 26 && !charts["scatterNdvi"]) {{
        const canvas = document.getElementById("chartScatterNdvi");
        if (canvas) {{
          const ctx = canvas.getContext("2d");
          const d = window.DECK_DATA.cafe_campanias;
          const valid = d.filter(r => r.rendimiento_qq_ha !== null);
          charts["scatterNdvi"] = new Chart(ctx, {{
            type: "scatter",
            data: {{
              datasets: [
                {{
                  label: "Campañas Auditadas (MODIS NDVI Anual)",
                  data: valid.map(r => ({{ x: r.ndvi_anual, y: r.rendimiento_qq_ha, anio: r.campania, val: r.ndvi_anual, unidad: "NDVI" }})),
                  backgroundColor: valid.map(r => r.campania === 2014 ? "#DC2626" : "#2563EB"),
                  pointRadius: valid.map(r => r.campania === 2014 ? 8 : 5)
                }},
                {{
                  type: "line",
                  label: "Tendencia Lineal NDVI (r = 0.154, p = 0.600 — Pendiente Nula)",
                  data: [{{ x: 0.69, y: 19.96 }}, {{ x: 0.78, y: 22.17 }}],
                  borderColor: "#94A3B8",
                  borderDash: [4, 4],
                  borderWidth: 1.8,
                  pointRadius: 0,
                  fill: false
                }}
              ]
            }},
            options: {{
              responsive: true,
              maintainAspectRatio: false,
              plugins: {{
                legend: {{ position: "top", labels: {{ font: {{ family: "IBM Plex Mono", size: 10 }} }} }},
                tooltip: {{
                  callbacks: {{
                    label: (ctx) => {{
                      if (ctx.raw.anio) {{
                        const notaRoya = ctx.raw.anio === 2014 ? " [⚠️ CRISIS DE LA ROYA AMARILLA -56%]" : "";
                        return `Campaña ${{ctx.raw.anio}}: ${{ctx.raw.val !== undefined ? ctx.raw.val.toFixed(2) : ctx.raw.x}} ${{ctx.raw.unidad || ''}} -> Rend: ${{ctx.raw.y.toFixed(2)}} qq/ha${{notaRoya}}`;
                      }}
                      return ctx.dataset.label;
                    }}
                  }}
                }}
              }},
              scales: {{
                x: {{ min: 0.68, max: 0.80, title: {{ display: true, text: "NDVI MODIS Anual (r = 0.154, p = 0.600 — Señal Saturada)" }} }},
                y: {{ min: 8, max: 38, title: {{ display: true, text: "Rendimiento (qq/ha)" }} }}
              }}
            }}
          }});
        }}
      }}

      // Slide 27: Demo 2 Validación expansiva Jaén
      if (idx === 27 && !charts["demoJaen"]) {{
        switchJaenViewMode("trajectory");
      }}
    }} catch (err) {{
      console.warn("Visual initialization notice on slide", idx, err);
    }}
  }}

  function filterBenchmarkPunchana(filterType) {{
    const chart = charts["benchmark"];
    if (!chart) return;
    const allData = window.DECK_DATA.benchmark;
    let filtered = allData;
    if (filterType === "leaders") {{
      filtered = allData.filter(r => r.p_valor_vs_mejor >= 0.05);
    }} else if (filterType === "nwp") {{
      filtered = allData.filter(r => (r.familia && r.familia.includes("Física Global")) || (r.modelo && r.modelo.includes("ExtraTrees")));
    }} else if (filterType === "local") {{
      filtered = allData.filter(r => !(r.familia && r.familia.includes("Física Global")));
    }}

    ["btnBmAll", "btnBmLeaders", "btnBmNwp", "btnBmLocal"].forEach(id => {{
      const b = document.getElementById(id);
      if (b) b.classList.remove("active");
    }});
    if (filterType === "all") document.getElementById("btnBmAll")?.classList.add("active");
    if (filterType === "leaders") document.getElementById("btnBmLeaders")?.classList.add("active");
    if (filterType === "nwp") document.getElementById("btnBmNwp")?.classList.add("active");
    if (filterType === "local") document.getElementById("btnBmLocal")?.classList.add("active");

    chart.data.labels = filtered.map(r => r.modelo);
    chart.data.datasets[0].data = filtered.map(r => r.rmse_1d);
    chart.data.datasets[0].extraData = filtered;
    chart.data.datasets[0].backgroundColor = filtered.map(r => {{
      if (r.modelo && r.modelo.includes("ExtraTrees")) return "#059669";
      if (r.familia && r.familia.includes("Física Global")) return "#8B5CF6";
      if (r.p_valor_vs_mejor >= 0.05) return "#10B981";
      if (r.familia && r.familia.includes("Baseline")) return "#EF4444";
      return "#F59E0B";
    }});
    chart.update();
  }}

  function filterDemo7dView(viewType) {{
    const chart = charts["demo7d"];
    if (!chart) return;
    ["btnDemoAll", "btnDemoNwp", "btnDemoWinner"].forEach(id => {{
      const b = document.getElementById(id);
      if (b) b.classList.remove("active");
    }});
    if (viewType === "all") document.getElementById("btnDemoAll")?.classList.add("active");
    if (viewType === "nwp") document.getElementById("btnDemoNwp")?.classList.add("active");
    if (viewType === "winner") document.getElementById("btnDemoWinner")?.classList.add("active");

    if (viewType === "all") {{
      [0, 1, 2, 3, 4, 5, 6].forEach(i => chart.setDatasetVisibility(i, true));
      [7, 8].forEach(i => chart.setDatasetVisibility(i, false));
    }} else if (viewType === "nwp") {{
      [0, 1, 5, 6].forEach(i => chart.setDatasetVisibility(i, true));
      [2, 3, 4, 7, 8].forEach(i => chart.setDatasetVisibility(i, false));
    }} else if (viewType === "winner") {{
      [0, 1, 2, 3].forEach(i => chart.setDatasetVisibility(i, true));
      [4, 5, 6, 7, 8].forEach(i => chart.setDatasetVisibility(i, false));
    }}
    chart.update();
  }}

  function switchScatterVariable(varType) {{
    const chart = charts["scatterNdvi"];
    if (!chart) return;
    const d = window.DECK_DATA.cafe_campanias;
    const valid = d.filter(r => r.rendimiento_qq_ha !== null);

    ["btnScatterNdvi", "btnScatterDef", "btnScatterLluvia"].forEach(id => {{
      const b = document.getElementById(id);
      if (b) b.classList.remove("active");
    }});

    if (varType === "ndvi") {{
      document.getElementById("btnScatterNdvi")?.classList.add("active");
      chart.data.datasets[0].label = "Campañas Auditadas (MODIS NDVI Anual)";
      chart.data.datasets[0].data = valid.map(r => ({{ x: r.ndvi_anual, y: r.rendimiento_qq_ha, anio: r.campania, val: r.ndvi_anual, unidad: "NDVI" }}));
      chart.data.datasets[1].label = "Tendencia Lineal NDVI (r = 0.154, p = 0.600 — Pendiente Nula)";
      chart.data.datasets[1].data = [{{ x: 0.69, y: 19.96 }}, {{ x: 0.78, y: 22.17 }}];
      chart.options.scales.x.min = 0.68;
      chart.options.scales.x.max = 0.80;
      chart.options.scales.x.title.text = "NDVI MODIS Anual (r = 0.154, p = 0.600 — Señal Saturada)";
    }} else if (varType === "deficit") {{
      document.getElementById("btnScatterDef")?.classList.add("active");
      chart.data.datasets[0].label = "Campañas Auditadas (Déficit Hídrico Floración)";
      chart.data.datasets[0].data = valid.map(r => ({{ x: r.def_hidrico_flor_mm, y: r.rendimiento_qq_ha, anio: r.campania, val: r.def_hidrico_flor_mm, unidad: "mm" }}));
      chart.data.datasets[1].label = "Tendencia Lineal Déficit (r = 0.756, p = 0.002 — Fuerte Causalidad)";
      chart.data.datasets[1].data = [{{ x: -280, y: 16.67 }}, {{ x: 480, y: 27.63 }}];
      chart.options.scales.x.min = -300;
      chart.options.scales.x.max = 500;
      chart.options.scales.x.title.text = "Balance Hídrico Floración P - PET (mm) · ERA5 (r = 0.756, p = 0.002)";
    }} else if (varType === "lluvia") {{
      document.getElementById("btnScatterLluvia")?.classList.add("active");
      chart.data.datasets[0].label = "Campañas Auditadas (Lluvia en Floración)";
      chart.data.datasets[0].data = valid.map(r => ({{ x: r.lluvia_flor_mm, y: r.rendimiento_qq_ha, anio: r.campania, val: r.lluvia_flor_mm, unidad: "mm" }}));
      chart.data.datasets[1].label = "Tendencia Lineal Lluvia (r = 0.751, p = 0.002 — Señal Crítica)";
      chart.data.datasets[1].data = [{{ x: 50, y: 16.48 }}, {{ x: 800, y: 27.52 }}];
      chart.options.scales.x.min = 50;
      chart.options.scales.x.max = 820;
      chart.options.scales.x.title.text = "Precipitación Acumulada Floración Ago-Oct (mm) · ERA5 (r = 0.751, p = 0.002)";
    }}
    chart.update();
  }}

  function switchJaenViewMode(mode) {{
    const canvas = document.getElementById("chartDemoJaen");
    if (!canvas) return;
    const ctx = canvas.getContext("2d");

    ["btnJaenTraj", "btnJaenBench"].forEach(id => {{
      const b = document.getElementById(id);
      if (b) b.classList.remove("active");
    }});

    if (mode === "benchmark") {{
      document.getElementById("btnJaenBench")?.classList.add("active");
      if (charts["demoJaen"]) {{
        charts["demoJaen"].destroy();
      }}
      const bm = window.DECK_DATA.cafe_benchmark || [];
      charts["demoJaen"] = new Chart(ctx, {{
        type: "bar",
        data: {{
          labels: bm.map(r => r.modelo),
          datasets: [{{
            label: "MAE Walk-Forward (qq/ha)",
            data: bm.map(r => r.mae_walkforward),
            extraData: bm,
            backgroundColor: bm.map(r => {{
              if (r.modelo && r.modelo.includes("Random Forest")) return "#059669";
              if (r.modelo && r.modelo.includes("Déficit Hídrico")) return "#0284C7";
              if (r.modelo && r.modelo.includes("NDVI Anual")) return "#DC2626";
              if (r.familia && r.familia.includes("Baseline")) return "#94A3B8";
              if (r.p_valor_vs_mejor >= 0.05) return "#10B981";
              return "#8B5CF6";
            }})
          }}]
        }},
        options: {{
          indexAxis: "y",
          responsive: true,
          maintainAspectRatio: false,
          plugins: {{
            legend: {{ display: false }},
            tooltip: {{
              callbacks: {{
                label: (ctx) => {{
                  const row = ctx.dataset.extraData ? ctx.dataset.extraData[ctx.dataIndex] : null;
                  if (!row) return `MAE: ${{ctx.raw}} qq/ha`;
                  return [
                    `MAE Walk-Forward: ${{row.mae_walkforward}} qq/ha | RMSE: ${{row.rmse_walkforward}} qq/ha`,
                    `MAPE: ${{row.mape_walkforward}}% | Error en Récord 2020: ${{row.error_abs_2020}} qq/ha`,
                    `Familia: ${{row.familia}} | Hardware: ${{row.hardware}} (${{row.tiempo_ms}} ms)`,
                    `p-valor vs RF: ${{row.p_valor_vs_mejor >= 0.05 ? row.p_valor_vs_mejor + ' (Sin dif. sig.)' : row.p_valor_vs_mejor + ' (Inferior)'}}`
                  ];
                }}
              }}
            }}
          }},
          scales: {{
            x: {{ min: 3.0, max: 9.0, title: {{ display: true, text: "MAE Walk-Forward (qq/ha) — Menor es mejor" }} }}
          }}
        }}
      }});
    }} else {{
      document.getElementById("btnJaenTraj")?.classList.add("active");
      if (charts["demoJaen"]) {{
        charts["demoJaen"].destroy();
      }}
      const d = window.DECK_DATA.cafe_predicciones || window.DECK_DATA.cafe_resultados;
      charts["demoJaen"] = new Chart(ctx, {{
        type: "line",
        data: {{
          labels: d.map(r => r.campania),
          datasets: [
            {{
              label: "Observado Oficial SIEA (qq/ha)",
              data: d.map(r => r.rendimiento_real !== undefined ? r.rendimiento_real : r.rendimiento_obs),
              borderColor: "#FFFFFF",
              borderWidth: 3.2,
              pointRadius: 4.5
            }},
            {{
              label: "M12: Random Forest (Líder MAE 3.72)",
              data: d.map(r => r["M12: Random Forest Parsimonioso (d=2)"] !== undefined ? r["M12: Random Forest Parsimonioso (d=2)"] : r.pred_m4_fusion),
              borderColor: "#059669",
              borderWidth: 2.5,
              pointRadius: 3.5
            }},
            {{
              label: "M08: Solo Déficit Hídrico (MAE 3.90)",
              data: d.map(r => r["M08: Solo Déficit Hídrico Floración"] !== undefined ? r["M08: Solo Déficit Hídrico Floración"] : r.pred_m3_clima),
              borderColor: "#0284C7",
              borderWidth: 2.0,
              borderDash: [4, 3],
              pointRadius: 3
            }},
            {{
              label: "M11: ElasticNet Multimodal (MAE 4.33)",
              data: d.map(r => r["M11: ElasticNet Multimodal (L1+L2)"] !== undefined ? r["M11: ElasticNet Multimodal (L1+L2)"] : r.pred_m4_fusion),
              borderColor: "#8B5CF6",
              borderWidth: 2.0,
              borderDash: [3, 2],
              pointRadius: 2.5
            }},
            {{
              label: "M05: Solo NDVI Anual (Trampa MAE 5.45)",
              data: d.map(r => r["M05: Solo NDVI Anual (Saturado)"] !== undefined ? r["M05: Solo NDVI Anual (Saturado)"] : r.pred_m2_satelite),
              borderColor: "#DC2626",
              borderWidth: 2.2,
              borderDash: [5, 4],
              pointRadius: 3
            }}
          ]
        }},
        options: {{
          responsive: true,
          maintainAspectRatio: false,
          plugins: {{
            legend: {{ position: "top", labels: {{ font: {{ family: "IBM Plex Mono", size: 10.5 }} }} }},
            tooltip: {{
              callbacks: {{
                afterLabel: (ctx) => {{
                  if (ctx.label === "2020") return "⚠️ AÑO RÉCORD NACIONAL (42.5 qq/ha) — Desafío de extrapolación";
                  return "";
                }}
              }}
            }}
          }},
          scales: {{
            y: {{ min: 12, max: 46, title: {{ display: true, text: "Rendimiento (qq/ha)" }} }}
          }}
        }}
      }});
    }}
  }}

  function switchPunchanaView(mode) {{
    const chartBox = document.getElementById("punchanaChartContainer");
    const anatomyBox = document.getElementById("punchanaAnatomyContainer");
    const btnChart = document.getElementById("btnPunchanaChart");
    const btnAnatomy = document.getElementById("btnPunchanaAnatomy");

    if (mode === "anatomy") {{
      if (chartBox) chartBox.style.display = "none";
      if (anatomyBox) anatomyBox.style.display = "flex";
      if (btnChart) btnChart.classList.remove("active");
      if (btnAnatomy) btnAnatomy.classList.add("active");
    }} else {{
      if (anatomyBox) anatomyBox.style.display = "none";
      if (chartBox) chartBox.style.display = "flex";
      if (btnAnatomy) btnAnatomy.classList.remove("active");
      if (btnChart) btnChart.classList.add("active");
      if (charts["benchmark"]) charts["benchmark"].resize();
    }}
  }}

  function switchCafeSystemView(mode) {{
    const chartBox = document.getElementById("cafeChartContainer");
    const anatomyBox = document.getElementById("cafeAnatomyContainer");
    const btnChart = document.getElementById("btnCafeChart");
    const btnAnatomy = document.getElementById("btnCafeAnatomy");

    if (mode === "anatomy") {{
      if (chartBox) chartBox.style.display = "none";
      if (anatomyBox) anatomyBox.style.display = "flex";
      if (btnChart) btnChart.classList.remove("active");
      if (btnAnatomy) btnAnatomy.classList.add("active");
    }} else {{
      if (anatomyBox) anatomyBox.style.display = "none";
      if (chartBox) chartBox.style.display = "flex";
      if (btnAnatomy) btnAnatomy.classList.remove("active");
      if (btnChart) btnChart.classList.add("active");
      if (charts["scatterNdvi"]) charts["scatterNdvi"].resize();
    }}
  }}

  function switchFenologiaView(mode) {{
    const relojBox = document.getElementById("fenologiaRelojContainer");
    const trampasBox = document.getElementById("fenologiaTrampasContainer");
    const btnReloj = document.getElementById("btnFenoReloj");
    const btnTrampas = document.getElementById("btnFenoTrampas");

    if (mode === "trampas") {{
      if (relojBox) relojBox.style.display = "none";
      if (trampasBox) trampasBox.style.display = "flex";
      if (btnReloj) btnReloj.classList.remove("active");
      if (btnTrampas) btnTrampas.classList.add("active");
    }} else {{
      if (trampasBox) trampasBox.style.display = "none";
      if (relojBox) relojBox.style.display = "flex";
      if (btnTrampas) btnTrampas.classList.remove("active");
      if (btnReloj) btnReloj.classList.add("active");
    }}
  }}

  function toggleDataset(dsIndex) {{
    if (!charts["demo7d"]) return;
    const isHidden = charts["demo7d"].isDatasetVisible(dsIndex);
    charts["demo7d"].setDatasetVisibility(dsIndex, !isHidden);
    charts["demo7d"].update();
  }}

  function getSlideFromHash() {{
    const hash = window.location.hash.replace("#", "");
    const num = parseInt(hash, 10);
    return (!isNaN(num) && num >= 1 && num <= totalSlides) ? num : 1;
  }}

  window.addEventListener("DOMContentLoaded", () => {{
    updateSlide(getSlideFromHash());
  }});

  window.addEventListener("hashchange", () => {{
    const s = getSlideFromHash();
    if (s !== currentSlide) {{
      updateSlide(s);
    }}
  }});
</script>
</body>
</html>
"""


def build_deck(output_dir: Path | None = None) -> Path:
    """
    Compila el deck interactivo de 30 diapositivas y retorna la ruta a `index.html`.

    Args:
        output_dir (Path | None, opcional): Directorio destino de compilación. Si es
            `None`, escribe directamente en `BASE_DIR`.

    Returns:
        Path: Ruta al archivo `index.html` generado.
    """
    target_dir = Path(output_dir) if output_dir is not None else BASE_DIR
    target_dir.mkdir(parents=True, exist_ok=True)

    data_payload = _load_deck_data()
    data_json = json.dumps(data_payload, ensure_ascii=False, allow_nan=False)
    notes_json = json.dumps(get_speaker_notes(), ensure_ascii=False, allow_nan=False)

    branding = get_branding()
    for key, candidates in PROTOTYPE_CANDIDATES.items():
        branding[key] = _encode_first_existing(candidates)

    # Carga los diagramas anatómicos SVG generados con Anatomy Framework.
    anatomy_c1_path = BASE_DIR / "front/components/anatomy/anatomy_estacion_vs_malla.svg"
    anatomy_c2_path = BASE_DIR / "front/components/anatomy/anatomy_cafe_sombra_ndvi.svg"
    branding["anatomy_c1_svg"] = (
        anatomy_c1_path.read_text(encoding="utf-8") if anatomy_c1_path.is_file() else ""
    )
    branding["anatomy_c2_svg"] = (
        anatomy_c2_path.read_text(encoding="utf-8") if anatomy_c2_path.is_file() else ""
    )

    css_content = get_deck_css(branding=branding)
    chartjs_local_code = _load_chartjs_bundle()
    slides_p1 = get_slides_part1(branding=branding)
    slides_p2 = get_slides_part2(branding=branding)

    html_content = _render_html_document(
        data_json=data_json,
        notes_json=notes_json,
        branding=branding,
        css_content=css_content,
        slides_p1=slides_p1,
        slides_p2=slides_p2,
        chartjs_local_code=chartjs_local_code,
    )

    presentation_path = target_dir / "presentacion.html"
    presentation_path.write_text(html_content, encoding="utf-8")

    index_path = target_dir / "index.html"
    index_path.write_text(html_content, encoding="utf-8")

    _sync_runtime_assets(target_dir)

    print(
        f"Deck interactivo de 30 diapositivas generado con éxito en: "
        f"{presentation_path} e {index_path} ({len(html_content)} bytes)"
    )
    return index_path


def main() -> None:
    """
    Ejecuta la compilación del deck desde línea de comandos aceptando `--output-dir`.
    """
    parser = argparse.ArgumentParser(
        description="Compila el deck interactivo de la charla 2026-forecasting-ia."
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=None,
        help="Directorio destino donde escribir index.html y presentacion.html.",
    )
    args = parser.parse_args()
    build_deck(output_dir=args.output_dir)


if __name__ == "__main__":
    main()
