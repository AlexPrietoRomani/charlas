# Charlas & Ponencias — Alex Prieto Romani

Repositorio multicharla centralizado (**`AlexPrietoRomani/charlas`**) que reúne mis ponencias técnicas bajo un **Hub selector estático** publicado en GitHub Pages:

> **URL pública final (tras renombrar el repositorio a `charlas`):** [`https://alexprietoromani.github.io/charlas/`](https://alexprietoromani.github.io/charlas/)

Cada charla vive autocontenida dentro de `talks/<slug>/`, declara sus metadatos en un manifiesto `talk.json` y conserva intacta su estética y tecnología propia (`python-deck`, `astro`, `static` o `custom`), sin interferir con el Hub ni con otras ponencias.

---

## Catálogo actual de charlas

| Slug | Título | Evento | Fecha | Motor | Diapositivas | Origen / Notas |
|---|---|---|---|---|---|---|
| `2026-forecasting-ia` | ¿Puede la IA predecir el futuro? Casos de forecasting real | Iquitos Data Fest 2026 | 2026-10-05 | `python-deck` | 30 | Deck HTML single-file + Chart.js offline (SENAMHI Iquitos + Café Jaén) |
| `2026-falsa-alarma` | Falsa alarma o amenaza real: el dilema oculto detrás de cada dato | Storytelling con Datos · Valle del Elqui | 2026-07-23 | `astro` | 21 | Migrada desde `Data_Wizard` (Astro estático con `--base` dinámico) |

---

## Estructura del repositorio

```text
charlas/
├── .github/workflows/deploy.yml   # CI/CD: build multicharla + pytest + GitHub Pages
├── hub/                           # Hub selector personal (HTML/CSS/JS + build_hub.py)
├── shared/
│   ├── manifest.py                # Descubrimiento y validación estricta de talk.json
│   └── python_deck/               # Assets compartidos (Chart.js offline, branding, styles)
├── scripts/
│   └── build_all.py               # Orquestador maestro multi-motor (_site/)
├── talks/
│   ├── _template_python_deck/     # Plantilla base para charlas con motor python-deck
│   ├── _template_static/          # Plantilla base para charlas static / custom
│   ├── 2026-forecasting-ia/       # Charla 1 (python-deck)
│   └── 2026-falsa-alarma/         # Charla 2 (astro)
├── tests/
│   ├── unit/                      # Pruebas unitarias de manifiestos, estructura y CI
│   ├── integration/               # Pruebas de compilación multi-motor con build_all.py
│   └── e2e/                       # Suite Playwright Chromium sobre _site/
├── docs/                          # Especificación técnica (architecture, db, ejecucion)
├── pyproject.toml                 # Configuración de paquete y pytest
└── requirements.txt               # Dependencias Python ligeras de build y testing
```

---

## Cómo levantar el Hub + charlas localmente

### 1. Requisitos e instalación

- **Python** `3.11+`
- **Node.js** `22+` y **pnpm** `10+` (para charlas con motor `astro`)

```bash
python -m pip install -r requirements.txt
pnpm --dir talks/2026-falsa-alarma install --frozen-lockfile
```

*(Opcional para ejecutar pruebas E2E con Playwright: `python -m playwright install chromium`.)*

### 2. Compilar todo el sitio y servir en local

```bash
python scripts/build_all.py --base-path /
python -m http.server -d _site 8000
```

Abre en el navegador:
- **Hub selector:** `http://localhost:8000/`
- **Charla `2026-forecasting-ia`:** `http://localhost:8000/2026-forecasting-ia/`
- **Charla `2026-falsa-alarma`:** `http://localhost:8000/2026-falsa-alarma/`

*(Para simular exactamente el subpath de GitHub Pages en local, compila con `--base-path /charlas`.)*

### 3. Ejecutar la suite de pruebas

```bash
python -m pytest -v
```

---

## Cómo agregar una nueva charla

El orquestador `scripts/build_all.py` descubre automáticamente cualquier subcarpeta dentro de `talks/` que contenga un `talk.json` válido (las carpetas con prefijo `_` como `_template_*` o con `"draft": true` se omiten en producción).

### Opción A — Mismo estilo (`python-deck`)

Ideal para decks técnicos single-file con Chart.js offline, atajos de teclado y notas del orador (`[N]`):

1. Copia la plantilla base usando un slug en `kebab-case`:
   ```bash
   cp -r talks/_template_python_deck talks/2027-mi-nueva-charla
   ```
2. Edita `talks/2027-mi-nueva-charla/talk.json` (actualiza `"slug"`, `"title"`, `"event"`, `"date"`, `"tags"`, `"slides_count"`, `"duration_min"` y deja `"engine": "python-deck"` con `"draft": false` cuando esté lista).
3. Personaliza las diapositivas, notas y datos dentro de `talks/2027-mi-nueva-charla/back/build_deck.py`.

### Opción B — Estilo diferente (`static` o `custom`: HTML puro / Reveal.js / Quarto / Slidev)

Ideal cuando quieres total libertad visual o usas un generador externo sin tocar el resto del repositorio:

1. Copia la plantilla estática:
   ```bash
   cp -r talks/_template_static talks/2027-mi-charla-libre
   ```
2. En `talks/2027-mi-charla-libre/talk.json`:
   - Usa **`"engine": "static"`** si ya tienes HTML/CSS/JS o Reveal.js listo (`entry: "index.html"`): `build_all.py` copiará la carpeta directamente a `_site/<slug>/`.
   - Usa **`"engine": "custom"`** si necesitas compilar con Quarto, Slidev o Marp, añadiendo el bloque `"build"`:
     ```json
     "engine": "custom",
     "entry": "index.html",
     "build": {
       "cmd": "quarto render deck.qmd --output-dir _build",
       "out_dir": "_build"
     }
     ```

### Opción C — Subproyecto Astro (`astro`)

Ideal para presentaciones construidas como app estática Astro:

1. Crea tu subproyecto en `talks/2027-mi-charla-astro/` con `"engine": "astro"` y `"entry": "index.html"` en `talk.json`.
2. Configura `base` de forma dinámica en `astro.config.mjs` para soportar tanto `/` local como `/charlas/<slug>` en GitHub Pages:
   ```javascript
   const astroBase = process.env.ASTRO_BASE || '/charlas/2027-mi-charla-astro';
   export default defineConfig({
     site: 'https://alexprietoromani.github.io',
     base: astroBase,
     output: 'static',
   });
   ```
3. `scripts/build_all.py` ejecutará `pnpm --dir talks/<slug> install --frozen-lockfile` (si falta `node_modules/`) y `pnpm --dir talks/<slug> build --base <talk_base>` propagando `ASTRO_BASE`.

---

## Despliegue automático y renombrado del repositorio

### CI/CD con GitHub Pages

Cada `push` a la rama `master` dispara [`.github/workflows/deploy.yml`](.github/workflows/deploy.yml), que:
1. Instala Python `3.11`, `pnpm` `10` y Node.js `22`.
2. Compila el Hub y todas las charlas activas con `python scripts/build_all.py --base-path /charlas`.
3. Ejecuta las pruebas `pytest tests/unit tests/integration -v`.
4. Publica `_site/` en GitHub Pages mediante `actions/upload-pages-artifact@v3` y `actions/deploy-pages@v4`.

### Renombrar el repositorio en GitHub a `charlas`

Para activar la URL definitiva `https://alexprietoromani.github.io/charlas/`:

1. En GitHub, ve a **Settings → General → Repository name**, cámbialo de `charla_forecasting` a `charlas` y haz clic en **Rename**.
2. En **Settings → Pages**, verifica que **Source** esté configurado en **GitHub Actions**.
3. Actualiza el remoto en tu copia local:
   ```bash
   git remote set-url origin https://github.com/AlexPrietoRomani/charlas.git
   git remote -v
   ```
