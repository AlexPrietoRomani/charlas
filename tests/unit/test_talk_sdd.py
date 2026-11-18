"""
Archivo: tests/unit/test_talk_sdd.py
Fecha de modificación: 15/11/2026
Autor: Alex Prieto <alexprieto1997@gmail.com>

Descripción:
Valida la charla `2026-sdd-proyectos-reales` (taller de 2 horas, motor
`python-deck`), comprobando el contrato de su manifiesto `talk.json`, la
portada SVG ejecutiva, los módulos `front/` con la estética gerencial clara,
la gráfica offline compartida `shared/python_deck/assets/chart.umd.min.js` y
la compilación autocontenida mediante `build_deck` con soporte `--output-dir`.

Acciones Principales:
    - Valida `load_manifest(Path("talks/2026-sdd-proyectos-reales"))`.
    - Comprueba portada `assets/cover.svg` (1200x630) y `chart.umd.min.js` compartido.
    - Verifica la coreografía en el HTML: `data-index`, barra por bloques, atajos
      (N/G/F), fragmentos `data-step`, SVG animados y notas del orador con tiempos.
    - Simula la compilación con `build_deck(output_dir=tmp_path)` y vía CLI
      `--output-dir`, validando tamaño, Chart.js incrustado y ausencia de NaN/errores.

Estructura Interna:
    - `_load_talk_build_module`: Carga dinámicamente `back/build_deck.py` de la charla.
    - `_extract_window_json`: Extrae el JSON de un `window.X = {...};` del HTML.
    - `test_manifest_and_talk_assets_valid`: Prueba unitaria de manifiesto y activos.
    - `test_front_modules_expose_required_content`: Prueba unitaria de módulos front.
    - `test_user_simulation_build_deck_to_output_dir`: Simulación vía Python API.
    - `test_user_simulation_cli_proxy_output_dir`: Simulación vía CLI `--output-dir`.

Entradas / Dependencias:
    - `shared.manifest.load_manifest`, `talks/2026-sdd-proyectos-reales/`,
      `shared/python_deck/assets/chart.umd.min.js`.

Salidas / Efectos:
    - Reporta aprobación o fallo de los criterios de aceptación de la charla.

Ejemplo de Integración:
    python -m pytest tests/unit/test_talk_sdd.py -v
"""

import importlib.util
import json
import re
import subprocess
import sys
from pathlib import Path
from types import ModuleType

from shared.manifest import load_manifest

REPO_ROOT: Path = Path(__file__).resolve().parents[2]
TALK_DIR: Path = REPO_ROOT / "talks" / "2026-sdd-proyectos-reales"
SHARED_CHARTJS_PATH: Path = (
    REPO_ROOT / "shared" / "python_deck" / "assets" / "chart.umd.min.js"
)

EXPECTED_SLIDES_COUNT: int = 27
EXPECTED_BLOCKS: tuple[int, ...] = (1, 2, 3, 4, 5)
EXPECTED_CHARTS: tuple[str, ...] = ("coste_verificacion", "caso_auc")

MIN_HTML_BYTES: int = 180 * 1024


def _load_talk_build_module() -> ModuleType:
    """
    Importa dinámicamente el módulo `back/build_deck.py` de `2026-sdd-proyectos-reales`.

    Returns:
        ModuleType: Módulo cargado listo para invocar `build_deck`.
    """
    module_path = TALK_DIR / "back" / "build_deck.py"
    spec = importlib.util.spec_from_file_location("talk_sdd_build_deck", module_path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _extract_window_json(html_text: str, var_name: str) -> str:
    """
    Extrae la cadena JSON asignada a `window.<var>` dentro del HTML compilado.

    Args:
        html_text (str): Contenido completo de `index.html` o `presentacion.html`.
        var_name (str): Nombre de la variable global (`DECK_META`, `SPEAKER_NOTES`,
            `CHART_SPECS`).

    Returns:
        str: Cadena JSON cruda asignada a la variable global.
    """
    pattern = r"window\." + re.escape(var_name) + r"\s*=\s*(\{.*?\}|\[.*?\]);\s*</script>"
    match = re.search(pattern, html_text, flags=re.DOTALL)
    assert match is not None, (
        f"No se encontró el bloque `window.{var_name} = ...;` en el HTML."
    )
    return match.group(1)


def _no_unquoted_nan(payload_text: str) -> None:
    """
    Afirma que no exista el literal `NaN` sin comillas dentro de un JSON crudo.

    Args:
        payload_text (str): Cadena JSON extraída del HTML compilado.
    """
    assert re.search(r"(?<!\")\bNaN\b(?!\")", payload_text) is None, (
        "Se detectó NaN sin comillas dentro del JSON incrustado."
    )


def test_manifest_and_talk_assets_valid() -> None:
    """
    Verifica el manifiesto `talk.json`, la portada SVG y `chart.umd.min.js` compartido.
    """
    manifest = load_manifest(TALK_DIR)

    assert manifest.slug == "2026-sdd-proyectos-reales"
    assert manifest.title == "Aplicación de SDD en proyectos reales"
    assert manifest.engine == "python-deck"
    assert manifest.entry == "index.html"
    assert manifest.cover == "assets/cover.svg"
    assert manifest.slides_count == EXPECTED_SLIDES_COUNT
    assert manifest.duration_min == 120
    assert manifest.date == "2026-11-14"
    assert manifest.tags == ("SDD", "ODD", "EGM", "Web", "Data Science", "project-suite")

    cover_path = TALK_DIR / "assets" / "cover.svg"
    assert cover_path.is_file(), "Falta la portada assets/cover.svg"
    cover_text = cover_path.read_text(encoding="utf-8")
    assert "<svg" in cover_text
    assert "1200" in cover_text and "630" in cover_text, (
        "La portada SVG debe medir 1200x630"
    )

    for rel_path in (
        "front/styles.py",
        "front/slides_p1.py",
        "front/slides_p2.py",
        "front/notes.py",
        "back/build_deck.py",
    ):
        assert (TALK_DIR / rel_path).is_file(), f"Falta el archivo de la charla: {rel_path}"

    assert SHARED_CHARTJS_PATH.is_file(), "Falta chart.umd.min.js en shared/python_deck/assets/"
    assert SHARED_CHARTJS_PATH.stat().st_size > 100_000


def test_front_modules_expose_required_content() -> None:
    """
    Comprueba que los módulos `front/` exponen las 24 diapositivas, 5 bloques,
    notas con tiempos y las dos especificaciones Chart.js.
    """
    build_module = _load_talk_build_module()

    slides = build_module._merge_slides()
    assert len(slides) == EXPECTED_SLIDES_COUNT

    blocks = build_module._compute_blocks(slides)
    assert tuple(b["block"] for b in blocks) == EXPECTED_BLOCKS
    assert blocks[0]["from"] == 0 and blocks[-1]["to"] == 120

    notes_module_path = TALK_DIR / "front" / "notes.py"
    spec = importlib.util.spec_from_file_location("sdd_notes_test", notes_module_path)
    assert spec is not None and spec.loader is not None
    notes_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(notes_module)

    missing_notes = [
        slide["id"] for slide in slides if slide["id"] not in notes_module.NOTES
    ]
    assert not missing_notes, f"Diapositivas sin notas del orador: {missing_notes}"

    p2_spec = importlib.util.spec_from_file_location(
        "sdd_slides_p2_test", TALK_DIR / "front" / "slides_p2.py"
    )
    assert p2_spec is not None and p2_spec.loader is not None
    p2_module = importlib.util.module_from_spec(p2_spec)
    p2_spec.loader.exec_module(p2_module)

    for chart_name in EXPECTED_CHARTS:
        spec_cfg = p2_module.CHART_SPECS[chart_name]
        assert spec_cfg["type"] in ("bar", "line")
        assert all(
            value == value for ds in spec_cfg["data"]["datasets"] for value in ds["data"]
        ), f"La gráfica {chart_name} contiene NaN"


def test_user_simulation_build_deck_to_output_dir(tmp_path: Path) -> None:
    """
    Simula la compilación directa del deck hacia `tmp_path` mediante `build_deck(output_dir=...)`.
    """
    build_module = _load_talk_build_module()
    assert build_module.BASE_DIR == TALK_DIR.resolve()
    assert build_module.REPO_ROOT == REPO_ROOT.resolve()

    out_dir = tmp_path / "dist_sdd"
    result_path = build_module.build_deck(output_dir=out_dir)

    index_path = out_dir / "index.html"
    presentation_path = out_dir / "presentacion.html"
    assert result_path == index_path
    assert index_path.is_file()
    assert presentation_path.is_file()
    assert index_path.stat().st_size > MIN_HTML_BYTES
    assert presentation_path.stat().st_size > MIN_HTML_BYTES

    html_text = index_path.read_text(encoding="utf-8")
    assert "Aplicación de SDD en proyectos reales" in html_text
    assert "chart.umd.min.js" in html_text or "Chart.defaults" in html_text

    # data-index: 24 secciones 1..24 y ninguna fuera de rango
    indexes = re.findall(r'<section class="slide[^"]*" data-index="(\d+)"', html_text)
    assert [int(i) for i in indexes] == list(range(1, EXPECTED_SLIDES_COUNT + 1))
    assert f'data-index="{EXPECTED_SLIDES_COUNT}"' in html_text

    # 5 bloques en la barra de progreso
    seg_blocks = re.findall(r'<div class="seg" data-block="(\d+)"', html_text)
    assert [int(b) for b in seg_blocks] == list(EXPECTED_BLOCKS)

    # Atajos de teclado y fragmentos progresivos
    for key_hint in ("'ArrowRight'", "'ArrowLeft'", "'n'", "'g'", "'f'"):
        assert key_hint in html_text, f"Falta el atajo de teclado {key_hint}"
    assert html_text.count("data-step=") >= 30, "Faltan fragmentos progresivos data-step"

    # Estética Bento gerencial
    for bento_marker in (
        "radial-gradient(#CBD5E1 1px",
        "background-size: 24px 24px",
        ".38s var(--spring)",
        "cubic-bezier(.16, 1, .3, 1)",
        "z-index: 2",
        "border-radius: 16px",
        "0 4px 20px rgba(15,23,42,.04)",
    ):
        assert bento_marker in html_text, f"Falta el marcador Bento en el CSS: {bento_marker}"

    # Diapo 5: Bento Dashboard a ancho completo con los dos carriles
    assert "Carril 1" in html_text and "Carril 2" in html_text
    assert "El salto 1" in html_text and "El salto 2" in html_text and "El salto 3" in html_text

    # Láminas de EJERCICIO EN VIVO · IR AL TERMINAL (prácticas 1, 2 y 3)
    assert html_text.count("EJERCICIO EN VIVO · IR AL TERMINAL") == 3
    assert html_text.count("t-dot g") == 3, "Cada lámina de práctica lleva su terminal oscura"
    assert "Práctica 1" in html_text and "Práctica 2" in html_text and "Práctica 3" in html_text

    # SVG animados (elefante/goldfish, comparativa AUC) y datos reales del laboratorio
    assert "animateMotion" in html_text
    assert "ELEFANTE" in html_text and "GOLDFISH" in html_text
    assert "AUC 0.9593" in html_text and "AUC 0.8318" in html_text
    assert "1,203 clientes" in html_text and "0.1275" in html_text
    assert "post_churn_cancellation_days" in html_text
    assert "AndinaTel" not in html_text and "50.000" not in html_text

    # Caso Web (AgroVision) y ecosistema Gentle-AI (antecedente de ODD)
    assert "AgroVision" in html_text and "T10.4.1" in html_text
    assert "Gentle-AI" in html_text and "Engram" in html_text
    assert "Alan Buscaglia" in html_text
    assert "X-User-Supabase-Url" in html_text and "SSRF" in html_text
    assert "backend-standards" in html_text and "astro-standards" in html_text

    # Metadatos, notas del orador y specs de gráficas sin NaN
    meta_json = _extract_window_json(html_text, "DECK_META")
    _no_unquoted_nan(meta_json)
    meta = json.loads(meta_json)
    assert meta["total"] == EXPECTED_SLIDES_COUNT
    assert [b["block"] for b in meta["blocks"]] == list(EXPECTED_BLOCKS)
    assert meta["blocks"][0]["from"] == 0 and meta["blocks"][-1]["to"] == 120

    notes_json = _extract_window_json(html_text, "SPEAKER_NOTES")
    _no_unquoted_nan(notes_json)
    notes = json.loads(notes_json)
    assert len(notes) == EXPECTED_SLIDES_COUNT
    assert all(
        note["body"].strip() and "min" in note["time"] and "Bloque" in note["time"]
        for note in notes
    ), "Cada nota del orador debe incluir tiempos por bloque"

    specs_json = _extract_window_json(html_text, "CHART_SPECS")
    _no_unquoted_nan(specs_json)
    specs = json.loads(specs_json)
    for chart_name in EXPECTED_CHARTS:
        assert chart_name in specs
        assert f'data-chart="{chart_name}"' in html_text

    # Ausencia de errores de compilación comunes
    assert "Traceback" not in html_text
    assert "__CSS__" not in html_text and "__ENGINE__" not in html_text


def test_user_simulation_cli_proxy_output_dir(tmp_path: Path) -> None:
    """
    Simula la ejecución por CLI del compilador `back/build_deck.py --output-dir`.
    """
    cli_out_dir = tmp_path / "cli_out_sdd"
    build_script = TALK_DIR / "back" / "build_deck.py"

    proc = subprocess.run(
        [sys.executable, str(build_script), "--output-dir", str(cli_out_dir)],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
        check=False,
    )

    assert proc.returncode == 0, f"Falló CLI build_deck.py:\n{proc.stdout}\n{proc.stderr}"
    index_path = cli_out_dir / "index.html"
    presentation_path = cli_out_dir / "presentacion.html"
    assert index_path.is_file()
    assert presentation_path.is_file()
    assert index_path.stat().st_size > MIN_HTML_BYTES

    html_text = index_path.read_text(encoding="utf-8")
    raw_meta_json = _extract_window_json(html_text, "DECK_META")
    _no_unquoted_nan(raw_meta_json)
    assert json.loads(raw_meta_json)["total"] == EXPECTED_SLIDES_COUNT
    notes = json.loads(_extract_window_json(html_text, "SPEAKER_NOTES"))
    assert len(notes) == EXPECTED_SLIDES_COUNT
