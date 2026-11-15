"""
Archivo: tests/unit/test_manifest.py
Fecha de modificación: 15/11/2026
Autor: Alex Prieto <alexprieto1997@gmail.com>

Descripción:
Valida el módulo `shared/manifest.py` mediante pruebas unitarias de contrato
(`talk.json`, validaciones semánticas, exclusión de plantillas y borradores) y
una prueba de simulación de usuario end-to-end sobre un directorio `talks` temporal.

Acciones Principales:
    - Verifica la carga válida completa y mínima de `TalkManifest`.
    - Comprueba el rechazo con `ManifestValidationError` ante datos inválidos.
    - Verifica el filtrado de `_template_*`, borradores y detección de slugs duplicados.
    - Simula un usuario creando charlas reales en `tmp_path` y serializando el catálogo.

Estructura Interna:
    - `_create_talk_dir`: Helper local que materializa una carpeta de charla y su `talk.json`.
    - `test_*`: Casos unitarios independientes de validación y descubrimiento.
    - `test_user_simulation_discover_and_serialize_catalog`: Simulación de usuario completa.

Entradas / Dependencias:
    - `shared.manifest` (`VALID_ENGINES`, `ManifestValidationError`, `TalkManifest`,
      `load_manifest`, `discover_talks`).

Salidas / Efectos:
    - Reporta aprobación o fallo de los criterios de aceptación de la Tarea T0.2.1.

Ejemplo de Integración:
    python -m pytest tests/unit/test_manifest.py -v
"""

import json
from pathlib import Path
from typing import Any

import pytest

from shared.manifest import (
    VALID_ENGINES,
    ManifestValidationError,
    TalkManifest,
    discover_talks,
    load_manifest,
)


def _create_talk_dir(
    root: Path,
    folder_name: str,
    payload: dict[str, Any],
    cover_relpath: str | None = None,
) -> Path:
    """
    Crea una carpeta de charla con su archivo `talk.json` y una portada opcional.

    Args:
        root (Path): Directorio padre donde reside la carpeta de la charla.
        folder_name (str): Nombre del subdirectorio de la charla.
        payload (dict[str, Any]): Contenido JSON para escribir en `talk.json`.
        cover_relpath (str | None, opcional): Ruta relativa de portada a crear en disco.

    Returns:
        Path: Ruta al directorio creado para la charla.
    """
    talk_dir = root / folder_name
    talk_dir.mkdir(parents=True, exist_ok=True)
    (talk_dir / "talk.json").write_text(
        json.dumps(payload, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    if cover_relpath is not None:
        cover_file = talk_dir / cover_relpath
        cover_file.parent.mkdir(parents=True, exist_ok=True)
        cover_file.write_bytes(b"PNG_FAKE_COVER")

    return talk_dir


def test_load_manifest_minimal_and_full_valid(tmp_path: Path) -> None:
    """
    Verifica la carga exitosa de un manifiesto mínimo y de uno con todos los campos opcionales.
    """
    minimal_payload = {
        "slug": "2026-minima",
        "title": "Charla Mínima",
        "event": "PyCon",
        "date": "2026-05-10",
        "engine": "static",
        "tags": ["python"],
    }
    minimal_dir = _create_talk_dir(tmp_path, "2026-minima", minimal_payload)
    minimal = load_manifest(minimal_dir)

    assert isinstance(minimal, TalkManifest)
    assert minimal.slug == "2026-minima"
    assert minimal.entry == "index.html"
    assert minimal.draft is False
    assert minimal.cover is None
    assert minimal.extras == {}
    assert minimal.tags == ("python",)

    full_payload = {
        "slug": "2026-completa",
        "title": "Forecasting con Modelos Fundacionales",
        "subtitle": "Comparativa de Chronos y TimesFM en series reales",
        "event": "Data Day Lima",
        "date": "2026-10-05",
        "engine": "custom",
        "tags": ["forecasting", "ia"],
        "entry": "deck.html",
        "cover": "assets/cover.png",
        "slides_count": 30,
        "duration_min": 45,
        "draft": False,
        "build": {"cmd": "python build.py", "out_dir": "dist"},
        "extras": {
            "notebooks": "notebooks/demo.ipynb",
            "repo": "https://github.com/AlexPrietoRomani/charlas",
        },
    }
    full_dir = _create_talk_dir(
        tmp_path,
        "2026-completa",
        full_payload,
        cover_relpath="assets/cover.png",
    )
    full = load_manifest(full_dir)

    assert full.subtitle == "Comparativa de Chronos y TimesFM en series reales"
    assert full.entry == "deck.html"
    assert full.cover == "assets/cover.png"
    assert full.slides_count == 30
    assert full.duration_min == 45
    assert full.build == {"cmd": "python build.py", "out_dir": "dist"}
    assert full.extras["repo"] == "https://github.com/AlexPrietoRomani/charlas"
    assert VALID_ENGINES == ("python-deck", "astro", "static", "custom")


@pytest.mark.parametrize(
    ("folder_name", "slug_value"),
    [
        ("2026-Invalid_Slug", "2026-Invalid_Slug"),
        ("2026-carpeta-real", "2026-otro-slug"),
    ],
)
def test_load_manifest_rejects_invalid_or_mismatched_slug(
    tmp_path: Path,
    folder_name: str,
    slug_value: str,
) -> None:
    """
    Comprueba que `load_manifest` rechaza slugs con caracteres inválidos o distintos a la carpeta.
    """
    payload = {
        "slug": slug_value,
        "title": "Charla con slug inválido",
        "event": "Meetup",
        "date": "2026-08-01",
        "engine": "static",
        "tags": ["datos"],
    }
    talk_dir = _create_talk_dir(tmp_path, folder_name, payload)

    with pytest.raises(ManifestValidationError):
        load_manifest(talk_dir)


@pytest.mark.parametrize("bad_date", ["2026-99-99", "20260510", "10-05-2026", "2026-02-30"])
def test_load_manifest_rejects_invalid_date(tmp_path: Path, bad_date: str) -> None:
    """
    Verifica el rechazo ante fechas fuera de calendario o sin formato estricto `YYYY-MM-DD`.
    """
    payload = {
        "slug": "2026-fecha-mala",
        "title": "Charla con fecha inválida",
        "event": "Meetup",
        "date": bad_date,
        "engine": "astro",
        "tags": ["astro"],
    }
    talk_dir = _create_talk_dir(tmp_path, "2026-fecha-mala", payload)

    with pytest.raises(ManifestValidationError):
        load_manifest(talk_dir)


def test_load_manifest_rejects_unknown_engine(tmp_path: Path) -> None:
    """
    Verifica el rechazo cuando `engine` no pertenece a los motores soportados.
    """
    payload = {
        "slug": "2026-motor-desconocido",
        "title": "Charla con motor no soportado",
        "event": "Conf",
        "date": "2026-06-15",
        "engine": "revealjs",
        "tags": ["web"],
    }
    talk_dir = _create_talk_dir(tmp_path, "2026-motor-desconocido", payload)

    with pytest.raises(ManifestValidationError):
        load_manifest(talk_dir)


def test_load_manifest_rejects_missing_or_traversal_cover(tmp_path: Path) -> None:
    """
    Verifica el rechazo ante portadas inexistentes o rutas con path traversal.
    """
    secret_file = tmp_path / "secret.png"
    secret_file.write_bytes(b"SECRET")

    missing_cover_payload = {
        "slug": "2026-portada-faltante",
        "title": "Portada Faltante",
        "event": "Meetup",
        "date": "2026-04-01",
        "engine": "static",
        "tags": ["slides"],
        "cover": "cover.png",
    }
    missing_dir = _create_talk_dir(tmp_path, "2026-portada-faltante", missing_cover_payload)

    with pytest.raises(ManifestValidationError):
        load_manifest(missing_dir)

    traversal_payload = {
        "slug": "2026-portada-escape",
        "title": "Portada Path Traversal",
        "event": "Meetup",
        "date": "2026-04-01",
        "engine": "static",
        "tags": ["slides"],
        "cover": "../secret.png",
    }
    traversal_dir = _create_talk_dir(tmp_path, "2026-portada-escape", traversal_payload)

    with pytest.raises(ManifestValidationError):
        load_manifest(traversal_dir)


def test_load_manifest_rejects_custom_engine_without_build_cmd(tmp_path: Path) -> None:
    """
    Verifica que `engine == 'custom'` falle si falta `build` o `build.cmd`.
    """
    no_build_payload = {
        "slug": "2026-custom-sin-build",
        "title": "Custom sin bloque build",
        "event": "Conf",
        "date": "2026-03-15",
        "engine": "custom",
        "tags": ["quarto"],
    }
    no_build_dir = _create_talk_dir(tmp_path, "2026-custom-sin-build", no_build_payload)

    with pytest.raises(ManifestValidationError):
        load_manifest(no_build_dir)

    missing_cmd_payload = {
        "slug": "2026-custom-sin-cmd",
        "title": "Custom sin build.cmd",
        "event": "Conf",
        "date": "2026-03-15",
        "engine": "custom",
        "tags": ["quarto"],
        "build": {"out_dir": "dist"},
    }
    missing_cmd_dir = _create_talk_dir(tmp_path, "2026-custom-sin-cmd", missing_cmd_payload)

    with pytest.raises(ManifestValidationError):
        load_manifest(missing_cmd_dir)


def test_discover_talks_excludes_templates_drafts_and_rejects_duplicate_slugs(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """
    Verifica la exclusión de `_template_*` y `draft: true`, y el error por `slug` duplicado.
    """
    _create_talk_dir(
        tmp_path,
        "_template_static",
        {
            "slug": "template-static",
            "title": "Plantilla",
            "event": "Template",
            "date": "2026-01-01",
            "engine": "static",
            "tags": ["template"],
        },
    )
    _create_talk_dir(
        tmp_path,
        "2026-borrador",
        {
            "slug": "2026-borrador",
            "title": "Borrador Privado",
            "event": "Interno",
            "date": "2026-02-01",
            "engine": "static",
            "tags": ["draft"],
            "draft": True,
        },
    )
    _create_talk_dir(
        tmp_path,
        "2026-publicada",
        {
            "slug": "2026-publicada",
            "title": "Charla Publicada",
            "event": "PyData",
            "date": "2026-07-01",
            "engine": "python-deck",
            "tags": ["pydata"],
        },
    )

    public_talks = discover_talks(tmp_path)
    assert [item.slug for item in public_talks] == ["2026-publicada"]

    all_talks = discover_talks(tmp_path, include_drafts=True)
    assert [item.slug for item in all_talks] == ["2026-publicada", "2026-borrador"]

    # Simula dos carpetas distintas devolviendo el mismo slug para validar la guarda.
    duplicate_manifest = TalkManifest(
        slug="slug-duplicado",
        title="Charla Duplicada",
        event="Conf",
        date="2026-09-01",
        engine="static",
        tags=("dup",),
    )
    (tmp_path / "2026-dup-uno").mkdir()
    (tmp_path / "2026-dup-dos").mkdir()
    monkeypatch.setattr(
        "shared.manifest.load_manifest",
        lambda _talk_dir: duplicate_manifest,
    )

    with pytest.raises(ManifestValidationError, match="duplicado"):
        discover_talks(tmp_path)


def test_user_simulation_discover_and_serialize_catalog(tmp_path: Path) -> None:
    """
    Simula un usuario creando charlas (`2026-a`, `2026-b`), plantilla y borrador en `tmp_path`.
    """
    _create_talk_dir(
        tmp_path,
        "2026-a",
        {
            "slug": "2026-a",
            "title": "Primera Charla Cronológica",
            "event": "Meetup Abril",
            "date": "2026-04-12",
            "engine": "astro",
            "tags": ["astro", "visualizacion"],
            "cover": "cover.png",
        },
        cover_relpath="cover.png",
    )
    _create_talk_dir(
        tmp_path,
        "2026-b",
        {
            "slug": "2026-b",
            "title": "Segunda Charla Más Reciente",
            "event": "Conferencia Octubre",
            "date": "2026-10-05",
            "engine": "python-deck",
            "tags": ["forecasting", "ia"],
            "slides_count": 30,
        },
    )
    _create_talk_dir(
        tmp_path,
        "_template_foo",
        {
            "slug": "template-foo",
            "title": "Plantilla Ignorada",
            "event": "N/A",
            "date": "2026-01-01",
            "engine": "static",
            "tags": ["template"],
        },
    )
    _create_talk_dir(
        tmp_path,
        "2026-draft-oculto",
        {
            "slug": "2026-draft-oculto",
            "title": "Borrador En Progreso",
            "event": "WIP",
            "date": "2026-12-01",
            "engine": "static",
            "tags": ["wip"],
            "draft": True,
        },
    )
    # Verifica que carpetas ocultas iniciadas con punto también se ignoren.
    (tmp_path / ".cache").mkdir()

    catalog = discover_talks(tmp_path)
    assert [talk.slug for talk in catalog] == ["2026-b", "2026-a"]

    root_serialized = [talk.to_dict(base_path="/") for talk in catalog]
    subpath_serialized = [talk.to_dict(base_path="/charlas") for talk in catalog]

    assert root_serialized[0]["url"] == "/2026-b/"
    assert root_serialized[1]["url"] == "/2026-a/"
    assert subpath_serialized[0]["url"] == "/charlas/2026-b/"
    assert subpath_serialized[1]["url"] == "/charlas/2026-a/"
    assert root_serialized[1]["cover"] == "cover.png"

    # Confirma serialización JSON completa sin tipos no serializables.
    serialized_json = json.dumps(subpath_serialized, ensure_ascii=False)
    decoded = json.loads(serialized_json)
    assert len(decoded) == 2
    assert decoded[0]["slug"] == "2026-b"
    assert decoded[1]["tags"] == ["astro", "visualizacion"]


def test_discover_talks_tiebreaks_by_slug_and_requires_manifest(tmp_path: Path) -> None:
    """
    Verifica el desempate por `slug` ascendente y el error si falta `talk.json`.
    """
    _create_talk_dir(
        tmp_path,
        "2026-zeta",
        {
            "slug": "2026-zeta",
            "title": "Charla Zeta",
            "event": "Conf",
            "date": "2026-08-15",
            "engine": "static",
            "tags": ["a"],
        },
    )
    _create_talk_dir(
        tmp_path,
        "2026-alfa",
        {
            "slug": "2026-alfa",
            "title": "Charla Alfa",
            "event": "Conf",
            "date": "2026-08-15",
            "engine": "static",
            "tags": ["b"],
        },
    )

    ordered = discover_talks(tmp_path)
    assert [item.slug for item in ordered] == ["2026-alfa", "2026-zeta"]

    (tmp_path / "2026-sin-manifiesto").mkdir()
    with pytest.raises(ManifestValidationError, match="talk.json"):
        discover_talks(tmp_path)

