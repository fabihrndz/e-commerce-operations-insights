# Documentación: tokenized_access_logs.csv

Este archivo registra la actividad de navegación de los usuarios en la plataforma de e-commerce, incluyendo productos vistos y categorías visitadas.

## Columnas

| Columna | Descripción |
| :--- | :--- |
| **Product** | Nombre del producto que el usuario visualizó. |
| **Category** | Categoría a la que pertenece el producto visitado. |
| **Date** | Fecha y hora exacta del acceso (formato: `M/D/YYYY H:MM`). |
| **Month** | Mes del acceso (ej: Sep, Oct). |
| **Hour** | Hora del día en la que se registró el acceso (0-23). |
| **Department** | Departamento asociado al producto (ej: fitness, apparel, fan shop). |
| **ip** | Dirección IP del usuario (enmascarada/tokenizada). |
| **url** | Ruta completa de la URL visitada en la tienda. |


Documentación del Análisis Exploratorio de Datos (EDA)
Proyecto: Análisis de Tráfico Web y Campañas Estacionales (E-commerce)

Volumen del Dataset: 469,977 filas × 8 columnas

Fecha: 25 de mayo de 2026

Estado: Fase de Limpieza, De duplicación y Formateo

1. Resumen Ejecutivo
El objetivo de este análisis exploratorio es limpiar y estructurar un conjunto masivo de registros de acceso (logs) de una tienda virtual. El dataset captura el comportamiento de los usuarios durante un periodo crítico de ventas (campañas navideñas e invernales) a lo largo de varios años. El análisis se centra en eliminar redundancias temporales, corregir la dimensionalidad y preparar los datos para analizar patrones de comportamiento y embudos de conversión.

2. Hallazgos Críticos y Diagnóstico por Columnas
A. Integridad de los Datos (Duplicados)
Se detectaron 3,219 registros completamente duplicados. Al tratarse de registros de accesos web, los duplicados exactos suelen ser errores de doble petición del navegador o fallos en el sistema de registro de logs. Se procederá a su eliminación inmediata para evitar sesgos en las métricas de tráfico.

B. Análisis Temporal y Estacionalidad (Date, Month, Hour)
Date: La columna registra la fecha y hora exacta del acceso en formato americano (M/D/YYYY H:MM).

Horizonte Temporal: Los datos abarcan desde septiembre hasta enero, cubriendo consecutivamente los años 2015 a 2018. Esto confirma que el dataset está especializado en el comportamiento de los usuarios durante la campaña de Navidad y rebajas de invierno.

Redundancia Estructural: Las columnas Month y Hour contienen información complementaria que ya está embebida dentro de la estacionalidad de la columna principal Date, lo que genera una duplicidad innecesaria de dimensiones.

C. Análisis de Rutas y Navegación (url)
url: Contiene la ruta completa de la dirección web visitada dentro de la tienda. Se evalúa como una variable de baja usabilidad analítica en su estado actual, ya que las URLs crudas suelen aportar demasiado ruido (alta cardinalidad) y dispersión al modelo sin un procesamiento de texto avanzado previo.

3. Plan de Acción: Limpieza y Transformación (Pipeline de Datos)
Para dejar el dataset optimizado y listo para la fase analítica, se ejecutarán las siguientes transformaciones técnicas:

✂️ Eliminación de Ruido y Redundancias (Drop)
Deduplicación: Aplicar un filtrado drástico para eliminar las 3,219 filas repetidas, reduciendo el dataset a un total neto de 466,758 registros únicos.

Eliminación de Columnas (Month y Hour): Se descartan por completo para simplificar el dataset, ya que toda la información temporal se extraerá de manera nativa y controlada desde la columna de origen.

Descarte de url: Se elimina la columna de rutas completas para optimizar el coste computacional y reducir variables que no aportan valor predictivo directo.

🛠️ Modificaciones y Splitting de Columnas
Tratamiento Avanzado de Date (Operación Split):

Se aplicará una división estructural de la columna para separar de forma limpia la Fecha de la Hora en dos nuevas variables independientes.

Ambas columnas resultantes se castearán a sus tipos correspondientes (Date a formato fecha estándar y Time/Hour a formato de tiempo).

Ingeniería de Características Temporales (Propuesta):

Tras realizar el split, se aprovechará el formato de fecha para agrupar los datos por años (2015, 2016, 2017, 2018) y poder realizar análisis comparativos interanuales del rendimiento de las distintas campañas navideñas.

4. Conclusiones Provisionales del EDA
A pesar de tener un volumen muy elevado de registros (casi medio millón de filas), este dataset es sumamente compacto en cuanto a variables (solo 8 columnas). Tras la eliminación de los duplicados y de las columnas redundantes (Month, Hour, url), el dataset quedará significativamente optimizado.

El foco principal del proyecto tras esta limpieza será el análisis de series temporales, permitiendo identificar cuáles son los días de la semana, horas pico y meses específicos donde la campaña navideña registra la mayor actividad de los consumidores.
