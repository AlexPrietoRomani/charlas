# Plantilla `python-deck` para nuevas charlas

Esta carpeta (`talks/_template_python_deck/`) es la base oficial para crear charlas con el motor **`python-deck`**: un HTML single-file autocontenido con tema oscuro técnico, **Chart.js offline** compartido desde `shared/python_deck/assets/chart.umd.min.js`, navegación por teclado y drawer de notas del orador `[N]`.

> Los directorios que comienzan con `_` son ignorados automáticamente por `discover_talks()` y por el Hub.

---

## Estructura de la plantilla

- `talk.json`: metadatos de la charla validados por `shared/manifest.py`.
- `cover.svg`: portada ligera por defecto (1200x675). Puedes reemplazarla por un `.png` o editar el `.svg`.
- `back/build_deck.py`: generador del deck en Python (`build_deck(output_dir)` + CLI `--output-dir`).
- `README.md`: esta guía rápida.

---

## Cómo crear una nueva charla desde esta plantilla

1. **Copia la carpeta** asignando un nombre en `kebab-case` (ej. `2027-mi-nueva-charla`):
   ```bash
   cp -r talks/_template_python_deck talks/2027-mi-nueva-charla
   ```
2. **Edita `talks/2027-mi-nueva-charla/talk.json`**:
   - Cambia `"slug"` para que **coincida exactamente** con el nombre de la carpeta (`"2027-mi-nueva-charla"`).
   - Actualiza `"title"`, `"subtitle"`, `"event"`, `"date"` (`YYYY-MM-DD`), `"tags"`, `"slides_count"` y `"duration_min"`.
   - Cambia `"draft": false` (o elimina la clave `"draft"`) cuando quieras publicarla en el Hub.
3. **Personaliza tus diapositivas, notas y datos en `back/build_deck.py`**:
   - `_build_sample_data()`: reemplaza el dataset de ejemplo o carga tus CSV/JSON desde `data/`.
   - `_build_speaker_notes()`: redacta el guion por número de diapositiva (visible al presionar `N`).
   - `_build_slides_html()`: agrega tus `<section class="slide" data-index="...">` y actualiza el conteo total de diapositivas.
   - Si agregas más gráficos Chart.js, inicialízalos dentro de `initSlideVisuals(idx)` en el script del deck.
4. **Actualiza la portada**: reemplaza `cover.svg` o apunta `"cover"` en `talk.json` a una imagen dentro de la carpeta de la charla.

---

## Compilación y controles de presentación

- **Compilar solo esta charla hacia `_site/`:**
  ```bash
  python talks/2027-mi-nueva-charla/back/build_deck.py --output-dir _site/2027-mi-nueva-charla
  ```
- **Compilar todo el repositorio (Hub + todas las charlas):**
  ```bash
  python scripts/build_all.py
  ```
- **Atajos de teclado en el navegador:**
  - `→` / `Espacio` / `PageDown`: diapositiva siguiente.
  - `←` / `PageUp`: diapositiva anterior.
  - `N`: abrir o cerrar el drawer de **Notas del Orador**.
  - `F`: activar o salir de **Pantalla completa**.
  - `Home` / `End`: ir a la primera o última diapositiva.
