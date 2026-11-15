"""
Archivo: shared/manifest.py
Fecha de modificación: 15/11/2026
Autor: Alex Prieto <alexprieto1997@gmail.com>

Descripción:
Descubre, carga y valida los manifiestos `talk.json` de cada charla bajo el
directorio `talks/`, aplicando el contrato JSON Schema y las reglas semánticas
de integridad definidas para el catálogo de `charlas`.

Acciones Principales:
    - Valida la estructura de `talk.json` mediante `jsonschema`.
    - Verifica reglas semánticas: fecha ISO estricta, coincidencia `slug == carpeta`,
      portada existente sin path traversal y bloque `build` en motor `custom`.
    - Descubre charlas publicables ordenadas por fecha descendente y slug ascendente.

Estructura Interna:
    - `ManifestValidationError`: Excepción de dominio para manifiestos inválidos.
    - `TalkManifest`: Dataclass inmutable que representa una charla validada.
    - `load_manifest`: Carga y valida el manifiesto de una carpeta de charla.
    - `discover_talks`: Escanea `talks_root`, filtra plantillas/borradores y ordena.

Entradas / Dependencias:
    - Archivos `talks/<slug>/talk.json` y librerías `jsonschema`, `dataclasses`, `pathlib`.

Salidas / Efectos:
    - Produce objetos `TalkManifest` y diccionarios serializables para el Hub y orquestador.

Ejemplo de Integración:
    from pathlib import Path
    from shared.manifest import discover_talks

    talks = discover_talks(Path("talks"))
"""

from dataclasses import dataclass, field
from datetime import date
import json
from pathlib import Path
import re
from typing import Any

import jsonschema

VALID_ENGINES: tuple[str, ...] = ("python-deck", "astro", "static", "custom")
MANIFEST_FILENAME: str = "talk.json"
DEFAULT_ENTRY: str = "index.html"
SLUG_REGEX: str = r"^[a-z0-9-]+$"
ISO_DATE_PATTERN: re.Pattern[str] = re.compile(r"^\d{4}-\d{2}-\d{2}$")

TALK_MANIFEST_SCHEMA: dict[str, Any] = {
    "type": "object",
    "required": ["slug", "title", "event", "date", "engine", "tags"],
    "additionalProperties": False,
    "properties": {
        "slug": {"type": "string", "pattern": SLUG_REGEX},
        "title": {"type": "string", "minLength": 3, "maxLength": 160},
        "subtitle": {"type": ["string", "null"]},
        "event": {"type": "string", "minLength": 1},
        "date": {"type": "string", "pattern": r"^\d{4}-\d{2}-\d{2}$"},
        "engine": {"type": "string", "enum": list(VALID_ENGINES)},
        "tags": {
            "type": "array",
            "minItems": 1,
            "items": {"type": "string", "minLength": 1},
        },
        "entry": {"type": "string", "minLength": 1},
        "cover": {"type": ["string", "null"], "minLength": 1},
        "slides_count": {"type": ["integer", "null"], "minimum": 1},
        "duration_min": {"type": ["integer", "null"], "minimum": 1},
        "draft": {"type": "boolean"},
        "build": {
            "type": ["object", "null"],
            "required": ["cmd", "out_dir"],
            "additionalProperties": False,
            "properties": {
                "cmd": {"type": "string", "minLength": 1},
                "out_dir": {"type": "string", "minLength": 1},
            },
        },
        "extras": {
            "type": "object",
            "additionalProperties": False,
            "properties": {
                "notebooks": {"type": ["string", "null"], "minLength": 1},
                "repo": {"type": ["string", "null"], "minLength": 1},
            },
        },
    },
}


class ManifestValidationError(ValueError):
    """
    Representa un error de validación estructural o semántica en un manifiesto `talk.json`.
    """


@dataclass(frozen=True)
class TalkManifest:
    """
    Representa un manifiesto de charla validado e inmutable.

    Attributes:
        slug (str): Identificador kebab-case único que coincide con la carpeta.
        title (str): Título principal de la ponencia.
        event (str): Evento o contexto de presentación.
        date (str): Fecha en formato ISO `YYYY-MM-DD`.
        engine (str): Motor de compilación (`python-deck`, `astro`, `static` o `custom`).
        tags (tuple[str, ...]): Etiquetas temáticas no vacías.
        subtitle (str | None): Subtítulo opcional de la charla.
        entry (str): Archivo HTML principal dentro del sitio compilado.
        cover (str | None): Ruta relativa de la imagen de portada dentro de la charla.
        slides_count (int | None): Cantidad estimada o real de diapositivas.
        duration_min (int | None): Duración estimada en minutos.
        draft (bool): Indica si la charla permanece como borrador privado.
        build (dict[str, str] | None): Configuración de compilación personalizada.
        extras (dict[str, str]): Enlaces complementarios como notebooks o repositorio.
        talk_dir (Path | None): Ruta resuelta al directorio fuente de la charla.
    """

    slug: str
    title: str
    event: str
    date: str
    engine: str
    tags: tuple[str, ...]
    subtitle: str | None = None
    entry: str = DEFAULT_ENTRY
    cover: str | None = None
    slides_count: int | None = None
    duration_min: int | None = None
    draft: bool = False
    build: dict[str, str] | None = None
    extras: dict[str, str] = field(default_factory=dict)
    talk_dir: Path | None = None

    def to_dict(self, base_path: str = "/") -> dict[str, Any]:
        """
        Convierte el manifiesto en un diccionario serializable a JSON para el catálogo.

        Args:
            base_path (str, opcional): Prefijo base de despliegue (ej. `/` o `/charlas`).

        Returns:
            dict[str, Any]: Diccionario con todos los campos públicos y la propiedad `url`.
        """
        normalized_base = base_path.rstrip("/")
        talk_url = f"{normalized_base}/{self.slug}/"

        return {
            "slug": self.slug,
            "title": self.title,
            "subtitle": self.subtitle,
            "event": self.event,
            "date": self.date,
            "engine": self.engine,
            "entry": self.entry,
            "cover": self.cover,
            "slides_count": self.slides_count,
            "duration_min": self.duration_min,
            "draft": self.draft,
            "tags": list(self.tags),
            "build": dict(self.build) if self.build is not None else None,
            "extras": dict(self.extras),
            "url": talk_url,
        }


def _read_manifest_json(manifest_path: Path) -> dict[str, Any]:
    """
    Lee y decodifica un archivo `talk.json` verificando que su raíz sea un objeto JSON.

    Args:
        manifest_path (Path): Ruta al archivo `talk.json`.

    Returns:
        dict[str, Any]: Contenido JSON decodificado.

    Raises:
        ManifestValidationError: Si el archivo no existe, contiene JSON inválido o no es objeto.
    """
    if not manifest_path.is_file():
        raise ManifestValidationError(
            f"No existe el archivo de manifiesto requerido: {manifest_path}"
        )

    try:
        raw_text = manifest_path.read_text(encoding="utf-8")
        payload = json.loads(raw_text)
    except (OSError, json.JSONDecodeError) as exc:
        raise ManifestValidationError(
            f"Error al leer JSON válido en {manifest_path}: {exc}"
        ) from exc

    if not isinstance(payload, dict):
        raise ManifestValidationError(
            f"El manifiesto {manifest_path} debe contener un objeto JSON en la raíz."
        )

    return payload


def _validate_json_schema(payload: dict[str, Any], manifest_path: Path) -> None:
    """
    Valida el diccionario del manifiesto contra el contrato JSON Schema oficial.

    Args:
        payload (dict[str, Any]): Datos decodificados de `talk.json`.
        manifest_path (Path): Ruta del archivo evaluado para mensajes de error claros.

    Raises:
        ManifestValidationError: Si algún campo incumple tipos, longitudes o valores permitidos.
    """
    try:
        jsonschema.validate(instance=payload, schema=TALK_MANIFEST_SCHEMA)
    except jsonschema.ValidationError as exc:
        raise ManifestValidationError(
            f"Esquema inválido en {manifest_path}: {exc.message}"
        ) from exc


def _validate_non_blank_fields(payload: dict[str, Any], manifest_path: Path) -> None:
    """
    Verifica que los textos obligatorios y etiquetas no contengan únicamente espacios en blanco.

    Args:
        payload (dict[str, Any]): Manifiesto validado por esquema.
        manifest_path (Path): Ruta del archivo evaluado.

    Raises:
        ManifestValidationError: Si algún campo textual contiene solo espacios.
    """
    if not payload["title"].strip():
        raise ManifestValidationError(f"'title' no puede estar vacío en {manifest_path}.")
    if not payload["event"].strip():
        raise ManifestValidationError(f"'event' no puede estar vacío en {manifest_path}.")

    for tag in payload["tags"]:
        if not tag.strip():
            raise ManifestValidationError(
                f"Las etiquetas en 'tags' no pueden estar vacías en {manifest_path}."
            )

    entry = payload.get("entry")
    if entry is not None and not entry.strip():
        raise ManifestValidationError(f"'entry' no puede estar vacío en {manifest_path}.")


def _validate_iso_date(raw_date: str, manifest_path: Path) -> None:
    """
    Valida que la fecha tenga formato estricto `YYYY-MM-DD` y exista en el calendario.

    Args:
        raw_date (str): Cadena de fecha declarada en el manifiesto.
        manifest_path (Path): Ruta del archivo evaluado.

    Raises:
        ManifestValidationError: Si la fecha no cumple formato ISO o es inexistente.
    """
    # Python 3.11 acepta formatos compactos sin guiones en fromisoformat; exige regex primero.
    if not ISO_DATE_PATTERN.match(raw_date):
        raise ManifestValidationError(
            f"Fecha inválida '{raw_date}' en {manifest_path}; usa formato YYYY-MM-DD."
        )

    try:
        date.fromisoformat(raw_date)
    except ValueError as exc:
        raise ManifestValidationError(
            f"Fecha de calendario inválida '{raw_date}' en {manifest_path}: {exc}"
        ) from exc


def _validate_cover_path(cover: str | None, talk_dir: Path, manifest_path: Path) -> None:
    """
    Verifica que la portada exista como archivo dentro de `talk_dir` sin path traversal.

    Args:
        cover (str | None): Ruta relativa declarada en `cover`.
        talk_dir (Path): Directorio raíz de la charla.
        manifest_path (Path): Ruta del archivo evaluado.

    Raises:
        ManifestValidationError: Si la ruta escapa de `talk_dir` o el archivo no existe.
    """
    if cover is None:
        return

    if not cover.strip() or Path(cover).is_absolute():
        raise ManifestValidationError(
            f"Ruta de portada inválida '{cover}' en {manifest_path}."
        )

    resolved_root = talk_dir.resolve()
    resolved_cover = (resolved_root / cover).resolve()

    if not resolved_cover.is_relative_to(resolved_root):
        raise ManifestValidationError(
            f"La portada '{cover}' intenta escapar fuera de {talk_dir}."
        )

    if not resolved_cover.is_file():
        raise ManifestValidationError(
            f"El archivo de portada '{cover}' no existe en {talk_dir}."
        )


def _validate_build_config(payload: dict[str, Any], manifest_path: Path) -> None:
    """
    Valida la obligatoriedad y consistencia de `build` cuando `engine == 'custom'`.

    Args:
        payload (dict[str, Any]): Manifiesto validado por esquema.
        manifest_path (Path): Ruta del archivo evaluado.

    Raises:
        ManifestValidationError: Si falta `build` en motor `custom` o contiene campos vacíos.
    """
    build_config = payload.get("build")

    if payload["engine"] == "custom" and build_config is None:
        raise ManifestValidationError(
            f"El motor 'custom' exige el bloque 'build' en {manifest_path}."
        )

    if build_config is not None:
        if not build_config["cmd"].strip() or not build_config["out_dir"].strip():
            raise ManifestValidationError(
                f"'build.cmd' y 'build.out_dir' no pueden estar vacíos en {manifest_path}."
            )


def load_manifest(talk_dir: Path) -> TalkManifest:
    """
    Carga y valida el manifiesto `talk.json` ubicado dentro de `talk_dir`.

    Args:
        talk_dir (Path): Ruta a la carpeta de una charla específica.

    Returns:
        TalkManifest: Instancia validada e inmutable del manifiesto.

    Raises:
        ManifestValidationError: Si el directorio o su `talk.json` incumplen el contrato.
    """
    if not talk_dir.is_dir():
        raise ManifestValidationError(
            f"La ruta de la charla no es un directorio válido: {talk_dir}"
        )

    manifest_path = talk_dir / MANIFEST_FILENAME
    payload = _read_manifest_json(manifest_path)
    _validate_json_schema(payload, manifest_path)
    _validate_non_blank_fields(payload, manifest_path)

    if payload["slug"] != talk_dir.name:
        raise ManifestValidationError(
            f"El slug '{payload['slug']}' debe coincidir con la carpeta '{talk_dir.name}'."
        )

    _validate_iso_date(payload["date"], manifest_path)
    _validate_cover_path(payload.get("cover"), talk_dir, manifest_path)
    _validate_build_config(payload, manifest_path)

    raw_extras = payload.get("extras") or {}
    clean_extras: dict[str, str] = {
        key: value for key, value in raw_extras.items() if value is not None
    }
    raw_build = payload.get("build")
    clean_build: dict[str, str] | None = dict(raw_build) if raw_build is not None else None

    return TalkManifest(
        slug=payload["slug"],
        title=payload["title"],
        event=payload["event"],
        date=payload["date"],
        engine=payload["engine"],
        tags=tuple(payload["tags"]),
        subtitle=payload.get("subtitle"),
        entry=payload.get("entry", DEFAULT_ENTRY),
        cover=payload.get("cover"),
        slides_count=payload.get("slides_count"),
        duration_min=payload.get("duration_min"),
        draft=payload.get("draft", False),
        build=clean_build,
        extras=clean_extras,
        talk_dir=talk_dir.resolve(),
    )


def discover_talks(
    talks_root: Path,
    include_drafts: bool = False,
) -> list[TalkManifest]:
    """
    Escanea `talks_root`, valida las charlas activas y las ordena por fecha descendente.

    Ignora subdirectorios cuyos nombres comienzan con `_` o `.`, excluye borradores
    salvo que `include_drafts` sea `True`, garantiza unicidad de `slug` y ordena por
    `date` descendente (desempate por `slug` ascendente).

    Args:
        talks_root (Path): Directorio raíz que agrupa las carpetas de charlas.
        include_drafts (bool, opcional): Incluye charlas con `draft=True` si es `True`.

    Returns:
        list[TalkManifest]: Lista ordenada de manifiestos validados.

    Raises:
        ManifestValidationError: Si `talks_root` no existe, falta algún `talk.json` o hay
            slugs duplicados.
    """
    if not talks_root.is_dir():
        raise ManifestValidationError(
            f"El directorio raíz de charlas no existe o no es carpeta: {talks_root}"
        )

    discovered: list[TalkManifest] = []
    seen_slugs: set[str] = set()

    candidate_dirs = sorted(
        (
            entry
            for entry in talks_root.iterdir()
            if entry.is_dir() and not entry.name.startswith(("_", "."))
        ),
        key=lambda entry: entry.name,
    )

    for talk_dir in candidate_dirs:
        manifest = load_manifest(talk_dir)
        if manifest.draft and not include_drafts:
            continue

        if manifest.slug in seen_slugs:
            raise ManifestValidationError(
                f"Slug duplicado detectado en el catálogo: '{manifest.slug}'."
            )

        seen_slugs.add(manifest.slug)
        discovered.append(manifest)

    discovered.sort(
        key=lambda item: (-date.fromisoformat(item.date).toordinal(), item.slug)
    )
    return discovered
