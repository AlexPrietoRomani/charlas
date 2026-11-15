"""
Archivo: tests/unit/test_hub_builder.py
Fecha de modificación: 15/11/2026
Autor: Alex Prieto <alexprieto1997@gmail.com>

Descripción:
Valida la generación del Hub selector (`hub/build_hub.py`, `hub/template.html` y
`hub/assets/`) mediante pruebas unitarias con fixtures y una simulación de usuario
sobre las charlas reales descubiertas en `talks/`.

Acciones Principales:
    - Comprueba la creación de `index.html`, `talks.json`, `profile_alex.jpg` y portadas.
    - Verifica la identidad personal pura de Alex Prieto Romani sin `data_wizard_badge`.
    - Valida el escape XSS de `</` en el JSON embebido y la normalización de `base_path`.
    - Simula el flujo real con `discover_talks(Path("talks"))` verificando cada activo referido.

Estructura Interna:
    - `_create_fixture_talk`: Helper local para materializar un `TalkManifest` y su portada.
    - `_extract_embedded_catalog`: Extrae y decodifica el JSON incrustado en `index.html`.
    - `test_build_hub_*`: Pruebas unitarias de contrato y seguridad.
    - `test_user_simulation_*`: Simulación end-to-end sobre el catálogo real.

Entradas / Dependencias:
    - `hub.build_hub.build_hub` y `shared.manifest` (`TalkManifest`, `discover_talks`).

Salidas / Efectos:
    - Reporta aprobación o fallo de los criterios de aceptación de la Tarea T2.1.1.

Ejemplo de Integración:
    python -m pytest tests/unit/test_hub_builder.py -v
"""

import json
from pathlib import Path
import re
from typing import Any

from hub.build_hub import build_hub
from shared.manifest import TalkManifest, discover_talks


def _create_fixture_talk(
    root: Path,
    slug: str,
    title: str,
    engine: str,
    date_str: str,
    cover_filename: str | None = "cover.png",
    subtitle: str | None = "Resumen de prueba",
) -> TalkManifest:
    """
    Crea una carpeta de charla fixture en `root` y devuelve su `TalkManifest`.

    Args:
        root (Path): Directorio temporal donde se crea la carpeta de la charla.
        slug (str): Identificador kebab-case de la charla.
        title (str): Título de la charla fixture.
        engine (str): Motor asignado (`python-deck`, `astro`, `static` o `custom`).
        date_str (str): Fecha ISO `YYYY-MM-DD`.
        cover_filename (str | None, opcional): Nombre de portada relativa a crear.
        subtitle (str | None, opcional): Subtítulo descriptivo de la charla.

    Returns:
        TalkManifest: Instancia de manifiesto lista para pasar a `build_hub()`.
    """
    talk_dir = root / slug
    talk_dir.mkdir(parents=True, exist_ok=True)

    cover_rel: str | None = None
    if cover_filename is not None:
        cover_file = talk_dir / cover_filename
        cover_file.parent.mkdir(parents=True, exist_ok=True)
        cover_file.write_bytes(b"FAKE_IMAGE_BYTES")
        cover_rel = cover_filename

    return TalkManifest(
        slug=slug,
        title=title,
        subtitle=subtitle,
        event="Evento Demo 2026",
        date=date_str,
        engine=engine,
        tags=("Forecasting", "Python"),
        entry="index.html",
        cover=cover_rel,
        slides_count=12,
        duration_min=20,
        talk_dir=talk_dir,
    )


def _extract_embedded_catalog(index_html: str) -> dict[str, Any]:
    """
    Extrae y parsea el bloque `<script id="catalog-data">` del HTML generado.

    Args:
        index_html (str): Contenido completo de `index.html`.

    Returns:
        dict[str, Any]: Diccionario decodificado del catálogo embebido.
    """
    match = re.search(
        r'<script id="catalog-data" type="application/json">(.*?)</script>',
        index_html,
        flags=re.DOTALL,
    )
    assert match is not None, "No se encontró el bloque <script id='catalog-data'>."
    return json.loads(match.group(1))


def test_build_hub_generates_expected_artifacts_and_branding(tmp_path: Path) -> None:
    """
    Verifica que `build_hub()` genera `index.html`, `talks.json`, avatar y portadas válidas.
    """
    talks_root = tmp_path / "talks"
    talk_one = _create_fixture_talk(
        root=talks_root,
        slug="2026-demo-python",
        title="Charla Uno Python",
        engine="python-deck",
        date_str="2026-10-01",
        cover_filename="assets/cover_one.png",
    )
    talk_two = _create_fixture_talk(
        root=talks_root,
        slug="2026-demo-astro",
        title="Charla Dos Astro",
        engine="astro",
        date_str="2026-08-15",
        cover_filename="public/cover_two.jpg",
    )

    out_dir = tmp_path / "_site"
    generated_index = build_hub(
        talks=[talk_one, talk_two],
        out_dir=out_dir,
        base_path="/charlas",
    )

    assert generated_index == out_dir / "index.html"
    assert generated_index.is_file()
    assert (out_dir / "talks.json").is_file()
    assert (out_dir / "hub_assets" / "profile_alex.jpg").is_file()
    assert (out_dir / "hub_assets" / "2026-demo-python_cover.png").is_file()
    assert (out_dir / "hub_assets" / "2026-demo-astro_cover.jpg").is_file()

    html_content = generated_index.read_text(encoding="utf-8")
    assert "Alex Prieto Romani" in html_content
    assert "hub_assets/profile_alex.jpg" in html_content
    assert "data_wizard_badge" not in html_content
    assert "Data_Wizard" not in html_content

    catalog = json.loads((out_dir / "talks.json").read_text(encoding="utf-8"))
    assert catalog["total_talks"] == 2
    assert catalog["base_path"] == "/charlas"
    assert catalog["generated_at"].endswith("Z")
    assert [item["slug"] for item in catalog["talks"]] == [
        "2026-demo-python",
        "2026-demo-astro",
    ]
    assert catalog["talks"][0]["cover_url"] == "hub_assets/2026-demo-python_cover.png"
    assert catalog["talks"][0]["url"] == "/charlas/2026-demo-python/"
    assert catalog["talks"][0]["manifest"]["slug"] == "2026-demo-python"
    assert "url" not in catalog["talks"][0]["manifest"]


def test_build_hub_escapes_script_tags_and_handles_root_base_path(tmp_path: Path) -> None:
    """
    Comprueba el escape XSS de `</` en JSON embebido y la normalización con `base_path='/'`.
    """
    talks_root = tmp_path / "talks"
    talk_xss = _create_fixture_talk(
        root=talks_root,
        slug="2026-xss-check",
        title="Charla con </script> seguro",
        engine="static",
        date_str="2026-09-10",
        cover_filename=None,
        subtitle="Texto </script><img src=x>",
    )

    out_dir = tmp_path / "_site_root"
    index_path = build_hub(talks=[talk_xss], out_dir=out_dir, base_path="/")

    html_content = index_path.read_text(encoding="utf-8")
    assert "<\\/script>" in html_content

    embedded_catalog = _extract_embedded_catalog(html_content)
    assert embedded_catalog["base_path"] == "/"
    assert embedded_catalog["total_talks"] == 1
    assert embedded_catalog["talks"][0]["title"] == "Charla con </script> seguro"
    assert embedded_catalog["talks"][0]["cover_url"] is None
    assert embedded_catalog["talks"][0]["url"] == "/2026-xss-check/"


def test_user_simulation_hub_with_real_talks_and_existing_assets(tmp_path: Path) -> None:
    """
    Simula al usuario compilando el Hub real desde `talks/` y verifica que todo activo existe.
    """
    real_talks = discover_talks(Path("talks"))
    assert len(real_talks) >= 2

    out_dir = tmp_path / "_site"
    index_path = build_hub(talks=real_talks, out_dir=out_dir, base_path="/charlas")

    html_content = index_path.read_text(encoding="utf-8")
    assert "Alex Prieto Romani" in html_content
    assert "data_wizard_badge" not in html_content
    assert "Data_Wizard" not in html_content

    # Verifica que todas las rutas locales a `hub_assets/` declaradas en el HTML existen en disco.
    referenced_assets = set(re.findall(r'hub_assets/[A-Za-z0-9_.-]+', html_content))
    assert "hub_assets/profile_alex.jpg" in referenced_assets
    for rel_asset in referenced_assets:
        asset_file = out_dir / rel_asset
        assert asset_file.is_file(), f"Falta activo referenciado en HTML: {rel_asset}"
        assert asset_file.stat().st_size > 0

    embedded_catalog = _extract_embedded_catalog(html_content)
    disk_catalog = json.loads((out_dir / "talks.json").read_text(encoding="utf-8"))
    assert embedded_catalog == disk_catalog
    assert disk_catalog["total_talks"] == len(real_talks)

    for talk_item in embedded_catalog["talks"]:
        cover_url = talk_item["cover_url"]
        assert cover_url is not None
        cover_path = out_dir / cover_url
        assert cover_path.is_file(), f"Falta portada declarada en JSON: {cover_url}"
        assert cover_path.stat().st_size > 0
