"""
Archivo: tests/unit/test_talk_forecasting.py
Fecha de modificación: 15/11/2026
Autor: Alex Prieto <alexprieto1997@gmail.com>

Descripción:
Valida la migración de la charla `2026-forecasting-ia` hacia `talks/2026-forecasting-ia/`,
comprobando el contrato de su manifiesto `talk.json`, la extracción de `chart.umd.min.js`
hacia `shared/python_deck/assets/`, la presencia de los datasets reales y la compilación
autónoma mediante `build_deck` con soporte `--output-dir`.

Acciones Principales:
    - Valida `load_manifest(Path("talks/2026-forecasting-ia"))`.
    - Comprueba la existencia de `shared/python_deck/assets/chart.umd.min.js` y CSV/JSON reales.
    - Verifica exclusión de archivos prohibidos dentro de la charla migrada.
    - Simula la compilación del usuario con `build_deck(output_dir=tmp_path)` y vía CLI
      `--output-dir`, validando tamaño, `window.DECK_DATA`, `Chart` y ausencia de `NaN`.

Estructura Interna:
    - `_load_talk_build_module`: Carga dinámicamente `back/build_deck.py` de la charla.
    - `_extract_deck_data_json`: Extrae el bloque JSON crudo asignado a `window.DECK_DATA`.
    - `test_manifest_and_shared_assets_valid`: Prueba unitaria de manifiesto y activos.
    - `test_talk_excludes_forbidden_root_artifacts`: Prueba unitaria de higiene de migración.
    - `test_user_simulation_build_deck_to_output_dir`: Simulación vía Python API.
    - `test_user_simulation_cli_proxy_output_dir`: Simulación vía CLI `--output-dir`.

Entradas / Dependencias:
    - `shared.manifest.load_manifest`, `talks/2026-forecasting-ia/`, `shared/python_deck/assets/`.

Salidas / Efectos:
    - Reporta aprobación o fallo de los criterios de aceptación de la Tarea T1.1.1.

Ejemplo de Integración:
    python -m pytest tests/unit/test_talk_forecasting.py -v
"""

import importlib.util
import json
import re
import subprocess
import sys
from pathlib import Path
from types import ModuleType

import pandas as pd

from shared.manifest import load_manifest

REPO_ROOT: Path = Path(__file__).resolve().parents[2]
TALK_DIR: Path = REPO_ROOT / "talks" / "2026-forecasting-ia"
SHARED_CHARTJS_PATH: Path = (
    REPO_ROOT / "shared" / "python_deck" / "assets" / "chart.umd.min.js"
)

EXPECTED_DATA_FILES: tuple[str, ...] = (
    "data/caso_1/benchmark_punchana.csv",
    "data/caso_1/senamhi_forecast_7d.csv",
    "data/caso_1/experimento_extrapolacion.csv",
    "data/caso_1/noaa_ecmwf_forecast.csv",
    "data/caso_1/senamhi_diario.csv",
    "data/caso_2/cafe_jaen_campanias.csv",
    "data/caso_2/cafe_jaen_resultados.csv",
    "data/caso_2/benchmark_cafe.csv",
    "data/caso_2/cafe_jaen_predicciones_modelos.csv",
    "data/caso_2/cafe_jaen_hipotesis.json",
)

MIN_HTML_BYTES: int = 500 * 1024


def _load_talk_build_module() -> ModuleType:
    """
    Importa dinámicamente el módulo `back/build_deck.py` de `talks/2026-forecasting-ia/`.

    Returns:
        ModuleType: Módulo cargado listo para invocar `build_deck`.
    """
    module_path = TALK_DIR / "back" / "build_deck.py"
    spec = importlib.util.spec_from_file_location("talk_2026_build_deck", module_path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _extract_deck_data_json(html_text: str) -> str:
    """
    Extrae la cadena JSON asignada a `window.DECK_DATA` dentro del HTML compilado.

    Args:
        html_text (str): Contenido completo de `index.html` o `presentacion.html`.

    Returns:
        str: Cadena JSON cruda asignada a `window.DECK_DATA`.
    """
    match = re.search(
        r"window\.DECK_DATA\s*=\s*(\{.*?\});\s*</script>",
        html_text,
        flags=re.DOTALL,
    )
    assert match is not None, "No se encontró el bloque `window.DECK_DATA = {...};` en el HTML."
    return match.group(1)


def test_manifest_and_shared_assets_valid() -> None:
    """
    Verifica el manifiesto `talk.json`, `chart.umd.min.js` compartido y los CSV/JSON de datos.
    """
    manifest = load_manifest(TALK_DIR)

    assert manifest.slug == "2026-forecasting-ia"
    assert manifest.engine == "python-deck"
    assert manifest.entry == "index.html"
    assert manifest.cover == "docs/images/front/bg_cover_official.png"
    assert manifest.slides_count == 31
    assert manifest.duration_min == 35
    assert manifest.tags == ("Forecasting", "ML/DL", "SENAMHI", "NDVI")
    assert "notebooks" in manifest.extras

    assert SHARED_CHARTJS_PATH.is_file(), "Falta chart.umd.min.js en shared/python_deck/assets/"
    assert SHARED_CHARTJS_PATH.stat().st_size > 100_000

    for rel_path in EXPECTED_DATA_FILES:
        file_path = TALK_DIR / rel_path
        assert file_path.is_file(), f"Falta archivo de datos esperado: {rel_path}"
        if file_path.suffix == ".csv":
            df = pd.read_csv(file_path)
            assert not df.empty, f"El CSV {rel_path} está vacío"
        else:
            payload = json.loads(file_path.read_text(encoding="utf-8"))
            assert payload, f"El JSON {rel_path} está vacío"


def test_talk_excludes_forbidden_root_artifacts() -> None:
    """
    Comprueba que la carpeta migrada excluye secretos, cachés y documentación de raíz del repo.
    """
    forbidden_paths = (
        TALK_DIR / "scripts" / "test_nlm_auth.py",
        TALK_DIR / "docs" / "description_proyecto.md",
        TALK_DIR / "docs" / "architecture",
        TALK_DIR / "docs" / "db",
        TALK_DIR / "docs" / "ejecucion.md",
        TALK_DIR / "docs" / "plan",
        TALK_DIR / "docs" / "task",
        TALK_DIR / "docs" / "logs" / "recibos",
    )
    for forbidden in forbidden_paths:
        assert not forbidden.exists(), f"Archivo o directorio prohibido copiado: {forbidden}"

    assert (TALK_DIR / "docs" / "logs" / "log.md").is_file()
    assert (TALK_DIR / "docs" / "PLANTILLA PONENTES.pptx").is_file()
    assert (TALK_DIR / "refs.bib").is_file()


def test_user_simulation_build_deck_to_output_dir(tmp_path: Path) -> None:
    """
    Simula la compilación directa del deck hacia `tmp_path` mediante `build_deck(output_dir=...)`.
    """
    build_module = _load_talk_build_module()
    assert build_module.BASE_DIR == TALK_DIR.resolve()
    assert build_module.REPO_ROOT == REPO_ROOT.resolve()

    out_dir = tmp_path / "dist_forecasting"
    result_path = build_module.build_deck(output_dir=out_dir)

    index_path = out_dir / "index.html"
    presentation_path = out_dir / "presentacion.html"
    assert result_path == index_path
    assert index_path.is_file()
    assert presentation_path.is_file()
    assert index_path.stat().st_size > MIN_HTML_BYTES
    assert presentation_path.stat().st_size > MIN_HTML_BYTES

    html_text = index_path.read_text(encoding="utf-8")
    assert "window.DECK_DATA" in html_text
    assert "Chart.defaults" in html_text
    assert "IQUITOS" in html_text and "DATA FEST 2026" in html_text
    assert 'data-index="31"' in html_text

    raw_deck_json = _extract_deck_data_json(html_text)
    assert re.search(r"(?<!\")\bNaN\b(?!\")", raw_deck_json) is None, (
        "Se detectó NaN sin comillas dentro de window.DECK_DATA."
    )
    parsed_data = json.loads(raw_deck_json)
    for expected_key in (
        "benchmark",
        "forecast_7d",
        "extrapolacion",
        "cafe_campanias",
        "cafe_resultados",
        "cafe_benchmark",
        "cafe_predicciones",
        "hipotesis_cafe",
        "noaa_ecmwf",
        "senamhi_reciente",
    ):
        assert expected_key in parsed_data
        assert len(parsed_data[expected_key]) > 0


def test_user_simulation_cli_proxy_output_dir(tmp_path: Path) -> None:
    """
    Simula la ejecución por CLI del proxy `scripts/build_deck.py --output-dir`.
    """
    cli_out_dir = tmp_path / "cli_out"
    proxy_script = TALK_DIR / "scripts" / "build_deck.py"

    proc = subprocess.run(
        [sys.executable, str(proxy_script), "--output-dir", str(cli_out_dir)],
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

    raw_deck_json = _extract_deck_data_json(index_path.read_text(encoding="utf-8"))
    assert re.search(r"(?<!\")\bNaN\b(?!\")", raw_deck_json) is None
    assert json.loads(raw_deck_json)["benchmark"]
