# Ejecución — Data_Wizard

## Requisitos previos

- Node.js >= 22.12.0
- pnpm

## Arranque local

```bash
pnpm install
pnpm astro dev --port 4321
```

Abrir `http://localhost:4321`.

## Build para producción

```bash
pnpm astro build
```

El resultado queda en `dist/`.

## Despliegue en GitHub Pages

1. Push a `main`/`master`
2. En GitHub: Settings → Pages → Source: GitHub Actions
3. O configurar build manual con `pnpm astro build` y servir `dist/`

## Regenerar datos climáticos

```bash
python obtener_clima.py --lat -30.03 --lon -70.71 --inicio 2025-06-01 --fin 2025-08-14 --salida data/clima_valle_elqui.csv
```

Requiere internet para Open-Meteo API. Sin `--sin-escenario` inyecta la noche crítica.

## Estructura de slides

19 diapositivas, ~30 min de presentación:

1. Apertura (título)
2. El lugar (mapa Leaflet)
3. El gancho ("2 AM")
4. El concepto (falsa alarma vs. amenaza)
5. Los 4 desenlaces (matriz 2×2 vacía)
6. Ponle precio (matriz con costos)
7. El dial (slider interactivo)
8. La trampa (96% + cuadrícula)
9. Los datos (timeline)
10. 18 de julio (clímax)
11. La cuenta (US$ 56.160)
12. La decisión (matriz llena)
13. El patrón (universalidad)
14. Cierre (frase para llevar)
15-19. Extras (storytelling, contramedidas, sidebar, KPI)
