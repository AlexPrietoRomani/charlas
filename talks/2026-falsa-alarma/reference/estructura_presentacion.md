# Estructura y Secuencia de la Presentación: "Falsa Alarma o Amenaza Real"

Este documento detalla la estructura paso a paso de las diapositivas de la presentación interactiva en Astro, la narrativa para cada una, las referencias formales de pie de página y las justificaciones analíticas basadas en datos reales del cultivo de fresas en el Valle del Elqui.

---

## Estilo Visual y Diseño
*   **Color Palette:** Fondo claro (`#FFFFFF`) con textos y líneas en negro puro (`#000000`) para simular planos técnicos. Diapositivas dramáticas de tensión en modo oscuro (`#050505`).
*   **Bordes:** Rígidos y afilados (`border-radius: 0 !important`), líneas finas y rejillas estructuradas.
*   **Referencias:** Cada diapositiva contiene referencias formales al pie de página (`<footer>`) alineadas a la izquierda en tamaño pequeño (`0.7rem`) para soporte técnico y rigor gerencial.

---

## Secuencia de Diapositivas

### 1. Portada (Apertura)
*   **Título:** Falsa alarma o amenaza real
*   **Subtítulo:** El dilema oculto detrás de cada dato
*   **Estampas (Scattered):** 
    *   `MODEL ACCURACY: 96.0%`
    *   `VALLE DEL ELQUI · CHILE`
    *   `TRADE-OFF ANALYSIS`
*   **Narrativa:** Presentar el dilema central: decidir con datos implica equivocarse, pero no todos los errores cuestan igual.
*   **Referencia:** *Caso de estudio: Predicción de heladas en cultivos de fresa, Valle del Elqui, Coquimbo, Chile (2025).*

### 2. Storytelling en Datos (Fundamento Teórico)
*   **Título:** Los datos no se explican solos. Necesitan una historia.
*   **Estructura Asimétrica:** 
    *   *Izquierda:* El puente entre el análisis y la acción.
    *   *Derecha:* Marco SUCCESs (*Made to Stick*) en caja de bordes rígidos.
*   **Contenido:**
    *   **Data Analyst:** Pasa de creador de reportes estáticos a socio estratégico.
    *   **Data Scientist:** Conecta la optimización matemática con el costo real del negocio.
*   **Referencia:** *Nussbaumer Knaflic, C. (2015). Storytelling with Data: A Data Visualization Guide for Business Professionals. Wiley. / Heath, C., & Heath, D. (2007). Made to Stick. Random House.*

### 3. El Proceso del Storytelling (Los 6 Pasos)
*   **Título:** El Proceso: De datos crudos a una narrativa con impacto
*   **Estructura:** Rejilla de 3 columnas con números gigantes (01 al 06) interactivos que revelan tips al hacer clic.
*   **Pasos:** Contexto, Visualización, Ruido, Atención, Diseño, Historia.
*   **Referencia:** *Metodología adaptada de Cole Nussbaumer Knaflic - Storytelling with Data.*

### 4. El Flujo de Trabajo en Acción
*   **Título:** ¿Cómo cambia la toma de decisiones según el enfoque?
*   **Estructura:** Dos columnas con borde divisorio central negro grueso.
    *   *Columna Izquierda (Rojo/Gris):* Flujo tradicional inercial basado en accuracy (96%).
    *   *Columna Derecha (Cian/Blanco):* Flujo narrativo centrado en asimetría y salvaguardas.
*   **Referencia:** *Análisis comparativo de procesos de Business Intelligence en la toma de decisiones agrícolas (2025).*

### 5. El Escenario (El Lugar y la Planta)
*   **Título:** El escenario: Valle del Elqui y el cultivo de fresas
*   **Estructura:** 50:50 Asimétrica.
    *   *Izquierda:* Mapa en color de Leaflet con downscaling de Open-Meteo.
    *   *Derecha:* Fotografía a color `assets/strawberry_flower_frost_damage.png` con descripción del daño celular bajo -0.5 °C.
*   **Referencia:** *Históricos climatológicos coordinados vía API Open-Meteo (downscaling NOAA GFS y ECMWF) / Fisiología de la floración de Fragaria ananassa.*

### 6. El Gancho (La Decisión)
*   **Título:** Son las 2 de la madrugada.
*   **Modo:** Oscuro dramático (`slide dark`).
*   **Contenido:** Tensión psicológica del operador. Agua, energía y mano de obra en juego.
*   **Referencia:** *Manual de operaciones: Control activo de heladas mediante micro-aspersores.*

### 7. Dos formas de equivocarse (Concepto)
*   **Título:** No hay una sola forma de equivocarse. Hay dos —y son opuestas.
*   **Estructura:** Dos tarjetas con bordes rígidos y detalles a color.
    *   *Falsa Alarma (FP):* Operación innecesaria. Molesto, pero barato.
    *   *Amenaza No Detectada (FN):* Helada catastrófica. Silencioso, pero costoso.
*   **Referencia:** *Neyman, J., & Pearson, E. S. (1928). On the Use and Interpretation of Certain Test Criteria for Purposes of Statistical Inference. Biometrika.*

### 8. Cuatro desenlaces posibles (Matriz Vacía)
*   **Título:** Cuatro desenlaces posibles
*   **Estructura:** Matriz de confusión interactiva. Al hacer clic en cada celda, muestra el significado de negocio en un panel.
*   **Referencia:** *Matriz de confusión estándar aplicada a clasificación binaria de riesgos climáticos.*

### 9. Valorización del Error (Ponle Precio)
*   **Título:** No cuentes errores. Ponles precio.
*   **Estructura:** Matriz con precios inyectados. FP = US$ 340/noche; FN = US$ 56,160/sector. La celda de FN está marcada con un borde negro grueso de advertencia.
*   **Referencia:** *Estructura de costos operativos y tasación de pérdida por sector en floración (Datos de Valle del Elqui, 2025).*

### 10. El Dial de Decisión (El Umbral)
*   **Título:** El dial que nadie ve: el umbral
*   **Estructura:**
    *   *Izquierda:* Slider interactivo de umbral (°C).
    *   *Derecha:* Falsas alarmas, capturas y amenazas resultantes.
*   **Referencia:** *Teoría de detección de señales (SDT) y calibración de umbrales óptimos de decisión.*

### 11. La Trampa de la Exactitud (La Métrica)
*   **Título:** “El modelo acierta el 96% de las noches.”
*   **Estructura:**
    *   *Izquierda:* Número gigante `96%` en negro.
    *   *Derecha:* Rejilla de 75 puntos (noches) con el único FN destacado en rojo.
*   **Referencia:** *Métricas de evaluación: Limitaciones del Accuracy en datasets altamente desbalanceados.*

### 12. Línea de Tiempo (Los Datos)
*   **Título:** Lo que dijeron los modelos… y lo que pasó
*   **Estructura:** Gráfico lineal técnico interactivo (Chart.js) de 75 noches. Destaca la desviación crítica de 5.0 °C el 18 de julio.
*   **Referencia:** *Serie de tiempo climatológica: Temporada de invierno 2025 (Valle del Elqui).*

### 13. El Clímax (18 de Julio)
*   **Título:** Una decisión completamente razonable… y equivocada
*   **Modo:** Oscuro dramático (`slide dark`).
*   **Estructura:** Flujo de decisión lineal con flechas y cajas de lectura técnica.
*   **Referencia:** *Informe técnico de helada crítica del 18-Jul-2025.*

### 14. La Cuenta (El Daño)
*   **Título:** La cuenta del negocio
*   **Modo:** Oscuro dramático (`slide dark`).
*   **Estructura:**
    *   *Izquierda:* Gráfico de barras (Chart.js) de pérdidas reales en Sector D.
    *   *Derecha:* Pérdida total de `US$ 56.160` y la comparativa asimétrica de 82×.
*   **Referencia:** *Reporte de pérdidas y rendimientos por sector, Agrícola Valle del Elqui (Julio 2025).*

### 15. Salvaguardas (Contramedidas)
*   **Título:** No basta con detectar el error. Hay que diseñar contramedidas.
*   **Estructura:** 50:50 Asimétrica.
    *   *Izquierda:* 4 tarjetas de contramedidas con simulación económica.
    *   *Derecha:* Fotografía `assets/strawberry_field_sprinklers_night.png` a color mostrando control por micro-aspersores.
*   **Contramedidas:**
    *   1. **Umbral Conservador (3.5 °C):** Captura todas las heladas. Costo extra: US$ 4,420. **Ahorro neto: US$ 52,420**.
    *   2. **Ensemble de Modelos:** Integrar NOAA GFS, ECMWF y local.
    *   3. **Sensor local IoT:** Gatillo de contingencia física por debajo de 0 °C (US$ 50).
    *   4. **Escalación humana:** Decisión experta a las 2 AM en zona gris (1 °C a 3 °C).
*   **Referencia:** *Diseño de sistemas redundantes para la mitigación del riesgo en agricultura de precisión.*

### 16. Storytelling → Predicción
*   **Título:** ¿Cómo el storytelling ayuda a predecir?
*   **Estructura:** Línea de flujo interactiva de 4 pasos (Historia, Impacto, Negociación, Calibración).
*   **Referencia:** *Cole Nussbaumer Knaflic - Storytelling with Data.*

### 17. La Matriz Resuelta (La Decisión)
*   **Título:** El modelo no decide. Decide quien entiende el negocio.
*   **Estructura:** Matriz final con el conteo de la temporada y el umbral calibrado para mitigar pérdidas catastróficas.
*   **Referencia:** *Calibración de matrices de costo-beneficio para la optimización de activos agrícolas.*

### 18. Universalidad (El Patrón)
*   **Título:** El mismo dilema, en todas partes
*   **Estructura:** 3 columnas (Test médico, Filtro de spam, Seguridad/Fraude bancario) con bordes finos.
*   **Referencia:** *Clasificación binaria asimétrica en ingeniería de software, medicina y finanzas.*

### 19. Cierre (Mensaje Clave)
*   **Título:** Decidir con datos no es acertar siempre. Es elegir con qué error puedes vivir.
*   **Modo:** Oscuro dramático (`slide dark`).
*   **Estructura:** Mensaje centrado con firma del presentador.
*   **Referencia:** *Mensaje de cierre. Caso de estudio Data Wizard (2026).*
