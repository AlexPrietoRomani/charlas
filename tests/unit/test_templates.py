"""
Archivo: tests/unit/test_templates.py
Fecha de modificación: 15/11/2026
Autor: Alex Prieto <alexprieto1997@gmail.com>

Descripción:
Valida las plantillas reutilizables `talks/_template_python_deck/` y
`talks/_template_static/` mediante pruebas unitarias de contrato (`discover_talks`
y `load_manifest`) y pruebas de simulación de usuario copiando, descubriendo y
compilando ambas plantillas en un directorio temporal aislado.

Acciones Principales:
    - Comprueba que `discover_talks(Path("talks"))` excluye las carpetas `_template_*`
      y retorna únicamente `["2026-forecasting-ia", "2026-falsa-alarma"]`.
    - Verifica que `load_manifest()` valida los `talk.json` de ambas plantillas al
      renombrar su carpeta temporal para coincidir con su `slug`.
    - Simula el flujo completo de usuario copiando `_template_python_deck`, publicando
      el manifiesto, descubriéndola y compilando `index.html` con `--output-dir`.
    - Simula el flujo de usuario copiando `_template_static`, publicando el manifiesto
      y validándola con `discover_talks()` junto con su `index.html` de 3 diapositivas.

Estructura Interna:
    - `_copy_template_with_updates`: Helper local para clonar una plantilla y ajustar `talk.json`.
    - `test_discover_talks_ignores_templates_and_returns_real_talks`: Prueba unitaria.
    - `test_load_manifest_validates_both_templates_when_folder_matches_slug`: Prueba unitaria.
    - `test_user_simulation_python_deck_template_copy_discover_and_build`: Simulación de usuario.
    - `test_user_simulation_static_template_copy_and_discover`: Simulación de usuario.

Entradas / Dependencias:
    - `shared.manifest` (`discover_talks`, `load_manifest`), `talks/_template_python_deck/`,
      `talks/_template_static/` y `shared/python_deck/assets/chart.umd.min.js`.

Salidas / Efectos:
    - Reporta aprobación o fallo de los criterios de aceptación de la Tarea T1.3.1.

Ejemplo de Integración:
    python -m pytest tests/unit/test_templates.py -v
"""

import json
import re
import shutil
import subprocess
import sys
from pathlib import Path

import pytest

from shared.manifest import discover_talks, load_manifest

REPO_ROOT: Path = Path(__file__).resolve().parents[2]
TALKS_ROOT: Path = REPO_ROOT / "talks"
TEMPLATE_PYTHON_DIR: Path = TALKS_ROOT / "_template_python_deck"
TEMPLATE_STATIC_DIR: Path = TALKS_ROOT / "_template_static"


def _copy_template_with_updates(
    source_dir: Path,
    target_dir: Path,
    *,
    slug: str | None = None,
    draft: bool | None = None,
) -> Path:
    """
    Copia una plantilla hacia `target_dir` y actualiza opcionalmente su `talk.json`.

    Args:
        source_dir (Path): Directorio origen de la plantilla.
        target_dir (Path): Directorio destino de la copia temporal.
        slug (str | None, opcional): Nuevo `slug` a escribir en `talk.json`.
        draft (bool | None, opcional): Nuevo valor booleano para `draft` en `talk.json`.

    Returns:
        Path: Ruta al directorio copiado.
    """
    shutil.copytree(source_dir, target_dir)
    manifest_path = target_dir / "talk.json"
    payload = json.loads(manifest_path.read_text(encoding="utf-8"))

    if slug is not None:
        payload["slug"] = slug
    if draft is not None:
        payload["draft"] = draft

    manifest_path.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    return target_dir


def test_discover_talks_ignores_templates_and_returns_real_talks() -> None:
    """
    Verifica que `discover_talks(Path("talks"))` ignora `_template_*` y devuelve solo las charlas activas.
    """
    assert TEMPLATE_PYTHON_DIR.is_dir(), "Falta talks/_template_python_deck/"
    assert TEMPLATE_STATIC_DIR.is_dir(), "Falta talks/_template_static/"

    discovered = discover_talks(TALKS_ROOT)
    slugs = [talk.slug for talk in discovered]

    assert slugs == ["2026-sdd-proyectos-reales", "2026-forecasting-ia", "2026-falsa-alarma"]


@pytest.mark.parametrize(
    ("template_dir", "expected_engine"),
    [
        (TEMPLATE_PYTHON_DIR, "python-deck"),
        (TEMPLATE_STATIC_DIR, "static"),
    ],
)
def test_load_manifest_validates_both_templates_when_folder_matches_slug(
    tmp_path: Path,
    template_dir: Path,
    expected_engine: str,
) -> None:
    """
    Verifica que `load_manifest()` valida ambas plantillas cuando su carpeta coincide con `slug`.
    """
    raw_manifest = json.loads((template_dir / "talk.json").read_text(encoding="utf-8"))
    template_slug = raw_manifest["slug"]

    copied_dir = _copy_template_with_updates(template_dir, tmp_path / template_slug)
    manifest = load_manifest(copied_dir)

    assert manifest.slug == template_slug
    assert manifest.engine == expected_engine
    assert manifest.entry == "index.html"
    assert manifest.cover == "cover.svg"
    assert manifest.draft is True
    assert manifest.slides_count == 3
    assert (copied_dir / "cover.svg").is_file()
    assert (copied_dir / "README.md").is_file()


def test_user_simulation_python_deck_template_copy_discover_and_build(
    tmp_path: Path,
) -> None:
    """
    Simula a un usuario copiando `_template_python_deck`, descubriéndola y compilándola con `--output-dir`.
    """
    talks_sandbox = tmp_path / "talks"
    talks_sandbox.mkdir(parents=True, exist_ok=True)

    demo_dir = _copy_template_with_updates(
        TEMPLATE_PYTHON_DIR,
        talks_sandbox / "2027-demo-py",
        slug="2027-demo-py",
        draft=False,
    )

    discovered = discover_talks(talks_sandbox)
    assert [talk.slug for talk in discovered] == ["2027-demo-py"]
    assert discovered[0].engine == "python-deck"

    output_dir = tmp_path / "_site" / "2027-demo-py"
    result = subprocess.run(
        [
            sys.executable,
            str(demo_dir / "back" / "build_deck.py"),
            "--output-dir",
            str(output_dir),
        ],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == 0, f"Falló build_deck.py:\n{result.stdout}\n{result.stderr}"

    compiled_html = output_dir / "index.html"
    assert compiled_html.is_file(), "No se generó index.html en output_dir"

    html_text = compiled_html.read_text(encoding="utf-8")
    assert len(html_text) > 100_000, "Se esperaba Chart.js embebido dentro de index.html"

    slide_matches = re.findall(r'<section class="slide[^"]*" data-index="(\d+)"', html_text)
    assert slide_matches == ["1", "2", "3"]

    assert "Chart.defaults" in html_text
    assert "new Chart(" in html_text
    assert "window.DECK_DATA" in html_text
    assert "speakerDrawer" in html_text
    assert "ArrowRight" in html_text and "ArrowLeft" in html_text
    assert "Alex Prieto Romani" in html_text
    assert "data_wizard_badge" not in html_text


def test_user_simulation_static_template_copy_and_discover(tmp_path: Path) -> None:
    """
    Simula a un usuario copiando `_template_static`, publicando su `talk.json` y validándola.
    """
    talks_sandbox = tmp_path / "talks"
    talks_sandbox.mkdir(parents=True, exist_ok=True)

    demo_dir = _copy_template_with_updates(
        TEMPLATE_STATIC_DIR,
        talks_sandbox / "2027-demo-static",
        slug="2027-demo-static",
        draft=False,
    )

    discovered = discover_talks(talks_sandbox)
    assert [talk.slug for talk in discovered] == ["2027-demo-static"]
    assert discovered[0].engine == "static"
    assert discovered[0].entry == "index.html"

    index_path = demo_dir / "index.html"
    assert index_path.is_file()
    html_text = index_path.read_text(encoding="utf-8")

    slide_matches = re.findall(r'<section class="slide[^"]*" data-index="(\d+)"', html_text)
    assert slide_matches == ["1", "2", "3"]
    assert "ArrowRight" in html_text and "ArrowLeft" in html_text
    assert "#F8FAFC" in html_text
    assert "Alex Prieto Romani" in html_text
