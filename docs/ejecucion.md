# Guía de Ejecución — `charlas`

> **Proyecto:** `AlexPrietoRomani/charlas` · **Actualizado:** 2026-11-14
> **Tipo:** Sitio estático multicharla (Orquestador Python + Subproyectos Astro/Static) desplegado en GitHub Pages.

---

## 1. Requisitos previos

| Software | Versión mínima | Verificar con |
|---|---|---|
| Python | 3.11+ | `python --version` |
| Node.js | 22+ | `node --version` |
| pnpm | 10+ | `pnpm --version` |
| Git | 2.30+ | `git --version` |

---

## 2. Instalación de dependencias (local)

```powershell
# Dependencias Python (compilación de decks + tests)
python -m pip install -r requirements.txt
python -m pip install pytest playwright

# Si es la primera vez con Playwright en esta máquina:
python -m playwright install chromium
```

Para la charla Astro (`talks/2026-falsa-alarma/`):

```powershell
pnpm --dir talks/2026-falsa-alarma install --frozen-lockfile
```

---

## 3. Compilar y previsualizar todo el Hub + Charlas en local

```powershell
# 1. Compilar todas las charlas y el Hub en _site/
python scripts/build_all.py --base-path /

# 2. Servir localmente para probar rutas idénticas a producción
python -m http.server -d _site 8000
```

Luego abrir `http://localhost:8000/` en el navegador:
- Hub selector: `http://localhost:8000/`
- Charla 1: `http://localhost:8000/2026-forecasting-ia/`
- Charla 2: `http://localhost:8000/2026-falsa-alarma/`

> **Nota sobre `--base-path`:** En local con `http.server -d _site` se usa `--base-path /` (por defecto cuando se prueba local) o `--base-path /charlas` si se simula el subpath de GitHub Pages (`https://alexprietoromani.github.io/charlas/`). En CI (`deploy.yml`) se compila con `--base-path /charlas`.

---

## 4. Agregar una nueva charla

1. **Mismo estilo (Python Deck):** copia `talks/_template_python_deck/` a `talks/<nuevo-slug>/`, edita `talk.json`, `front/slides.py` y `front/notes.py`.
2. **Estilo diferente (HTML puro / Reveal.js / Quarto):** copia `talks/_template_static/` a `talks/<nuevo-slug>/`, coloca tu `index.html` y edita `talk.json` con `"engine": "static"` (o `"custom"` + `"build"`).
3. **Proyecto Astro independiente:** coloca el proyecto en `talks/<nuevo-slug>/` con `"engine": "astro"` en `talk.json` y configura `base` dinámico en `astro.config.mjs`.

---

## 5. Pruebas

```powershell
# Suite completa (unit + integración + E2E Playwright)
python -m pytest -q
```

---

## 6. Despliegue en GitHub Pages

Cada `push` a `master` ejecuta `.github/workflows/deploy.yml`, valida todos los `talk.json`, compila cada charla en `_site/<slug>/`, genera el Hub en `_site/index.html`, ejecuta `pytest` y despliega `_site/` a GitHub Pages.
