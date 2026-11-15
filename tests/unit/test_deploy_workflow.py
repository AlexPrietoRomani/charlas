"""
Archivo: tests/unit/test_deploy_workflow.py
Fecha de modificación: 15/11/2026
Autor: Alex Prieto <alexprieto1997@gmail.com>

Descripción:
Valida la configuración CI/CD de GitHub Pages en `.github/workflows/deploy.yml`
y simula localmente la compilación del sitio completo con `--base-path /charlas`
en un directorio temporal para verificar las rutas generadas.

Acciones Principales:
    - Parsea `.github/workflows/deploy.yml` con `yaml.safe_load`.
    - Verifica triggers (`master`, `workflow_dispatch`), permisos y concurrencia.
    - Comprueba la presencia y orden lógico de Python 3.11, Node 22, pnpm,
      `scripts/build_all.py --base-path /charlas`, `pytest` y despliegue de `_site`.
    - Simula la ejecución de `scripts/build_all.py --out-dir <tmp_path/_site> --base-path /charlas`
      y valida prefijos `/charlas/...` en `talks.json` y `2026-falsa-alarma/index.html`.

Estructura Interna:
    - `_load_workflow`: Carga y valida la raíz YAML del archivo de workflow.
    - `_find_step_by_uses`: Busca un paso por prefijo o nombre exacto de `uses`.
    - `test_deploy_workflow_triggers_and_permissions`: Prueba unitaria de metadatos YAML.
    - `test_deploy_workflow_steps_and_order`: Prueba unitaria de pasos y orden CI.
    - `test_user_simulation_build_with_charlas_base_path`: Simulación de build productivo.

Entradas / Dependencias:
    - `.github/workflows/deploy.yml`, `scripts/build_all.py` y `pyyaml`.

Salidas / Efectos:
    - Reporta el cumplimiento de los Criterios de Aceptación de la Tarea T3.1.1.

Ejemplo de Integración:
    python -m pytest tests/unit/test_deploy_workflow.py -v
"""

import json
from pathlib import Path
import subprocess
import sys
from typing import Any

import yaml

REPO_ROOT: Path = Path(__file__).resolve().parents[2]
WORKFLOW_PATH: Path = REPO_ROOT / ".github" / "workflows" / "deploy.yml"
BUILD_ALL_SCRIPT: Path = REPO_ROOT / "scripts" / "build_all.py"
EXPECTED_BASE_PATH: str = "/charlas"
EXPECTED_WORKFLOW_NAME: str = "Build and Deploy Charlas Hub to GitHub Pages"


def _load_workflow() -> dict[str, Any]:
    """
    Lee y parsea `.github/workflows/deploy.yml` utilizando `yaml.safe_load`.

    Returns:
        dict[str, Any]: Estructura YAML deserializada del workflow.
    """
    assert WORKFLOW_PATH.is_file(), f"Falta el workflow en {WORKFLOW_PATH}"
    parsed = yaml.safe_load(WORKFLOW_PATH.read_text(encoding="utf-8"))
    assert isinstance(parsed, dict), "El workflow debe deserializarse como un diccionario YAML."
    return parsed


def _find_step_by_uses(steps: list[dict[str, Any]], action_name: str) -> tuple[int, dict[str, Any]]:
    """
    Localiza el índice y definición de un paso según su clave `uses`.

    Args:
        steps (list[dict[str, Any]]): Lista de pasos declarados en el job.
        action_name (str): Identificador exacto de la acción (ej. `actions/setup-python@v5`).

    Returns:
        tuple[int, dict[str, Any]]: Índice base cero y diccionario del paso encontrado.
    """
    for index, step in enumerate(steps):
        if step.get("uses") == action_name:
            return index, step
    raise AssertionError(f"No se encontró ningún paso con uses='{action_name}'.")


def test_deploy_workflow_triggers_and_permissions() -> None:
    """
    Verifica nombre, triggers (`master` y `workflow_dispatch`), permisos y concurrencia.
    """
    workflow = _load_workflow()

    assert workflow.get("name") == EXPECTED_WORKFLOW_NAME

    # En YAML 1.1 la clave sin comillas `on:` se parsea como booleano `True`.
    triggers = workflow.get("on") if "on" in workflow else workflow.get(True)
    assert isinstance(triggers, dict), "El workflow debe declarar bloque `on:`."
    assert triggers["push"]["branches"] == ["master"]
    assert "workflow_dispatch" in triggers

    assert workflow.get("permissions") == {
        "contents": "read",
        "pages": "write",
        "id-token": "write",
    }
    assert workflow.get("concurrency") == {
        "group": "pages",
        "cancel-in-progress": False,
    }


def test_deploy_workflow_steps_and_order() -> None:
    """
    Verifica toolchains, instalación, build con `--base-path /charlas`, `pytest` y Pages.
    """
    workflow = _load_workflow()
    job = workflow["jobs"]["build-and-deploy"]

    assert job["runs-on"] == "ubuntu-latest"
    assert job["environment"]["name"] == "github-pages"

    steps: list[dict[str, Any]] = job["steps"]

    checkout_idx, _ = _find_step_by_uses(steps, "actions/checkout@v4")
    python_idx, python_step = _find_step_by_uses(steps, "actions/setup-python@v5")
    pnpm_idx, pnpm_step = _find_step_by_uses(steps, "pnpm/action-setup@v4")
    node_idx, node_step = _find_step_by_uses(steps, "actions/setup-node@v4")
    configure_idx, _ = _find_step_by_uses(steps, "actions/configure-pages@v4")
    upload_idx, upload_step = _find_step_by_uses(steps, "actions/upload-pages-artifact@v3")
    deploy_idx, deploy_step = _find_step_by_uses(steps, "actions/deploy-pages@v4")

    assert str(python_step["with"]["python-version"]) == "3.11"
    assert str(pnpm_step["with"]["version"]) == "10"
    assert str(node_step["with"]["node-version"]) == "22"
    assert node_step["with"]["cache"] == "pnpm"
    assert node_step["with"]["cache-dependency-path"] == "talks/2026-falsa-alarma/pnpm-lock.yaml"
    assert upload_step["with"]["path"] == "_site"
    assert deploy_step["id"] == "deployment"

    # El caché pnpm de setup-node requiere que pnpm/action-setup se ejecute antes.
    assert checkout_idx < python_idx
    assert pnpm_idx < node_idx

    run_commands = [
        (idx, step["run"])
        for idx, step in enumerate(steps)
        if isinstance(step.get("run"), str)
    ]
    joined_runs = "\n".join(cmd for _, cmd in run_commands)

    assert "requirements.txt" in joined_runs
    assert "pnpm --dir talks/2026-falsa-alarma install --frozen-lockfile" in joined_runs

    build_idx = next(
        (idx for idx, cmd in run_commands if "scripts/build_all.py --base-path /charlas" in cmd),
        None,
    )
    pytest_idx = next(
        (idx for idx, cmd in run_commands if "pytest" in cmd),
        None,
    )

    assert build_idx is not None, "Falta el paso que ejecuta `scripts/build_all.py --base-path /charlas`."
    assert pytest_idx is not None, "Falta el paso que ejecuta `pytest` antes de subir el artefacto."
    assert node_idx < build_idx < pytest_idx < configure_idx < upload_idx < deploy_idx


def test_user_simulation_build_with_charlas_base_path(tmp_path: Path) -> None:
    """
    Simula la compilación del workflow usando `--base-path /charlas` sobre `tmp_path`.
    """
    out_dir = tmp_path / "_site"

    result = subprocess.run(
        [
            sys.executable,
            str(BUILD_ALL_SCRIPT),
            "--out-dir",
            str(out_dir),
            "--base-path",
            EXPECTED_BASE_PATH,
        ],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode == 0, (
        f"Falló la compilación CLI con --base-path /charlas:\n"
        f"STDOUT:\n{result.stdout}\nSTDERR:\n{result.stderr}"
    )

    talks_json_path = out_dir / "talks.json"
    hub_index_path = out_dir / "index.html"
    falsa_alarma_index_path = out_dir / "2026-falsa-alarma" / "index.html"

    assert talks_json_path.is_file(), "No se generó talks.json en el build simulado."
    assert hub_index_path.is_file(), "No se generó index.html del Hub."
    assert falsa_alarma_index_path.is_file(), "No se generó 2026-falsa-alarma/index.html."

    catalog = json.loads(talks_json_path.read_text(encoding="utf-8"))
    assert catalog["base_path"] == EXPECTED_BASE_PATH
    assert catalog["total_talks"] >= 2

    talk_urls = {entry["slug"]: entry["url"] for entry in catalog["talks"]}
    assert talk_urls["2026-forecasting-ia"] == "/charlas/2026-forecasting-ia/"
    assert talk_urls["2026-falsa-alarma"] == "/charlas/2026-falsa-alarma/"

    falsa_alarma_html = falsa_alarma_index_path.read_text(encoding="utf-8")
    assert "/charlas/2026-falsa-alarma/" in falsa_alarma_html
