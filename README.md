# Explorador ESOLMET

Este proyecto es una aplicación web interactiva desarrollada con Shiny for Python. Permite visualizar, analizar y descargar datos meteorológicos y solarimétricos de la estación ESOLMET-IER, abarcando diferentes años y variables clave.

Puedes visitar la Web App con este enlace:
[https://jramonha.shinyapps.io/explorador-esolmet/](https://jramonha.shinyapps.io/explorador-esolmet/)


## Objetivo

El objetivo principal de este proyecto es proporcionar una herramienta accesible y eficiente para explorar los datos meteorológicos y solarimétricos de ESOLMET-IER. La aplicación está diseñada para facilitar el análisis de tendencias anuales y mensuales, así como el acceso a los datos en un formato descargable.


## Proceso de limpieza de datos

Los datos crudos de ESOLMET son procesados en seis pasos clave para asegurar su consistencia y preparación para análisis:

1. **Carga y Conversión**:
   - Los archivos `.csv` se leen con `pandas`, convirtiendo valores no numéricos en `NaN`.

2. **Renombrado de columnas**:
   - Las columnas reciben nombres más claros y descriptivos, como `'I_glo_Avg'` → `'Ib'` (radiación directa).

3. **Eliminación de columnas urrelevantes**:
   - Columnas como `'RECORD'`, `'I_dir_Avg'` y `'I_uv_Avg'` se eliminan si están presentes.

4. **Exportación de datos limpios**:
   - Los datos procesados se guardan en formato `.parquet` para un manejo más eficiente.


## Estructura del proyecto

### Archivos principales

1. **`app.py`**:
   - Contiene la lógica principal de la aplicación web, incluidas las definiciones de la interfaz de usuario y el servidor.
   - Utiliza librerías como `pandas` y `plotly` para el manejo y la visualización de datos.

2. **`funciones.py`**:
   - Proporciona utilidades para cargar datos según el año y realizar cálculos específicos.

3. **`cleaning.ipynb`**:
   - Implementa el proceso de limpieza y preprocesamiento de los datos antes de cargarlos en la aplicación.

4. **`index.qmd`**:
   - Diapositivas sobre la presentación del proyecto.


## Funcionalidades

La aplicación web incluye lo siguiente:

1. **Visualización anual y mensual**:
   - Gráficos interactivos que muestran las tendencias de variables meteorológicas a lo largo del tiempo.
   - Resúmenes mensuales que incluyen medias, máximos, mínimos y desviaciones estándar.

2. **Selección de datos personalizada**:
   - Filtros por año, rango de fechas y variable meteorológica.

3. **Exploración de datos**:
   - Vista tabular de los datos filtrados.

4. **Descarga de datos**:
   - Posibilidad de descargar los datos seleccionados en formato CSV.


## Créditos
Los datos pertenecen a la estación [ESOLMET-IER](https://esolmet.ier.unam.mx/) y están destinados únicamente para fines educativos y de investigación.
