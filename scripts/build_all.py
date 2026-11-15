"""
Archivo: scripts/build_all.py
Fecha de modificación: 15/11/2026
Autor: Alex Prieto <alexprieto1997@gmail.com>

Descripción:
Orquestador maestro multi-motor del repositorio `charlas`. Descubre y valida
los manifiestos de `talks/`, compila cada charla según su motor (`python-deck`,
`astro`, `static` o `custom`) hacia `<out_dir>/<slug>/`, verifica la existencia
del archivo `entry` declarado y genera finalmente el Hub selector estático.

Acciones Principales:
    - Limpia y recrea el directorio de salida (`_site` por defecto).
    - Descubre charlas publicables mediante `shared.manifest.discover_talks`.
    - Despacha la compilación uniforme mediante `ENGINE_BUILDERS`.
    - Verifica la existencia de `<out_dir>/<slug>/<entry>` tras cada build.
    - Compila el portal principal invocando `hub.build_hub.build_hub`.

Estructura Interna:
    - `BuildError`: Excepción de dominio para fallos de compilación o entrada faltante.
    - `compute_talk_base`: Calcula la ruta base pública de cada charla.
    - `_run_subprocess`: Ejecuta subprocesos controlados lanzando `BuildError` ante fallos.
    - `build_python_deck_talk`: Compila charlas `python-deck` vía `back/build_deck.py`.
    - `build_astro_talk`: Instala dependencias si faltan y compila charlas `astro` con `pnpm`.
    - `build_static_talk`: Copia charlas estáticas excluyendo metadatos y cachés.
    - `build_custom_talk`: Ejecuta comandos `build.cmd` y copia `build.out_dir`.
    - `ENGINE_BUILDERS`: Mapa uniforme de motores hacia sus funciones constructoras.
    - `build_all`: Orquesta la compilación completa del sitio.
    - `main`: Punto de entrada CLI con `argparse`.

Entradas / Dependencias:
    - `shared.manifest` (`ManifestValidationError`, `TalkManifest`, `discover_talks`).
    - `hub.build_hub.build_hub`, ejecutable Python activo y `pnpm` para charlas Astro.

Salidas / Efectos:
    - Genera `<out_dir>/index.html`, `<out_dir>/talks.json`, `<out_dir>/hub_assets/` y
      un subdirectorio compilado `<out_dir>/<slug>/` por cada charla activa.

Ejecución:
    python scripts/build_all.py [--talks-dir TALKS_DIR] [--out-dir OUT_DIR] [--base-path BASE_PATH] [--include-drafts]

Ejemplo de Uso:
    python scripts/build_all.py --out-dir _site --base-path /charlas

Argumentos:
    - --talks-dir: str - Directorio raíz con carpetas de charlas (por defecto `talks`).
    - --out-dir: str - Directorio destino del sitio compilado (por defecto `_site`).
    - --base-path: str - Prefijo URL de despliegue (por defecto `/`).
    - --include-drafts: bool - Incluye charlas marcadas con `draft: true` si se especifica.
"""

import argparse
from collections.abc import Callable
import os
from pathlib import Path
import shutil
import subprocess
import sys

REPO_ROOT: Path = Path(__file__).resolve().parent.parent
# Garantiza la resolución de `shared` y `hub` al invocar `python scripts/build_all.py`.
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from hub.build_hub import build_hub  # noqa: E402
from shared.manifest import (  # noqa: E402
    ManifestValidationError,
    TalkManifest,
    discover_talks,
)

DEFAULT_TALKS_DIR: str = "talks"
DEFAULT_OUT_DIR: str = "_site"
DEFAULT_BASE_PATH: str = "/"
STATIC_IGNORE_PATTERNS: tuple[str, ...] = (
    "talk.json",
    "README.md",
    "__pycache__",
    "node_modules",
    ".git",
    ".astro",
)


class BuildError(RuntimeError):
    """
    Representa un error operacional durante la compilación de una charla o del sitio.
    """


TalkBuilder = Callable[[TalkManifest, Path, str], None]


def compute_talk_base(base_path: str, slug: str) -> str:
    """
    Calcula la ruta base pública asignada a una charla según `base_path`.

    Args:
        base_path (str): Prefijo raíz del sitio (ej. `/` o `/charlas`).
        slug (str): Identificador kebab-case de la charla.

    Returns:
        str: Ruta base normalizada (ej. `/mi-charla` o `/charlas/mi-charla`).
    """
    stripped = base_path.strip("/")
    if not stripped:
        return f"/{slug}"
    return f"/{stripped}/{slug}"


def _require_talk_dir(talk: TalkManifest) -> Path:
    """
    Obtiene y valida que el manifiesto posea un directorio fuente existente.

    Args:
        talk (TalkManifest): Manifiesto de la charla a compilar.

    Returns:
        Path: Directorio fuente resuelto de la charla.

    Raises:
        BuildError: Si `talk.talk_dir` es `None` o no corresponde a un directorio.
    """
    if talk.talk_dir is None or not talk.talk_dir.is_dir():
        raise BuildError(
            f"La charla '{talk.slug}' no tiene un directorio fuente válido: {talk.talk_dir}"
        )
    return talk.talk_dir


def _run_subprocess(
    command: list[str] | str,
    cwd: Path,
    env: dict[str, str] | None = None,
    shell: bool = False,
    context: str = "",
) -> None:
    """
    Ejecuta un subproceso de compilación y convierte cualquier fallo en `BuildError`.

    Args:
        command (list[str] | str): Comando o lista de argumentos a ejecutar.
        cwd (Path): Directorio de trabajo donde corre el subproceso.
        env (dict[str, str] | None, opcional): Variables de entorno explícitas.
        shell (bool, opcional): Habilita interpretación por shell para comandos `custom`.
        context (str, opcional): Etiqueta descriptiva para enriquecer el mensaje de error.

    Raises:
        BuildError: Si el comando falla al lanzarse o termina con código distinto de cero.
    """
    try:
        process = subprocess.run(
            command,
            cwd=cwd,
            env=env,
            shell=shell,
            capture_output=True,
            text=True,
            check=False,
        )
    except OSError as exc:
        raise BuildError(f"No se pudo ejecutar {context}: {exc}") from exc

    if process.returncode != 0:
        details = process.stderr.strip() or process.stdout.strip() or "sin salida"
        raise BuildError(
            f"Falló {context} con código {process.returncode}: {details}"
        )


def build_python_deck_talk(
    talk: TalkManifest,
    target_dir: Path,
    talk_base: str,
) -> None:
    """
    Compila una charla `python-deck` ejecutando su script `back/build_deck.py`.

    Args:
        talk (TalkManifest): Manifiesto validado de la charla.
        target_dir (Path): Directorio destino dentro de `<out_dir>/<slug>`.
        talk_base (str): Ruta base pública calculada para la charla.

    Raises:
        BuildError: Si falta `back/build_deck.py` o el subproceso Python falla.
    """
    _ = talk_base
    talk_dir = _require_talk_dir(talk)
    build_script = talk_dir / "back" / "build_deck.py"
    if not build_script.is_file():
        raise BuildError(
            f"No existe el script de compilación python-deck: {build_script}"
        )

    resolved_target = target_dir.resolve()
    resolved_target.mkdir(parents=True, exist_ok=True)
    _run_subprocess(
        command=[
            sys.executable,
            str(build_script),
            "--output-dir",
            str(resolved_target),
        ],
        cwd=talk_dir,
        context=f"python-deck ({talk.slug})",
    )


def build_astro_talk(
    talk: TalkManifest,
    target_dir: Path,
    talk_base: str,
) -> None:
    """
    Compila una charla `astro` usando `pnpm` y copia su salida `dist/` hacia `target_dir`.

    Args:
        talk (TalkManifest): Manifiesto validado de la charla.
        target_dir (Path): Directorio destino dentro de `<out_dir>/<slug>`.
        talk_base (str): Ruta base pública propagada vía `--base` y `ASTRO_BASE`.

    Raises:
        BuildError: Si falta `pnpm`, falla la instalación/compilación o no existe `dist/`.
    """
    talk_dir = _require_talk_dir(talk)
    pnpm_bin = shutil.which("pnpm")
    if pnpm_bin is None:
        raise BuildError(
            f"No se encontró 'pnpm' en PATH para compilar la charla Astro '{talk.slug}'."
        )

    node_modules_dir = talk_dir / "node_modules"
    if not node_modules_dir.exists():
        _run_subprocess(
            command=[pnpm_bin, "--dir", str(talk_dir), "install", "--frozen-lockfile"],
            cwd=talk_dir,
            context=f"pnpm install ({talk.slug})",
        )

    build_env = {**os.environ, "ASTRO_BASE": talk_base}
    # Omite '--' porque pnpm v11 lo reenvía literal a Astro y rompe la lectura de flags.
    _run_subprocess(
        command=[pnpm_bin, "--dir", str(talk_dir), "build", "--base", talk_base],
        cwd=talk_dir,
        env=build_env,
        context=f"pnpm build ({talk.slug})",
    )

    dist_dir = talk_dir / "dist"
    if not dist_dir.is_dir():
        raise BuildError(
            f"La compilación Astro de '{talk.slug}' no generó el directorio {dist_dir}."
        )

    shutil.copytree(dist_dir, target_dir, dirs_exist_ok=True)


def build_static_talk(
    talk: TalkManifest,
    target_dir: Path,
    talk_base: str,
) -> None:
    """
    Copia los archivos públicos de una charla `static` excluyendo metadatos y cachés.

    Args:
        talk (TalkManifest): Manifiesto validado de la charla.
        target_dir (Path): Directorio destino dentro de `<out_dir>/<slug>`.
        talk_base (str): Ruta base pública calculada para la charla.

    Raises:
        BuildError: Si el directorio fuente de la charla no es válido.
    """
    _ = talk_base
    talk_dir = _require_talk_dir(talk)
    shutil.copytree(
        talk_dir,
        target_dir,
        ignore=shutil.ignore_patterns(*STATIC_IGNORE_PATTERNS),
        dirs_exist_ok=True,
    )


def build_custom_talk(
    talk: TalkManifest,
    target_dir: Path,
    talk_base: str,
) -> None:
    """
    Ejecuta el comando personalizado `build.cmd` de una charla `custom` y copia `build.out_dir`.

    Args:
        talk (TalkManifest): Manifiesto validado de la charla.
        target_dir (Path): Directorio destino dentro de `<out_dir>/<slug>`.
        talk_base (str): Ruta base pública inyectada como `TALK_BASE`.

    Raises:
        BuildError: Si falta la configuración `build`, falla el comando o falta `out_dir`.
    """
    talk_dir = _require_talk_dir(talk)
    if not talk.build:
        raise BuildError(
            f"La charla custom '{talk.slug}' requiere configuración 'build' en talk.json."
        )

    build_cmd = talk.build.get("cmd", "").strip()
    out_rel_dir = talk.build.get("out_dir", "").strip()
    if not build_cmd or not out_rel_dir:
        raise BuildError(
            f"La charla custom '{talk.slug}' tiene 'build.cmd' o 'build.out_dir' vacío."
        )

    resolved_target = target_dir.resolve()
    custom_env = {
        **os.environ,
        "TALK_BASE": talk_base,
        "TALK_OUT_DIR": str(resolved_target),
    }
    _run_subprocess(
        command=build_cmd,
        cwd=talk_dir,
        env=custom_env,
        shell=True,
        context=f"custom build ({talk.slug})",
    )

    resolved_talk_dir = talk_dir.resolve()
    source_out_dir = (resolved_talk_dir / out_rel_dir).resolve()
    if not source_out_dir.is_relative_to(resolved_talk_dir):
        raise BuildError(
            f"El directorio 'build.out_dir' de '{talk.slug}' escapa fuera de {talk_dir}."
        )
    if not source_out_dir.is_dir():
        raise BuildError(
            f"La charla custom '{talk.slug}' no generó el directorio de salida {source_out_dir}."
        )

    shutil.copytree(source_out_dir, target_dir, dirs_exist_ok=True)


ENGINE_BUILDERS: dict[str, TalkBuilder] = {
    "python-deck": build_python_deck_talk,
    "astro": build_astro_talk,
    "static": build_static_talk,
    "custom": build_custom_talk,
}


def build_all(
    talks_dir: Path,
    out_dir: Path,
    base_path: str = DEFAULT_BASE_PATH,
    include_drafts: bool = False,
) -> list[TalkManifest]:
    """
    Limpia `out_dir`, compila todas las charlas activas y construye el Hub selector.

    Args:
        talks_dir (Path): Directorio raíz que contiene las carpetas de charlas.
        out_dir (Path): Directorio de salida consolidado (ej. `_site`).
        base_path (str, opcional): Prefijo URL de despliegue (`/` o `/charlas`).
        include_drafts (bool, opcional): Incluye charlas con `draft=True` si es `True`.

    Returns:
        list[TalkManifest]: Lista ordenada de charlas compiladas e incluidas en el Hub.

    Raises:
        ManifestValidationError: Si algún `talk.json` incumple el contrato.
        BuildError: Si falla la compilación de alguna charla o falta su `entry`.
    """
    resolved_out_dir = out_dir.resolve()
    if resolved_out_dir.exists():
        shutil.rmtree(resolved_out_dir)
    resolved_out_dir.mkdir(parents=True, exist_ok=True)

    talks = discover_talks(talks_dir, include_drafts=include_drafts)
    for talk in talks:
        builder = ENGINE_BUILDERS.get(talk.engine)
        if builder is None:
            raise BuildError(
                f"No existe un compilador registrado para el motor '{talk.engine}'."
            )

        talk_base = compute_talk_base(base_path=base_path, slug=talk.slug)
        target_dir = resolved_out_dir / talk.slug
        builder(talk, target_dir, talk_base)

        entry_path = target_dir / talk.entry
        if not entry_path.exists():
            raise BuildError(
                f"La charla '{talk.slug}' no generó el archivo de entrada requerido '{talk.entry}' en {target_dir}."
            )

    build_hub(talks, out_dir=resolved_out_dir, base_path=base_path)
    return talks


def _parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    """
    Define y parsea los argumentos CLI del orquestador maestro.

    Args:
        argv (list[str] | None, opcional): Lista explícita de argumentos para pruebas.

    Returns:
        argparse.Namespace: Argumentos validados del CLI.
    """
    parser = argparse.ArgumentParser(
        description="Compila todas las charlas activas y genera el Hub selector en _site/."
    )
    parser.add_argument(
        "--talks-dir",
        default=DEFAULT_TALKS_DIR,
        help="Directorio raíz con las carpetas de charlas (por defecto: talks).",
    )
    parser.add_argument(
        "--out-dir",
        default=DEFAULT_OUT_DIR,
        help="Directorio de salida del sitio compilado (por defecto: _site).",
    )
    parser.add_argument(
        "--base-path",
        default=DEFAULT_BASE_PATH,
        help="Prefijo URL público de despliegue (por defecto: /).",
    )
    parser.add_argument(
        "--include-drafts",
        action="store_true",
        help="Incluye charlas marcadas con draft=true en la compilación.",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    """
    Punto de entrada principal del script CLI `scripts/build_all.py`.

    Args:
        argv (list[str] | None, opcional): Argumentos CLI opcionales.

    Returns:
        int: Código de salida (0 en éxito, 1 ante errores de manifiesto o compilación).
    """
    args = _parse_args(argv)
    talks_dir = Path(args.talks_dir)
    out_dir = Path(args.out_dir)

    try:
        compiled_talks = build_all(
            talks_dir=talks_dir,
            out_dir=out_dir,
            base_path=args.base_path,
            include_drafts=args.include_drafts,
        )
    except (ManifestValidationError, BuildError, OSError) as exc:
        print(f"Error al compilar el sitio: {exc}", file=sys.stderr)
        return 1

    print(
        f"Compilación completada: {len(compiled_talks)} charlas generadas en '{out_dir}'."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
