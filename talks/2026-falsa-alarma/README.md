# Ponencia — "Falsa alarma o amenaza real: el dilema oculto detrás de cada dato"

Presentación de datos interactiva (estilo PowerPoint en HTML) que explica la **asimetría entre tipos de error** —falso positivo vs. falso negativo— usando un caso real de heladas agrícolas en un campo de fresa del Norte Chico (Valle del Elqui, Chile). 

Toda la narrativa se apoya en datos reales e interactividad: la presentación lee archivos CSV y calcula en vivo la matriz de confusión, los costos económicos asociados y los gráficos correspondientes en el navegador.

---

## Estructura del Proyecto

```text
Data_Wizard/
├── presentacion.html                      # Deck interactivo (16 diapositivas con mapa y gráficos)
├── strawberry_flower_frost_damage.png     # Ilustración del daño biológico de la helada en la flor
├── data/                                  # Carpeta de datos del caso
│   ├── rendimiento_fresa.csv              # Rendimiento por sector y pérdidas en USD
│   └── clima_valle_elqui.csv              # Datos climáticos (mínimas observadas y pronóstico)
├── reference/                             # Material y especificaciones de la ponencia
│   ├── Brief.md                           # Resumen conceptual completo de la charla
│   └── estructura_presentacion.md          # Secuencia y estructura detallada de las diapositivas
└── articles/                              # Bibliografía y lecturas recomendadas
    ├── Storytelling-with-Data.pdf         # Libro de referencia (PDF)
    └── Storytelling-with-Data.md          # Conversión del libro a Markdown para consultas
```

---

## Fundamentos del Relato

### 1. El Marco Metodológico: Storytelling con Datos
La presentación adopta el proceso de 6 pasos de **Cole Nussbaumer Knaflic** (*Storytelling with Data*, disponible en O'Reilly) y el marco **SUCCESs** (*Made to Stick* de Chip & Dan Heath) para estructurar el mensaje:
*   **Simple:** Mensaje nuclear en lugar de una saturación de métricas irrelevantes.
*   **Unexpected (Inesperado):** Revelar cómo un modelo con 96% de exactitud puede llevar a la ruina al negocio.
*   **Concrete (Concreto):** Traducir los falsos negativos a dólares reales (USD 56,160 perdidos).
*   **Credible (Creíble):** Datos climáticos procedentes de **Open-Meteo** (obtenidos mediante downscaling local de los modelos GFS de NOAA y ECMWF de Europa).
*   **Emotional (Emocional):** El operador del campo a las 2 AM teniendo que tomar una decisión con datos imperfectos.
*   **Stories (Historias):** El relato centrado en la noche crítica del 18 de julio y el daño físico real en las flores del Sector D.

---

## Cómo ver la Presentación

### Opción rápida (doble clic)
Abre `presentacion.html` directamente en cualquier navegador moderno. Si no hay conexión de servidor, la presentación cargará automáticamente datos de respaldo embebidos (fallbacks), por lo que funciona offline.

### Opción recomendada (carga los CSV de la carpeta `data/`)
Para poder modificar los CSV y ver los cambios reflejados en tiempo real en la presentación, sirve la carpeta con un servidor local:

```bash
# Iniciar un servidor local en el puerto 8000
python -m http.server 8000
```
Luego abre en tu navegador: [http://localhost:8000/presentacion.html](http://localhost:8000/presentacion.html)

---

## Ajuste de Parámetros
Los parámetros económicos y umbrales críticos se pueden calibrar directamente en las constantes al inicio del bloque `<script>` de `presentacion.html`:

*   `UMBRAL_ACTIVACION = 2.0` — Temperatura pronosticada a partir de la cual se activa la aspersión.
*   `UMBRAL_DANO = -0.5` — Temperatura observada por debajo de la cual se produce daño por helada radiativa en la flor.
*   `COSTO_NOCHE = 340` — Costo de operación (agua, energía, mano de obra) por noche protegida.

---

## Navegación
*   **→ / Barra Espaciadora / PageDown:** Siguiente diapositiva.
*   **← / PageUp:** Diapositiva anterior.
*   **F:** Alternar pantalla completa.
*   **Inicio / Fin:** Ir directamente a la primera o última diapositiva.
