"""
Archivo: tests/unit/test_setup.py
Fecha de modificación: 15/11/2026
Autor: Alex Prieto <alexprieto1997@gmail.com>

Descripción:
Valida el scaffolding inicial del repositorio `charlas`, incluyendo la
configuración de `pyproject.toml`, la separación de dependencias en
`requirements.txt`, la estructura base de directorios e importabilidad de
los paquetes `shared` y `hub`.

Acciones Principales:
    - Comprueba la validez sintáctica y campos clave de `pyproject.toml`.
    - Verifica las dependencias ligeras de CI y el respaldo de ML por charla.
    - Valida la existencia de directorios base y archivos `__init__.py`.
    - Comprueba la importación de `shared`, `shared.python_deck` y `hub`.
    - Simula la ejecución CLI de `pytest` desde la raíz del repositorio.

Estructura Interna:
    - `_parse_requirements`: Extrae líneas de paquetes activas de un `requirements.txt`.
    - `test_pyproject_toml_configuration`: Valida `pyproject.toml` con `tomllib`.
    - `test_requirements_split_and_backup`: Valida manifiestos de dependencias.
    - `test_base_directory_structure_exists`: Verifica carpetas y paquetes base.
    - `test_core_packages_are_importable`: Verifica importación de paquetes.
    - `test_pytest_cli_invocation_succeeds`: Simula ejecución real por CLI.

Entradas / Dependencias:
    - `pyproject.toml`, `requirements.txt` y `talks/2026-forecasting-ia/requirements.txt`.

Salidas / Efectos:
    - Reporta aprobación o fallo de los criterios de aceptación de T0.1.1.

Ejemplo de Integración:
    python -m pytest tests/unit/test_setup.py -v
"""

import importlib
import subprocess
import sys
import tomllib
from pathlib import Path

REPO_ROOT: Path = Path(__file__).resolve().parents[2]

EXPECTED_ROOT_REQUIREMENTS: tuple[str, ...] = (
    "pandas>=2.0.0",
    "numpy>=1.24.0",
    "jsonschema>=4.20.0",
    "pytest>=8.0.0",
    "playwright>=1.40.0",
)

EXPECTED_ML_REQUIREMENTS: tuple[str, ...] = (
    "scikit-learn>=1.3.0",
    "lightgbm>=4.0.0",
    "torch>=2.0.0",
    "chronos-forecasting>=0.0.4",
    "timesfm>=0.1.0",
)

REQUIRED_DIRECTORIES: tuple[str, ...] = (
    "shared",
    "shared/python_deck",
    "shared/python_deck/assets",
    "hub",
    "hub/assets",
    "talks",
    "talks/2026-forecasting-ia",
    "tests",
    "tests/unit",
    "tests/integration",
    "tests/e2e",
)

REQUIRED_INIT_FILES: tuple[str, ...] = (
    "shared/__init__.py",
    "shared/python_deck/__init__.py",
    "hub/__init__.py",
    "tests/__init__.py",
    "tests/unit/__init__.py",
    "tests/integration/__init__.py",
    "tests/e2e/__init__.py",
)


def _parse_requirements(requirements_path: Path) -> list[str]:
    """
    Lee un archivo `requirements.txt` y retorna las especificaciones no vacías.

    Args:
        requirements_path (Path): Ruta al archivo `requirements.txt`.

    Returns:
        list[str]: Lista de dependencias declaradas sin comentarios ni líneas vacías.
    """
    raw_lines = requirements_path.read_text(encoding="utf-8").splitlines()
    return [
        line.strip()
        for line in raw_lines
        if line.strip() and not line.strip().startswith("#")
    ]


def test_pyproject_toml_configuration() -> None:
    """
    Verifica que `pyproject.toml` es TOML válido y declara la configuración de `charlas`.
    """
    pyproject_path = REPO_ROOT / "pyproject.toml"
    assert pyproject_path.is_file(), "Falta pyproject.toml en la raíz del repo"

    with pyproject_path.open("rb") as file_handle:
        pyproject_data = tomllib.load(file_handle)

    assert pyproject_data["project"]["name"] == "charlas"
    pytest_options = pyproject_data["tool"]["pytest"]["ini_options"]
    assert pytest_options["pythonpath"] == ["."]
    assert pytest_options["testpaths"] == ["tests"]


def test_requirements_split_and_backup() -> None:
    """
    Verifica las 5 dependencias ligeras raíz y el respaldo ML en la charla 2026.
    """
    root_requirements_path = REPO_ROOT / "requirements.txt"
    talk_requirements_path = REPO_ROOT / "talks" / "2026-forecasting-ia" / "requirements.txt"

    assert root_requirements_path.is_file(), "Falta requirements.txt en la raíz"
    assert talk_requirements_path.is_file(), "Falta respaldo requirements.txt en talks/2026-forecasting-ia"

    root_specs = _parse_requirements(root_requirements_path)
    assert set(root_specs) == set(EXPECTED_ROOT_REQUIREMENTS)
    assert len(root_specs) == 5

    talk_specs = set(_parse_requirements(talk_requirements_path))
    for ml_dep in EXPECTED_ML_REQUIREMENTS:
        assert ml_dep in talk_specs, f"Falta dependencia ML respaldada: {ml_dep}"


def test_base_directory_structure_exists() -> None:
    """
    Comprueba que existen los directorios base y archivos `__init__.py` esperados.
    """
    for relative_dir in REQUIRED_DIRECTORIES:
        target_dir = REPO_ROOT / relative_dir
        assert target_dir.is_dir(), f"Falta el directorio requerido: {relative_dir}"

    for relative_init in REQUIRED_INIT_FILES:
        target_init = REPO_ROOT / relative_init
        assert target_init.is_file(), f"Falta el archivo __init__.py requerido: {relative_init}"


def test_core_packages_are_importable() -> None:
    """
    Verifica que `shared`, `shared.python_deck` y `hub` son importables desde la raíz.
    """
    shared_pkg = importlib.import_module("shared")
    python_deck_pkg = importlib.import_module("shared.python_deck")
    hub_pkg = importlib.import_module("hub")

    assert shared_pkg.__name__ == "shared"
    assert python_deck_pkg.__name__ == "shared.python_deck"
    assert hub_pkg.__name__ == "hub"


def test_pytest_cli_invocation_succeeds() -> None:
    """
    Simula la invocación de `pytest` por línea de comandos como usuario desde la raíz.
    """
    # Excluye esta misma prueba en el subproceso para evitar recursión infinita.
    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "pytest",
            "tests/unit/test_setup.py",
            "-k",
            "not test_pytest_cli_invocation_succeeds",
            "-q",
        ],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode == 0, f"Falló pytest CLI:\n{result.stdout}\n{result.stderr}"
    assert "4 passed" in result.stdout
