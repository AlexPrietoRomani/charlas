"""
Archivo: tests/integration/test_build_all.py
Fecha de modificación: 15/11/2026
Autor: Alex Prieto <alexprieto1997@gmail.com>

Descripción:
Valida el orquestador maestro `scripts/build_all.py` mediante pruebas unitarias
sobre motores `static` y `custom` en directorios temporales, verificación de fallos
controlados cuando falta el archivo `entry` y una simulación de usuario completa
sobre el catálogo real en `talks/`.

Acciones Principales:
    - Verifica la compilación de charlas `static` (con exclusión de metadatos) y `custom`.
    - Valida la propagación de `TALK_BASE`, `TALK_OUT_DIR` y limpieza previa de `out_dir`.
    - Comprueba el lanzamiento de `BuildError` y código de salida != 0 si falta `entry`.
    - Simula la ejecución CLI real sobre `talks/` con `--base-path /charlas`.

Estructura Interna:
    - `_write_talk_manifest`: Helper local para materializar `talk.json` de prueba.
    - `test_build_static_and_custom_talks_in_tmp`: Prueba unitaria multi-motor en `tmp_path`.
    - `test_build_raises_when_entry_missing`: Prueba unitaria de validación de `entry`.
    - `test_user_simulation_full_repo_build_all`: Simulación end-to-end del repo real.

Entradas / Dependencias:
    - `scripts.build_all` (`BuildError`, `build_all`, `compute_talk_base`, `main`).
    - Directorio real `talks/` y herramientas Python/`pnpm`.

Salidas / Efectos:
    - Reporta aprobación o fallo de los criterios de aceptación de la Tarea T2.2.1.

Ejemplo de Integración:
    python -m pytest tests/integration/test_build_all.py -v
"""

import json
from pathlib import Path
import subprocess
import sys
from typing import Any

import pytest

from scripts.build_all import BuildError, build_all, compute_talk_base, main

REPO_ROOT: Path = Path(__file__).resolve().parents[2]
BUILD_ALL_SCRIPT: Path = REPO_ROOT / "scripts" / "build_all.py"


def _write_talk_manifest(talk_dir: Path, payload: dict[str, Any]) -> None:
    """
    Escribe un archivo `talk.json` dentro de `talk_dir`.

    Args:
        talk_dir (Path): Carpeta destino de la charla fixture.
        payload (dict[str, Any]): Contenido JSON del manifiesto.
    """
    talk_dir.mkdir(parents=True, exist_ok=True)
    (talk_dir / "talk.json").write_text(
        json.dumps(payload, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )


def test_build_static_and_custom_talks_in_tmp(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """
    Verifica el despacho de `static` y `custom`, exclusiones, variables de entorno y Hub.
    """
    monkeypatch.chdir(tmp_path)
    talks_dir = Path("talks")
    out_dir = Path("_site")

    # Prepara un archivo residual para verificar la limpieza idempotente de `out_dir`.
    out_dir.mkdir(parents=True, exist_ok=True)
    stale_file = out_dir / "residual_antiguo.txt"
    stale_file.write_text("obsoleto", encoding="utf-8")

    static_dir = talks_dir / "2026-demo-static"
    _write_talk_manifest(
        static_dir,
        {
            "slug": "2026-demo-static",
            "title": "Charla Static Demo",
            "event": "Meetup Local",
            "date": "2026-05-10",
            "engine": "static",
            "tags": ["html"],
            "cover": "cover.png",
        },
    )
    (static_dir / "index.html").write_text(
        "<!doctype html><html><body><h1>Static OK</h1></body></html>",
        encoding="utf-8",
    )
    (static_dir / "README.md").write_text("# Documentación interna", encoding="utf-8")
    (static_dir / "cover.png").write_bytes(b"PNG_STATIC_COVER")
    (static_dir / "__pycache__").mkdir()
    (static_dir / "__pycache__" / "cache.pyc").write_bytes(b"CACHE")

    custom_dir = talks_dir / "2026-demo-custom"
    _write_talk_manifest(
        custom_dir,
        {
            "slug": "2026-demo-custom",
            "title": "Charla Custom Demo",
            "event": "Conf Custom",
            "date": "2026-09-20",
            "engine": "custom",
            "tags": ["custom"],
            "entry": "deck.html",
            "build": {
                "cmd": f'"{sys.executable}" custom_builder.py',
                "out_dir": "dist_custom",
            },
        },
    )
    (custom_dir / "custom_builder.py").write_text(
        "\n".join(
            [
                "import os",
                "from pathlib import Path",
                "out_dir = Path('dist_custom')",
                "out_dir.mkdir(parents=True, exist_ok=True)",
                "talk_base = os.environ.get('TALK_BASE', '')",
                "target_out = os.environ.get('TALK_OUT_DIR', '')",
                "(out_dir / 'deck.html').write_text(",
                "    f'<main data-base=\"{talk_base}\" data-out=\"{target_out}\">Custom OK</main>',",
                "    encoding='utf-8',",
                ")",
            ]
        ),
        encoding="utf-8",
    )

    assert compute_talk_base("/", "2026-demo-static") == "/2026-demo-static"
    assert compute_talk_base("/charlas", "2026-demo-custom") == "/charlas/2026-demo-custom"

    compiled = build_all(talks_dir=talks_dir, out_dir=out_dir, base_path="/charlas")
    assert [talk.slug for talk in compiled] == ["2026-demo-custom", "2026-demo-static"]
    assert not stale_file.exists()

    static_out = out_dir / "2026-demo-static"
    assert (static_out / "index.html").is_file()
    assert "Static OK" in (static_out / "index.html").read_text(encoding="utf-8")
    assert (static_out / "cover.png").is_file()
    assert not (static_out / "talk.json").exists()
    assert not (static_out / "README.md").exists()
    assert not (static_out / "__pycache__").exists()

    custom_out = out_dir.resolve() / "2026-demo-custom"
    custom_html = (custom_out / "deck.html").read_text(encoding="utf-8")
    assert 'data-base="/charlas/2026-demo-custom"' in custom_html
    assert f'data-out="{custom_out}"' in custom_html
    assert "Custom OK" in custom_html

    assert (out_dir / "index.html").is_file()
    catalog = json.loads((out_dir / "talks.json").read_text(encoding="utf-8"))
    assert catalog["total_talks"] == 2
    assert catalog["base_path"] == "/charlas"


def test_build_raises_when_entry_missing(tmp_path: Path) -> None:
    """
    Comprueba que `build_all()` lanza `BuildError` y el CLI retorna 1 si falta `entry`.
    """
    talks_dir = tmp_path / "talks"
    out_dir = tmp_path / "_site"
    broken_dir = talks_dir / "2026-sin-entry"
    _write_talk_manifest(
        broken_dir,
        {
            "slug": "2026-sin-entry",
            "title": "Charla Sin Archivo Entry",
            "event": "Meetup",
            "date": "2026-06-01",
            "engine": "static",
            "tags": ["static"],
            "entry": "index.html",
        },
    )
    (broken_dir / "otro.html").write_text("<p>Sin index.html</p>", encoding="utf-8")

    with pytest.raises(BuildError, match="index.html"):
        build_all(talks_dir=talks_dir, out_dir=out_dir, base_path="/")

    exit_code = main(
        [
            "--talks-dir",
            str(talks_dir),
            "--out-dir",
            str(out_dir),
            "--base-path",
            "/",
        ]
    )
    assert exit_code == 1


def test_user_simulation_full_repo_build_all(tmp_path: Path) -> None:
    """
    Simula la compilación CLI completa sobre `talks/` con `--base-path /charlas`.
    """
    out_dir = tmp_path / "_site"

    proc = subprocess.run(
        [
            sys.executable,
            str(BUILD_ALL_SCRIPT),
            "--talks-dir",
            str(REPO_ROOT / "talks"),
            "--out-dir",
            str(out_dir),
            "--base-path",
            "/charlas",
        ],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
        check=False,
    )

    assert proc.returncode == 0, (
        f"Falló `scripts/build_all.py`:\nSTDOUT:\n{proc.stdout}\nSTDERR:\n{proc.stderr}"
    )

    hub_index = out_dir / "index.html"
    talks_json = out_dir / "talks.json"
    profile_img = out_dir / "hub_assets" / "profile_alex.jpg"
    forecasting_index = out_dir / "2026-forecasting-ia" / "index.html"
    falsa_alarma_index = out_dir / "2026-falsa-alarma" / "index.html"
    elqui_csv = out_dir / "2026-falsa-alarma" / "data" / "clima_valle_elqui.csv"

    assert hub_index.is_file()
    assert talks_json.is_file()
    assert profile_img.is_file()
    assert forecasting_index.is_file()
    assert falsa_alarma_index.is_file()
    assert elqui_csv.is_file()

    falsa_alarma_html = falsa_alarma_index.read_text(encoding="utf-8")
    assert "/charlas/2026-falsa-alarma/" in falsa_alarma_html
