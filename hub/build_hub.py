"""
Archivo: hub/build_hub.py
Fecha de modificación: 15/11/2026
Autor: Alex Prieto <alexprieto1997@gmail.com>

Descripción:
Genera el portal selector principal del repositorio `charlas` (`index.html`), el
catálogo JSON consolidado (`talks.json`) y copia los activos visuales necesarios
hacia `<out_dir>/hub_assets/` conservando únicamente la marca personal del autor.

Acciones Principales:
    - Crea `<out_dir>` y `<out_dir>/hub_assets/`.
    - Copia la foto de perfil `hub/assets/profile_alex.jpg` al directorio destino.
    - Copia la portada existente de cada charla hacia `hub_assets/<slug>_cover.<ext>`.
    - Serializa `talks.json` e inyecta el catálogo saneado dentro de `hub/template.html`.

Estructura Interna:
    - `_normalize_base_path`: Normaliza el prefijo base de URL (`/` o `/charlas`).
    - `_build_clean_manifest`: Construye una vista limpia de `talk.json` para el modal.
    - `_copy_hub_profile_asset`: Copia la imagen de perfil hacia `hub_assets/`.
    - `_copy_talk_cover`: Copia la portada de una charla si existe en disco.
    - `_serialize_talk_entry`: Combina `to_dict`, `cover_url` y `manifest`.
    - `_render_hub_html`: Inyecta el JSON escapado en la plantilla HTML.
    - `build_hub`: Orquesta la compilación completa del Hub selector.

Entradas / Dependencias:
    - `hub/template.html`, `hub/assets/profile_alex.jpg` y `shared.manifest.TalkManifest`.

Salidas / Efectos:
    - Escribe `<out_dir>/index.html`, `<out_dir>/talks.json` y archivos en `<out_dir>/hub_assets/`.

Ejemplo de Integración:
    from pathlib import Path
    from shared.manifest import discover_talks
    from hub.build_hub import build_hub

    talks = discover_talks(Path("talks"))
    build_hub(talks=talks, out_dir=Path("_site"), base_path="/charlas")
"""

from datetime import datetime, timezone
import json
from pathlib import Path
import shutil
from typing import Any

from shared.manifest import TalkManifest

HUB_DIR: Path = Path(__file__).resolve().parent
DEFAULT_TEMPLATE_PATH: Path = HUB_DIR / "template.html"
DEFAULT_ASSETS_DIR: Path = HUB_DIR / "assets"
PROFILE_FILENAME: str = "profile_alex.jpg"
HUB_ASSETS_DIRNAME: str = "hub_assets"
CATALOG_FILENAME: str = "talks.json"
INDEX_FILENAME: str = "index.html"
CATALOG_PLACEHOLDER: str = "__CATALOG_JSON__"


def _normalize_base_path(base_path: str) -> str:
    """
    Normaliza el prefijo base de despliegue para evitar barras redundantes.

    Args:
        base_path (str): Prefijo base recibido (ej. `/`, `/charlas` o `charlas/`).

    Returns:
        str: Prefijo normalizado con barra inicial y sin barra final (excepto `/`).
    """
    stripped = base_path.strip("/")
    if not stripped:
        return "/"
    return f"/{stripped}"


def _build_clean_manifest(talk: TalkManifest) -> dict[str, Any]:
    """
    Construye un diccionario limpio equivalente a `talk.json` para inspección en UI.

    Args:
        talk (TalkManifest): Manifiesto validado de la charla.

    Returns:
        dict[str, Any]: Representación JSON limpia sin propiedades derivadas en tiempo de build.
    """
    clean_manifest: dict[str, Any] = {
        "slug": talk.slug,
        "title": talk.title,
    }
    if talk.subtitle is not None:
        clean_manifest["subtitle"] = talk.subtitle

    clean_manifest["event"] = talk.event
    clean_manifest["date"] = talk.date
    clean_manifest["engine"] = talk.engine
    clean_manifest["entry"] = talk.entry

    if talk.cover is not None:
        clean_manifest["cover"] = talk.cover
    if talk.slides_count is not None:
        clean_manifest["slides_count"] = talk.slides_count
    if talk.duration_min is not None:
        clean_manifest["duration_min"] = talk.duration_min
    if talk.draft:
        clean_manifest["draft"] = talk.draft

    clean_manifest["tags"] = list(talk.tags)

    if talk.build is not None:
        clean_manifest["build"] = dict(talk.build)
    if talk.extras:
        clean_manifest["extras"] = dict(talk.extras)

    return clean_manifest


def _copy_hub_profile_asset(hub_assets_dir: Path) -> Path:
    """
    Copia la fotografía de perfil personal del Hub hacia `hub_assets/`.

    Args:
        hub_assets_dir (Path): Carpeta destino `<out_dir>/hub_assets`.

    Returns:
        Path: Ruta al archivo copiado dentro de `hub_assets/`.

    Raises:
        FileNotFoundError: Si no existe `hub/assets/profile_alex.jpg`.
    """
    profile_source = DEFAULT_ASSETS_DIR / PROFILE_FILENAME
    if not profile_source.is_file():
        raise FileNotFoundError(
            f"No existe la imagen de perfil requerida del Hub: {profile_source}"
        )

    profile_target = hub_assets_dir / PROFILE_FILENAME
    shutil.copy2(profile_source, profile_target)
    return profile_target


def _copy_talk_cover(talk: TalkManifest, hub_assets_dir: Path) -> str | None:
    """
    Copia la portada de una charla hacia `hub_assets/` y retorna su ruta relativa.

    Args:
        talk (TalkManifest): Manifiesto de la charla evaluada.
        hub_assets_dir (Path): Carpeta destino `<out_dir>/hub_assets`.

    Returns:
        str | None: Ruta relativa `hub_assets/<slug>_cover<ext>` o `None` si no hay archivo.
    """
    if not talk.cover or talk.talk_dir is None:
        return None

    cover_source = talk.talk_dir / talk.cover
    if not cover_source.is_file():
        return None

    cover_filename = f"{talk.slug}_cover{cover_source.suffix}"
    cover_target = hub_assets_dir / cover_filename
    shutil.copy2(cover_source, cover_target)
    return f"{HUB_ASSETS_DIRNAME}/{cover_filename}"


def _serialize_talk_entry(
    talk: TalkManifest,
    hub_assets_dir: Path,
    base_path: str,
) -> dict[str, Any]:
    """
    Serializa una charla con su URL pública, portada copiada y manifiesto limpio.

    Args:
        talk (TalkManifest): Manifiesto validado de la charla.
        hub_assets_dir (Path): Carpeta destino donde se almacenan las portadas.
        base_path (str): Prefijo base normalizado para construir `url`.

    Returns:
        dict[str, Any]: Entrada lista para integrarse en `talks.json`.
    """
    entry = talk.to_dict(base_path=base_path)
    entry["cover_url"] = _copy_talk_cover(talk=talk, hub_assets_dir=hub_assets_dir)
    entry["manifest"] = _build_clean_manifest(talk)
    return entry


def _render_hub_html(catalog_payload: dict[str, Any], template_path: Path) -> str:
    """
    Inyecta el catálogo JSON dentro de la plantilla HTML escapando cierres de script.

    Args:
        catalog_payload (dict[str, Any]): Diccionario completo del catálogo de charlas.
        template_path (Path): Ruta a la plantilla base `hub/template.html`.

    Returns:
        str: Documento HTML final listo para escribirse como `index.html`.

    Raises:
        FileNotFoundError: Si la plantilla HTML no existe.
        ValueError: Si la plantilla no contiene el marcador `__CATALOG_JSON__`.
    """
    if not template_path.is_file():
        raise FileNotFoundError(f"No existe la plantilla del Hub: {template_path}")

    template_html = template_path.read_text(encoding="utf-8")
    if CATALOG_PLACEHOLDER not in template_html:
        raise ValueError(
            f"La plantilla {template_path} no contiene el marcador {CATALOG_PLACEHOLDER}."
        )

    raw_json = json.dumps(catalog_payload, ensure_ascii=False, indent=2)
    # Escapa `</` para impedir cierre prematuro de `<script>` ante contenido arbitrario.
    safe_json = raw_json.replace("</", "<\\/")
    return template_html.replace(CATALOG_PLACEHOLDER, safe_json, 1)


def build_hub(
    talks: list[TalkManifest],
    out_dir: Path,
    base_path: str = "/",
) -> Path:
    """
    Compila el Hub selector estático (`index.html`), `talks.json` y sus activos en `out_dir`.

    Args:
        talks (list[TalkManifest]): Lista de manifiestos validados que integran el catálogo.
        out_dir (Path): Directorio raíz de salida estática (ej. `_site`).
        base_path (str, opcional): Subpath de despliegue (ej. `/` o `/charlas`).

    Returns:
        Path: Ruta al archivo `index.html` generado dentro de `out_dir`.
    """
    normalized_base = _normalize_base_path(base_path)
    out_dir.mkdir(parents=True, exist_ok=True)
    hub_assets_dir = out_dir / HUB_ASSETS_DIRNAME
    hub_assets_dir.mkdir(parents=True, exist_ok=True)

    _copy_hub_profile_asset(hub_assets_dir)

    serialized_talks = [
        _serialize_talk_entry(
            talk=talk,
            hub_assets_dir=hub_assets_dir,
            base_path=normalized_base,
        )
        for talk in talks
    ]

    generated_at = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
    catalog_payload: dict[str, Any] = {
        "generated_at": generated_at,
        "base_path": normalized_base,
        "total_talks": len(serialized_talks),
        "talks": serialized_talks,
    }

    catalog_path = out_dir / CATALOG_FILENAME
    catalog_path.write_text(
        json.dumps(catalog_payload, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    rendered_html = _render_hub_html(
        catalog_payload=catalog_payload,
        template_path=DEFAULT_TEMPLATE_PATH,
    )
    index_path = out_dir / INDEX_FILENAME
    index_path.write_text(rendered_html, encoding="utf-8")
    return index_path
