// @ts-check
import { defineConfig } from 'astro/config';

// Resuelve la ruta base desde variable de entorno para desplegar en subrutas configurables
const astroBase = process.env.ASTRO_BASE || '/charlas/2026-falsa-alarma';

// https://astro.build/config
export default defineConfig({
  site: 'https://alexprietoromani.github.io',
  base: astroBase,
  output: 'static',
  build: {
    inlineStylesheets: 'always',
  },
});
