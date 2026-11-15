"""
Archivo: tests/unit/test_repo_structure.py
Fecha de modificación: 15/11/2026
Autor: Alex Prieto <alexprieto1997@gmail.com>

Descripción:
Valida la limpieza estructural definitiva de la raíz del repositorio `charlas`,
asegurando que los directorios y archivos legacy de `charla_forecasting` ya no
residen en la raíz, que la arquitectura multicharla vive en sus rutas canónicas y
que `README.md` documenta los flujos esenciales para el usuario.

Acciones Principales:
    - Comprueba la ausencia de directorios y archivos legacy en la raíz del repo.
    - Verifica la existencia de los paquetes, charlas, plantillas y docs canónicos.
    - Simula la lectura de `README.md` validando título, catálogo, comandos y motores.

Estructura Interna:
    - `test_root_has_no_legacy_duplicates`: Prueba unitaria de limpieza en raíz.
    - `test_canonical_repository_structure_exists`: Prueba unitaria de rutas canónicas.
    - `test_user_simulation_readme_documents_workflows`: Simulación de lectura del `README.md`.

Entradas / Dependencias:
    - Estructura de archivos del repositorio y `README.md`.

Salidas / Efectos:
    - Reporta aprobación o fallo de los Criterios de Aceptación de la Tarea T3.3.1.

Ejemplo de Integración:
    python -m pytest tests/unit/test_repo_structure.py -v
"""

from pathlib import Path

REPO_ROOT: Path = Path(__file__).resolve().parents[2]

LEGACY_ROOT_PATHS: tuple[str, ...] = (
    "front",
    "back",
    "data",
    "notebooks",
    "articles",
    "models",
    "screenshots",
    ".playwright-mcp",
    "presentacion.html",
    "mockup_hub.html",
    "refs.bib",
    "scripts/caso_1",
    "scripts/caso_2",
    "scripts/pagina",
    "scripts/build_deck.py",
    "scripts/README.md",
    "docs/images",
    "docs/notebooklm",
    "docs/papers",
    "docs/reference",
    "docs/audit_layout",
    "docs/PLANTILLA PONENTES.pptx",
)

CANONICAL_DIRS: tuple[str, ...] = (
    "hub",
    "shared",
    "talks/2026-forecasting-ia",
    "talks/2026-forecasting-ia/articles",
    "talks/2026-forecasting-ia/models",
    "talks/2026-falsa-alarma",
    "talks/_template_python_deck",
    "talks/_template_static",
)

CANONICAL_FILES: tuple[str, ...] = (
    "README.md",
    "scripts/build_all.py",
    ".github/workflows/deploy.yml",
    "docs/description_proyecto.md",
    "docs/architecture/architecture.md",
    "docs/db/diseno_db.md",
    "docs/ejecucion.md",
)

REQUIRED_README_TERMS: tuple[str, ...] = (
    "# Charlas & Ponencias — Alex Prieto Romani",
    "https://alexprietoromani.github.io/charlas/",
    "2026-forecasting-ia",
    "2026-falsa-alarma",
    "build_all.py",
    "http.server -d _site 8000",
    "python-deck",
    "astro",
    "static",
    "custom",
    "_template_python_deck",
    "_template_static",
    ".github/workflows/deploy.yml",
    "git remote set-url",
)


def test_root_has_no_legacy_duplicates() -> None:
    """
    Verifica que los archivos y directorios legacy migrados ya no existen en la raíz.
    """
    existing_legacy = [
        rel_path
        for rel_path in LEGACY_ROOT_PATHS
        if (REPO_ROOT / rel_path).exists()
    ]
    assert not existing_legacy, (
        f"Persisten rutas legacy duplicadas en la raíz: {existing_legacy}"
    )


def test_canonical_repository_structure_exists() -> None:
    """
    Comprueba que el Hub, módulos compartidos, charlas, plantillas y docs viven en sus rutas canónicas.
    """
    for rel_dir in CANONICAL_DIRS:
        target_dir = REPO_ROOT / rel_dir
        assert target_dir.is_dir(), f"Falta el directorio canónico requerido: {rel_dir}"

    for rel_file in CANONICAL_FILES:
        target_file = REPO_ROOT / rel_file
        assert target_file.is_file(), f"Falta el archivo canónico requerido: {rel_file}"


def test_user_simulation_readme_documents_workflows() -> None:
    """
    Simula la lectura de `README.md` validando la documentación de compilación, motores y despliegue.
    """
    readme_path = REPO_ROOT / "README.md"
    assert readme_path.is_file(), "Falta README.md en la raíz del repositorio."

    readme_text = readme_path.read_text(encoding="utf-8")
    missing_terms = [
        term for term in REQUIRED_README_TERMS if term not in readme_text
    ]
    assert not missing_terms, (
        f"README.md omite documentación esperada: {missing_terms}"
    )
