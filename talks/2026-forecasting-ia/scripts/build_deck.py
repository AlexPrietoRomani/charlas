"""
Archivo: talks/2026-forecasting-ia/scripts/build_deck.py
Fecha de modificación: 15/11/2026
Autor: Alex Prieto <alexprieto1997@gmail.com>

Descripción:
Proxy de compatibilidad hacia el motor backend del deck ubicado en
`talks/2026-forecasting-ia/back/build_deck.py`. Permite invocar la compilación
de la charla desde `scripts/build_deck.py` con soporte completo para `--output-dir`.

Acciones Principales:
    - Añade `talks/2026-forecasting-ia/back/` al inicio de `sys.path`.
    - Delega la compilación en `build_deck(output_dir=...)` y `main()`.

Estructura Interna:
    - `main`: Punto de entrada CLI delegado hacia `back/build_deck.py`.

Entradas / Dependencias:
    - `talks/2026-forecasting-ia/back/build_deck.py`.

Salidas / Efectos:
    - Genera `index.html` y `presentacion.html` en el directorio configurado.

Ejecución:
    python talks/2026-forecasting-ia/scripts/build_deck.py [--output-dir RUTA]

Ejemplo de Uso:
    python talks/2026-forecasting-ia/scripts/build_deck.py --output-dir _site/2026-forecasting-ia

Argumentos:
    - --output-dir: Path | None - Directorio destino opcional.
"""

import sys
from pathlib import Path

BASE_DIR: Path = Path(__file__).resolve().parent.parent
BACK_DIR: Path = BASE_DIR / "back"

if str(BACK_DIR) not in sys.path:
    sys.path.insert(0, str(BACK_DIR))

from build_deck import build_deck, main  # noqa: E402, F401

if __name__ == "__main__":
    main()
