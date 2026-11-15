# Plantilla `static` / `custom` para charlas con estilo libre

Esta carpeta (`talks/_template_static/`) sirve para crear charlas con cualquier estética o herramienta distinta a `python-deck`: HTML/CSS artesanal, Reveal.js, Tailwind CSS, Quarto, Slidev, Marp o exportaciones estáticas de terceros.

Incluye un deck mínimo autocontenido de **3 diapositivas en tema claro** (`index.html`) para demostrar visualmente que cada charla conserva su identidad visual sin interferir con el Hub ni con otras ponencias.

> Los directorios que comienzan con `_` son ignorados automáticamente por `discover_talks()`.

---

## Opción 1 — `"engine": "static"` (HTML, Reveal.js, Tailwind ya exportado)

Úsala cuando tu charla ya tiene un `index.html` (y opcionalmente carpetas `assets/`, `css/`, `js/`) listos para servir tal cual.

1. Copia la plantilla a una nueva carpeta `kebab-case`:
   ```bash
   cp -r talks/_template_static talks/2027-mi-charla-libre
   ```
2. Edita `talks/2027-mi-charla-libre/talk.json`:
   - Actualiza `"slug": "2027-mi-charla-libre"` (debe coincidir con la carpeta).
   - Mantén `"engine": "static"` y `"entry": "index.html"` (o la ruta relativa de entrada).
   - Cambia `"draft": false` (o elimina `"draft"`) para mostrarla en el Hub.
3. Reemplaza `index.html`, `cover.svg` y agrega tus activos locales dentro de la misma carpeta usando rutas relativas (`./assets/...`).

Durante `python scripts/build_all.py`, el orquestador copiará todo el contenido de la carpeta hacia `_site/<slug>/` y verificará que `entry` exista.

---

## Opción 2 — `"engine": "custom"` (Quarto, Slidev, Marp u otro generador)

Úsala cuando tu charla requiere un paso previo de compilación antes de copiar el resultado a `_site/<slug>/`.

1. Edita `talk.json` cambiando `"engine"` a `"custom"` y agregando el bloque obligatorio `"build"`:
   ```json
   {
     "slug": "2027-mi-charla-quarto",
     "title": "Storytelling con Quarto",
     "event": "Data Meetup 2027",
     "date": "2027-03-10",
     "engine": "custom",
     "entry": "index.html",
     "cover": "cover.svg",
     "draft": false,
     "tags": ["Quarto", "Storytelling"],
     "build": {
       "cmd": "quarto render deck.qmd --output-dir _build",
       "out_dir": "_build"
     }
   }
   ```
2. `scripts/build_all.py` ejecutará `build.cmd` dentro de `talks/<slug>/` y copiará `build.out_dir` hacia `_site/<slug>/`.

---

## Controles incluidos en el `index.html` base

- `←` / `→` o `Espacio`: retroceder o avanzar entre las 3 diapositivas.
- Botones inferiores `← Anterior` y `Siguiente →`.
- `Home` / `End`: saltar al inicio o cierre de la presentación.
