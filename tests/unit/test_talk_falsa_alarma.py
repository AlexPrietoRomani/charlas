"""
Archivo: tests/unit/test_talk_falsa_alarma.py
Fecha de modificación: 15/11/2026
Autor: Alex Prieto <alexprieto1997@gmail.com>

Descripción:
Valida la integración limpia de la charla `talks/2026-falsa-alarma/` basada en Astro,
verificando su manifiesto `talk.json`, la ausencia de binarios prohibidos o archivos
pesados, la parametrización de `astro.config.mjs` y el flujo real de compilación
mediante `pnpm`.

Acciones Principales:
    - Valida `talks/2026-falsa-alarma/talk.json` con `load_manifest()` y el conteo real de slides.
    - Audita que no existan archivos `.exe`, `.pdf`, artefactos excluidos ni archivos > 5 MB.
    - Verifica la configuración de `ASTRO_BASE`, `output: 'static'` e `inlineStylesheets: 'always'`.
    - Simula al usuario ejecutando `pnpm --dir talks/2026-falsa-alarma build -- --base /2026-falsa-alarma`
      y comprueba que la salida en `dist/` contiene HTML, CSV y todas las imágenes referenciadas.

Estructura Interna:
    - `_iter_clean_source_files`: Recorre los archivos versionables ignorando cachés de Node/Astro.
    - `test_falsa_alarma_manifest_is_valid`: Prueba unitaria del contrato `talk.json`.
    - `test_falsa_alarma_has_no_prohibited_or_oversized_files`: Auditoría unitaria de higiene y peso.
    - `test_astro_config_supports_env_base`: Verificación unitaria de `astro.config.mjs`.
    - `test_user_simulation_astro_build_and_assets`: Simulación E2E de compilación Astro.

Entradas / Dependencias:
    - `shared.manifest.load_manifest`, carpeta `talks/2026-falsa-alarma/` y ejecutable `pnpm`.

Salidas / Efectos:
    - Reporta el cumplimiento de los Criterios de Aceptación de la Tarea T1.2.1.

Ejemplo de Integración:
    python -m pytest tests/unit/test_talk_falsa_alarma.py -v
"""

from html.parser import HTMLParser
import os
from pathlib import Path
import re
import shutil
import subprocess
from typing import Iterator

from shared.manifest import TalkManifest, load_manifest

REPO_ROOT: Path = Path(__file__).resolve().parents[2]
TALK_DIR: Path = REPO_ROOT / "talks" / "2026-falsa-alarma"
MAX_ALLOWED_FILE_BYTES: int = 5 * 1024 * 1024
IGNORED_BUILD_DIRS: frozenset[str] = frozenset({"node_modules", "dist", ".astro"})
PROHIBITED_EXTENSIONS: frozenset[str] = frozenset({".exe", ".pdf"})
PROHIBITED_ROOT_ENTRIES: tuple[str, ...] = (
    "assets",
    "articles",
    ".git",
    ".github",
    ".playwright-mcp",
    ".project-suite",
    "presentacion.html",
)


class _AssetReferenceParser(HTMLParser):
    """
    Extrae referencias locales de imágenes, íconos y scripts desde HTML compilado.
    """

    def __init__(self) -> None:
        """
        Inicializa las colecciones de rutas detectadas en el documento HTML.
        """
        super().__init__()
        self.image_sources: list[str] = []
        self.icon_hrefs: list[str] = []
        self.script_sources: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        """
        Registra los atributos `src` y `href` relevantes por etiqueta HTML.

        Args:
            tag (str): Nombre de la etiqueta HTML encontrada.
            attrs (list[tuple[str, str | None]]): Pares atributo-valor de la etiqueta.
        """
        attr_map = dict(attrs)
        if tag == "img" and attr_map.get("src"):
            self.image_sources.append(attr_map["src"] or "")
        elif tag == "link" and attr_map.get("rel") == "icon" and attr_map.get("href"):
            self.icon_hrefs.append(attr_map["href"] or "")
        elif tag == "script" and attr_map.get("src"):
            self.script_sources.append(attr_map["src"] or "")


def _iter_clean_source_files(root_dir: Path) -> Iterator[Path]:
    """
    Itera sobre los archivos fuente de la charla omitiendo carpetas generadas o dependencias.

    Args:
        root_dir (Path): Directorio raíz de la charla Astro.

    Yields:
        Iterator[Path]: Rutas de archivos regulares fuera de `node_modules`, `dist` y `.astro`.
    """
    for current_root, dir_names, file_names in os.walk(root_dir):
        dir_names[:] = [name for name in dir_names if name not in IGNORED_BUILD_DIRS]
        base_path = Path(current_root)
        for file_name in file_names:
            yield base_path / file_name


def test_falsa_alarma_manifest_is_valid() -> None:
    """
    Verifica que `talks/2026-falsa-alarma/talk.json` cumple el contrato y el conteo de slides.
    """
    manifest = load_manifest(TALK_DIR)

    assert isinstance(manifest, TalkManifest)
    assert manifest.slug == "2026-falsa-alarma"
    assert manifest.engine == "astro"
    assert manifest.entry == "index.html"
    assert manifest.cover == "public/assets/strawberry_field_sprinklers_night.png"
    assert manifest.duration_min == 25
    assert manifest.draft is False
    assert "Astro" in manifest.tags

    index_astro = (TALK_DIR / "src" / "pages" / "index.astro").read_text(encoding="utf-8")
    actual_slides_count = len(re.findall(r'<section\s+class="slide', index_astro))
    assert actual_slides_count == 21
    assert manifest.slides_count == actual_slides_count


def test_falsa_alarma_has_no_prohibited_or_oversized_files() -> None:
    """
    Comprueba la ausencia de ejecutables, PDFs, carpetas prohibidas y archivos mayores a 5 MB.
    """
    for entry_name in PROHIBITED_ROOT_ENTRIES:
        forbidden_path = TALK_DIR / entry_name
        assert not forbidden_path.exists(), f"Entrada prohibida presente: {forbidden_path}"

    source_files = list(_iter_clean_source_files(TALK_DIR))
    assert source_files, "El directorio de la charla no contiene archivos fuente."

    for file_path in source_files:
        suffix = file_path.suffix.lower()
        assert suffix not in PROHIBITED_EXTENSIONS, f"Extensión prohibida en {file_path}"
        file_size = file_path.stat().st_size
        assert file_size <= MAX_ALLOWED_FILE_BYTES, (
            f"El archivo {file_path} pesa {file_size} bytes y supera el límite de 5 MB."
        )


def test_astro_config_supports_env_base() -> None:
    """
    Verifica que `astro.config.mjs` parametriza `base` con `ASTRO_BASE` y mantiene build estático.
    """
    config_text = (TALK_DIR / "astro.config.mjs").read_text(encoding="utf-8")

    assert "process.env.ASTRO_BASE" in config_text
    assert "'/charlas/2026-falsa-alarma'" in config_text
    assert "site: 'https://alexprietoromani.github.io'" in config_text
    assert "output: 'static'" in config_text
    assert "inlineStylesheets: 'always'" in config_text


def test_user_simulation_astro_build_and_assets() -> None:
    """
    Simula al usuario compilando la charla Astro con `--base /2026-falsa-alarma` y verifica `dist/`.
    """
    pnpm_executable = shutil.which("pnpm")
    assert pnpm_executable is not None, "El ejecutable 'pnpm' debe estar disponible en PATH."

    # En pnpm v7+, pasar '--' literal lo reenvía a Astro y bloquea las flags posteriores.
    build_result = subprocess.run(
        [
            pnpm_executable,
            "--dir",
            str(TALK_DIR),
            "build",
            "--base",
            "/2026-falsa-alarma",
        ],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    assert build_result.returncode == 0, (
        f"Falló la compilación Astro:\n{build_result.stdout}\n{build_result.stderr}"
    )

    dist_dir = TALK_DIR / "dist"
    index_html_path = dist_dir / "index.html"
    clima_csv_path = dist_dir / "data" / "clima_valle_elqui.csv"
    rendimiento_csv_path = dist_dir / "data" / "rendimiento_fresa.csv"
    cover_dist_path = dist_dir / "assets" / "strawberry_field_sprinklers_night.png"

    assert index_html_path.is_file(), "Falta dist/index.html tras compilar Astro."
    assert clima_csv_path.is_file(), "Falta dist/data/clima_valle_elqui.csv tras compilar."
    assert rendimiento_csv_path.is_file(), "Falta dist/data/rendimiento_fresa.csv tras compilar."
    assert cover_dist_path.is_file(), "Falta la portada en dist/assets/."

    html_content = index_html_path.read_text(encoding="utf-8")
    parser = _AssetReferenceParser()
    parser.feed(html_content)

    assert parser.image_sources, "No se encontraron etiquetas <img> en dist/index.html."
    for img_src in parser.image_sources:
        if img_src.startswith(("http://", "https://", "data:")):
            continue
        clean_rel_path = img_src.removeprefix("./").lstrip("/")
        assert (dist_dir / clean_rel_path).is_file(), (
            f"La imagen referenciada '{img_src}' no existe dentro de dist/."
        )

    for icon_href in parser.icon_hrefs:
        clean_icon_path = icon_href.removeprefix("./").lstrip("/")
        assert (dist_dir / clean_icon_path).is_file(), (
            f"El ícono referenciado '{icon_href}' no existe dentro de dist/."
        )

    local_astro_scripts = [
        src for src in parser.script_sources if src.startswith("/2026-falsa-alarma/_astro/")
    ]
    assert local_astro_scripts, (
        "Se esperaba al menos un bundle JS prefijado con '/2026-falsa-alarma/_astro/'."
    )
    for script_src in local_astro_scripts:
        rel_script_path = script_src.removeprefix("/2026-falsa-alarma/")
        assert (dist_dir / rel_script_path).is_file(), (
            f"El script compilado '{script_src}' no existe en dist/."
        )
