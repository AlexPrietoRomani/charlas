"""
Archivo: talks/2026-sdd-proyectos-reales/back/build_deck.py
Fecha de modificación: 15/11/2026
Autor: Alex Prieto <alexprieto1997@gmail.com>

Descripción:
Compilador de la charla `2026-sdd-proyectos-reales` (motor `python-deck`).
Carga el sistema de diseño (`front/styles.py`), las diapositivas
(`front/slides_p1.py`, `front/slides_p2.py`) y las notas del orador
(`front/notes.py`), y genera un HTML autocontenido con Chart.js incrustado
desde `shared/python_deck/assets/chart.umd.min.js` (con fallback CDN).

Acciones Principales:
    - `build_deck(output_dir)`: compila `index.html` y `presentacion.html`.
    - Calcula `window.DECK_META` (total + 5 bloques con rangos de slides y minutos),
      `window.SPEAKER_NOTES` y `window.CHART_SPECS` serializados sin NaN.
    - Renderiza `<section class="slide" data-index="N" data-block="B">` con
      fragmentos progresivos y diagramas SVG animados.
    - CLI: `python back/build_deck.py --output-dir <ruta>`.

Estructura Interna:
    - `_load_module`: importación por ruta de los módulos `front/`.
    - `_script_safe`: escapa `</script>` para inyección inline segura.
    - `_merge_slides` / `_compute_blocks`: normalización y metadatos del deck.
    - `_render_section`: una diapositiva como HTML.

Entradas / Dependencias:
    - `front/*.py` de esta charla y `shared/python_deck/assets/chart.umd.min.js`.

Salidas / Efectos:
    - Dos archivos HTML idénticos y autocontenidos en `output_dir`.

Ejemplo de Integración:
    python talks/2026-sdd-proyectos-reales/back/build_deck.py --output-dir dist
"""

import argparse
import importlib.util
import json
from pathlib import Path
from types import ModuleType
from typing import Any

HERE: Path = Path(__file__).resolve().parent
BASE_DIR: Path = HERE.parent
REPO_ROOT: Path = HERE.parents[2]
SHARED_CHARTJS_PATH: Path = (
    REPO_ROOT / "shared" / "python_deck" / "assets" / "chart.umd.min.js"
)

TITLE: str = "Aplicación de SDD en proyectos reales — SDD + ODD + EGM con project-suite"

BLOCK_MINUTES: dict[int, tuple[int, int]] = {
    1: (0, 25),
    2: (25, 50),
    3: (50, 75),
    4: (75, 100),
    5: (100, 120),
}


def _load_module(relative_path: Path, module_name: str) -> ModuleType:
    """
    Importa dinámicamente un módulo de `front/` por ruta absoluta.

    Args:
        relative_path (Path): Ruta del archivo `.py` dentro de la charla.
        module_name (str): Nombre técnico del módulo cargado.

    Returns:
        ModuleType: Módulo ejecutado listo para consulta de constantes.
    """
    spec = importlib.util.spec_from_file_location(module_name, relative_path)
    if spec is None or spec.loader is None:
        raise ImportError(f"No se pudo importar el módulo: {relative_path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _script_safe(text: str) -> str:
    """
    Escapa secuencias `</script` para inyección segura dentro de un `<script>`.

    Args:
        text (str): Contenido original (JS minificado o JSON).

    Returns:
        str: Contenido sin secuencias de cierre de script prematuras.
    """
    return text.replace("</script", "<\\/script")


def _dump_json(payload: Any) -> str:
    """
    Serializa a JSON estricto (UTF-8, sin NaN/Infinity) y apto para `<script>`.

    Args:
        payload (Any): Objeto serializable (dicts, listas, escalares).

    Returns:
        str: JSON como cadena segura para incrustación inline.
    """
    raw = json.dumps(payload, ensure_ascii=False, allow_nan=False)
    return raw.replace("</", "<\\/")


def _merge_slides() -> list[dict[str, Any]]:
    """
    Une las diapositivas de ambas partes y normaliza sus campos mínimos.

    Returns:
        list[dict[str, Any]]: 24 diapositivas ordenadas con id, bloque y cuerpo.

    Raises:
        ValueError: Si hay ids duplicados, bloques vacíos o bloques no contiguos.
    """
    p1 = _load_module(BASE_DIR / "front" / "slides_p1.py", "sdd_slides_p1")
    p2 = _load_module(BASE_DIR / "front" / "slides_p2.py", "sdd_slides_p2")

    slides: list[dict[str, Any]] = []
    for raw in list(p1.SLIDES_P1) + list(p2.SLIDES_P2):
        slide = dict(raw)
        slide.setdefault("layout", "")
        slide.setdefault("sub", "")
        slides.append(slide)

    ids = [s["id"] for s in slides]
    if len(ids) != len(set(ids)):
        raise ValueError("Ids de diapositiva duplicados en front/slides_p*.py")

    blocks = [s["block"] for s in slides]
    if blocks != sorted(blocks):
        raise ValueError("Los bloques deben ser contiguos y ascendentes")

    return slides


def _compute_blocks(slides: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """
    Calcula los rangos contiguos de cada bloque (slides 1-based + minutos).

    Args:
        slides (list[dict[str, Any]]): Diapositivas normalizadas.

    Returns:
        list[dict[str, Any]]: Metadatos por bloque: block, start, end, from, to.
    """
    blocks: list[dict[str, Any]] = []
    for number in sorted(set(s["block"] for s in slides)):
        indexes = [i + 1 for i, s in enumerate(slides) if s["block"] == number]
        from_min, to_min = BLOCK_MINUTES[number]
        blocks.append(
            {
                "block": number,
                "start": min(indexes),
                "end": max(indexes),
                "from": from_min,
                "to": to_min,
            }
        )
    return blocks


def _render_section(index: int, slide: dict[str, Any]) -> str:
    """
    Renderiza una diapositiva como `<section>` con su cabecera y cuerpo.

    Args:
        index (int): Índice 1-based de la diapositiva.
        slide (dict[str, Any]): Datos normalizados de la diapositiva.

    Returns:
        str: HTML de la sección.
    """
    layout = slide.get("layout", "")
    classes = "slide" if not layout else f"slide {layout}"
    parts = [
        f'<section class="{classes}" data-index="{index}" '
        f'data-block="{slide["block"]}" data-id="{slide["id"]}">'
    ]

    kicker = slide.get("kicker", "")
    if kicker:
        parts.append(f'<div class="kicker">{kicker}</div>')

    title = slide.get("title", "")
    if layout in ("cover", "divider"):
        parts.append(f"<h1>{title}</h1>")
    else:
        parts.append(f'<h1 class="slide-title">{title}</h1>')
        parts.append('<div class="rule"></div>')

    sub = slide.get("sub", "")
    if sub:
        css_class = "c-sub" if layout == "cover" else "slide-sub"
        parts.append(f'<p class="{css_class}">{sub}</p>')

    body = slide.get("body", "")
    if body:
        if layout in ("cover", "divider"):
            parts.append(body)
        else:
            parts.append(f'<div class="body-area">{body}</div>')

    parts.append("</section>")
    return "\n".join(parts)


def _render_segments(blocks: list[dict[str, Any]]) -> str:
    """
    Renderiza los 5 segmentos de la barra de progreso por bloques.

    Args:
        blocks (list[dict[str, Any]]): Metadatos de bloques.

    Returns:
        str: HTML de los segmentos.
    """
    segments = [
        '<div class="seg" data-block="%d"><div class="seg-fill"></div></div>' % b["block"]
        for b in blocks
    ]
    return "\n".join(segments)


def build_deck(output_dir: Path | str | None = None) -> Path:
    """
    Compila la presentación HTML autocontenida de la charla.

    Args:
        output_dir (Path | str | None): Directorio destino; por defecto `dist/`
            dentro de la carpeta de la charla.

    Returns:
        Path: Ruta del `index.html` generado.

    Raises:
        FileNotFoundError: Si falta `chart.umd.min.js` compartido.
    """
    out_dir = Path(output_dir) if output_dir is not None else BASE_DIR / "dist"
    out_dir.mkdir(parents=True, exist_ok=True)

    styles = _load_module(BASE_DIR / "front" / "styles.py", "sdd_styles")
    notes_module = _load_module(BASE_DIR / "front" / "notes.py", "sdd_notes")

    slides = _merge_slides()
    blocks = _compute_blocks(slides)

    notes: list[dict[str, str]] = []
    notes_lookup = notes_module.NOTES
    for slide in slides:
        note = notes_lookup.get(slide["id"], {})
        notes.append(
            {
                "time": note.get("time", ""),
                "body": note.get("body", "<p>Sin notas para esta diapositiva.</p>"),
            }
        )

    if len(notes) != len(slides):
        raise ValueError("La cantidad de notas no coincide con las diapositivas")

    sections = "\n".join(
        _render_section(i + 1, slide) for i, slide in enumerate(slides)
    )
    segments = _render_segments(blocks)

    if not SHARED_CHARTJS_PATH.is_file():
        raise FileNotFoundError(f"Falta Chart.js compartido: {SHARED_CHARTJS_PATH}")
    chartjs = _script_safe(SHARED_CHARTJS_PATH.read_text(encoding="utf-8"))

    chart_specs = _load_module(BASE_DIR / "front" / "slides_p2.py", "sdd_slides_p2")
    meta = {"total": len(slides), "blocks": blocks}

    html = styles.HTML_TEMPLATE
    replacements = {
        "__TITLE__": TITLE,
        "__DESCRIPTION__": slides[0].get("sub", TITLE),
        "__CSS__": styles.CSS,
        "__SECTIONS__": sections,
        "__SEGS__": segments,
        "__CHART_SPECS__": _dump_json(chart_specs.CHART_SPECS),
        "__CHARTJS__": chartjs,
        "__META__": _dump_json(meta),
        "__NOTES__": _dump_json(notes),
        "__ENGINE__": styles.ENGINE_JS,
    }
    for token, value in replacements.items():
        html = html.replace(token, value)

    leftover = [token for token in replacements if token in html]
    if leftover:
        raise ValueError(f"Tokens sin sustituir en la plantilla: {leftover}")

    index_path = out_dir / "index.html"
    index_path.write_text(html, encoding="utf-8")
    (out_dir / "presentacion.html").write_text(html, encoding="utf-8")
    return index_path


def main() -> int:
    """
    Punto de entrada CLI: `python back/build_deck.py [--output-dir RUTA]`.

    Returns:
        int: 0 en caso de éxito.
    """
    parser = argparse.ArgumentParser(
        description="Compila la charla 2026-sdd-proyectos-reales (python-deck)."
    )
    parser.add_argument(
        "--output-dir",
        default=str(BASE_DIR / "dist"),
        help="Directorio destino de index.html y presentacion.html",
    )
    args = parser.parse_args()
    result = build_deck(args.output_dir)
    print(f"[OK] Deck compilado: {result}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
