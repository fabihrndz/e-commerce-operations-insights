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
