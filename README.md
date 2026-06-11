# E-commerce Operations Insights 📊

Este proyecto consiste en un análisis integral de operaciones de e-commerce y supply chain, abarcando desde la exploración inicial de los datos hasta la creación de una base de datos relacional normalizada y la generación de visualizaciones estratégicas.

## ⚠️ Nota sobre el Dataset
Es fundamental destacar que el dataset utilizado es **sintético y diseñado exclusivamente con fines docentes**. Durante la fase de exploración (EDA), se identificaron diversas **inconsistencias lógicas** propias de su naturaleza generada artificialmente, tales como:
*   Ambigüedades en la relación entre coordenadas geográficas (latitud/longitud) y entidades organizativas (departamentos).
*   Patrones de datos que no siempre reflejan la complejidad o el comportamiento orgánico de un mercado real.

A pesar de estas limitaciones, el proyecto se ha desarrollado siguiendo los estándares de la industria para el tratamiento de datos reales, priorizando la integridad estructural y la normalización.

---

## 🚀 Fases del Proyecto

### 1. Análisis Exploratorio de Datos (EDA)
Se realizó una limpieza profunda y un análisis estadístico para entender la distribución de las ventas, los riesgos de logística y el comportamiento de los clientes. 
*   **Archivos:** `notebooks/01_eda.ipynb`, `src/exploration.py`

### 2. Proceso ETL (Extract, Transform, Load)
Transformación de los datos brutos (`files/raw`) en conjuntos de datos limpios y preparados para su ingesta. Se manejaron valores nulos, formatos de fecha y limpieza de strings.
*   **Archivos:** `notebooks/02_etl.ipynb`, `src/transform.py`

### 3. Construcción de Base de Datos (SQLAlchemy & MySQL)
Se diseñó e implementó una base de datos relacional robusta en **MySQL** utilizando **SQLAlchemy**. Se aplicó una estrategia de **normalización (v2)** para resolver las ambigüedades geoespaciales detectadas, estructurando la información en las siguientes tablas:
*   `locations`, `departments`, `categories`, `products`, `customers`, `orders`, `order_items`.
*   **Archivos:** `src/db_builder.py`, `notebooks/03_ingester.ipynb`

### 4. Visualizaciones e Insights
Generación de dashboards y gráficos para la toma de decisiones, centrados en rentabilidad, eficiencia logística y comportamiento del consumidor.
*   **Archivos:** `notebooks/04_visualizations.ipynb`

---

## 🛠️ Tecnologías Utilizadas
*   **Lenguaje:** Python 3.x
*   **Análisis de Datos:** Pandas, Numpy
*   **Base de Datos:** MySQL, SQLAlchemy, PyMySQL
*   **Visualización:** Matplotlib, Seaborn
*   **Entorno:** Jupyter Notebooks

---

## 📂 Estructura del Repositorio
```text
├── documentacion_propuesta/  # Documentación de diseño y normalización
├── files/                    # Datos raw y procesados (CSV)
├── notebooks/                # Notebooks secuenciales del proyecto (01-04)
├── queries/                  # Scripts SQL para consultas y validaciones
└── src/                      # Código modular (DB Builder, Transform, EDA)
```

---
*Proyecto desarrollado como ejercicio de ingeniería de datos y análisis operativo.*
