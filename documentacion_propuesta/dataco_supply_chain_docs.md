# Documentación: dataco_supply_chain.csv

Este archivo contiene información detallada sobre las operaciones de la cadena de suministro, incluyendo ventas, entregas y datos de clientes.

## Columnas

| Columna | Descripción |
| :--- | :--- |
| **Type** | Tipo de transacción realizada (DEBIT, TRANSFER, CASH, PAYMENT). |
| **Days for shipping (real)** | Días reales que tomó el envío del producto. |
| **Days for shipment (scheduled)** | Días programados para la entrega del producto. |
| **Benefit per order** | Ganancia por cada pedido realizado. |
| **Sales per customer** | Ventas totales realizadas por cliente. |
| **Delivery Status** | Estado de la entrega (Advance shipping, Late delivery, Shipping canceled, Shipping on time). |
| **Late_delivery_risk** | Variable categórica: (1) si el envío se retrasó, (0) si no. |
| **Category Id** | Código de la categoría del producto. |
| **Category Name** | Nombre de la categoría del producto. |
| **Customer City** | Ciudad del cliente. |
| **Customer Country** | País del cliente. |
| **Customer Email** | Correo electrónico del cliente (enmascarado). |
| **Customer Fname** | Nombre del cliente. |
| **Customer Id** | ID único del cliente. |
| **Customer Lname** | Apellido del cliente. |
| **Customer Segment** | Segmento del cliente (Consumer, Corporate, Home Office). |
| **Customer State** | Estado/Provincia del cliente. |
| **Customer Zipcode** | Código postal del cliente. |
| **Department Id** | Código del departamento de la tienda. |
| **Department Name** | Nombre del departamento de la tienda. |
| **Latitude** | Latitud de la ubicación de la tienda. |
| **Longitude** | Longitud de la ubicación de la tienda. |
| **Market** | Mercado de destino (Africa, Europe, LATAM, Pacific Asia, USCA). |
| **Order City** | Ciudad de destino del pedido. |
| **Order Country** | País de destino del pedido. |
| **Order Customer Id** | Código de cliente asociado al pedido. |
| **order date (DateOrders)** | Fecha y hora en la que se realizó el pedido. |
| **Order Id** | Código único del pedido. |
| **Order Item Cardprod Id** | Código del producto generado a través del lector RFID. |
| **Order Item Discount** | Valor del descuento aplicado al artículo. |
| **Order Item Discount Rate** | Porcentaje de descuento aplicado. |
| **Order Item Id** | Código único del artículo del pedido. |
| **Order Item Product Price** | Precio del producto sin descuento. |
| **Order Item Profit Ratio** | Ratio de beneficio del artículo. |
| **Order Item Quantity** | Cantidad de productos por pedido. |
| **Sales** | Valor total de la venta. |
| **Order Item Total** | Monto total por artículo. |
| **Order Profit Per Order** | Beneficio total por pedido. |
| **Order Region** | Región del mundo donde se entrega el pedido. |
| **Order State** | Estado de la región de entrega. |
| **Order Status** | Estado del pedido (COMPLETE, PENDING, CLOSED, CANCELED, etc.). |
| **Order Zipcode** | Código postal de destino (si está disponible). |
| **Product Card Id** | Código del producto. |
| **Product Category Id** | Código de la categoría del producto. |
| **Product Description** | Descripción del producto. |
| **Product Image** | Enlace a la imagen del producto. |
| **Product Name** | Nombre del producto. |
| **Product Price** | Precio unitario del producto. |
| **Product Status** | Estado del stock (0: disponible, 1: no disponible). |
| **shipping date (DateOrders)** | Fecha y hora exacta del envío. |
| **Shipping Mode** | Modo de envío (Standard Class, First Class, Second Class, Same Day). |


Documentación del Análisis Exploratorio de Datos (EDA)
Proyecto: Análisis de Logística y Órdenes de Pedidos

Volumen del Dataset: 180,519 filas × 53 columnas

Fecha: 25 de mayo de 2026

Estado: Fase de Limpieza y Preparación de Datos

1. Resumen Ejecutivo
El objetivo de este análisis exploratorio es evaluar la calidad de las 53 columnas del conjunto de datos, identificar redundancias, corregir anomalías estructurales y reducir la dimensionalidad del dataset eliminando variables irrelevantes o altamente correlacionadas. Esto optimizará el rendimiento de los modelos predictivos o analíticos que se construyan en las fases posteriores.

2. Hallazgos Críticos y Diagnóstico por Columnas
A. Datos Sensibles / Sin Varianza (Eliminación Inmediata)
Product Status: Variable constante. Todas las categorías registran el valor 0. Aunque teóricamente debería ser binaria (0: Disponible, 1: No disponible), al no tener variabilidad no aporta información al modelo.

Customer Email & Contraseña: Columnas anonimizadas o enmascaradas con el valor genérico "xxx". Al no contener datos reales ni aportar valor analítico, se descartan por completo.

Product Description: Columna vacía o carente de información relevante.

B. Redundancias y Solapamiento Geográfico
Order Zipcode: Presenta un 80% de valores nulos. La información geográfica se puede recuperar y mapear con mayor precisión a través de otras variables de ubicación.

Market / Order State / Order Region: Existe una triple redundancia de escala geográfica. Order State es confuso al mezclar estados y países. Se determina que Order Region (23 regiones) aporta el mejor balance de granularidad, permitiendo la eliminación de Market y Order State.

Customer City vs Customer Status: Ambas columnas contienen la misma información (nombre de la ciudad vs. su abreviatura/código). Se unificará el criterio utilizando una sola de ellas.

C. Inconsistencias de Negocio y Calidad
Customer Country: Presenta únicamente 2 países (EE. UU. y Puerto Rico). Se decide conservar temporalmente para segmentaciones y filtros futuros.

Customer State: Registra 46 de los 50 estados de EE. UU. Sin embargo, se detectó una anomalía de entrada de datos donde los códigos postales 95758 y 91738 se guardaron erróneamente como estados. Ambos corresponden a California (CA) y requieren imputación.

Product Image: Contiene enlaces URL a las imágenes de los productos. No se observa una usabilidad analítica clara a futuro, por lo que queda bajo observación para su posible descarte.

3. Plan de Acción: Limpieza y Transformación (Pipeline de Datos)
Basado en el diagnóstico, se ejecutarán las siguientes acciones de ingeniería de características (Feature Engineering) antes de proceder al modelado:

📑 Cuadro de Eliminación de Columnas (Drop)
Se eliminarán un total de 9 columnas para reducir el ruido y el coste computacional:

Product Status

Customer Email

Contraseña

Order Zipcode

Product Description

Order State

Market

Order Region (Eliminar duplicadas/versiones redundantes)

🛠️ Modificaciones y Casteo de Tipos de Datos
Corrección de Errores de Registro (Customer State):

Reemplazar los valores string 95758 y 91738 por la abreviatura de estado CA.

Casteo de Tipos (Data Type Casting):

Customer Zipcode: Convertir de tipo numérico a String/Texto. Los códigos postales no deben tratarse como números ya que no se realizan operaciones aritméticas con ellos y se pueden perder los ceros a la izquierda.

Order Item Discount: Convertir estrictamente a tipo Float (decimal) para garantizar precisión en los cálculos financieros.

Estandarización Numérica (Redondeo):

Aplicar una función global (round_columns.py) a todas las variables cuantitativas con decimales para fijar su precisión a 2 decimales.

Tratamiento de Fechas y Tiempos (order date (DateOrders)):

Realizar una operación de Split (separación) para dividir la columna en dos variables independientes: Order_Date y Order_Time.

Convertir la fecha (actualmente en formato americano MM/DD/AAAA) al tipo estándar datetime64 para facilitar análisis de series temporales por meses (Enero - Diciembre).

Validación de Identificadores (Claves Foráneas):

Mantener las columnas Product Card Id y Product Category Id intactas. Se identifican como claves foráneas (FK) relacionales que conectan las entidades de Clientes, Pedidos y Productos en el modelo de datos.

4. Conclusiones Provisionales del EDA
El dataset cuenta con un volumen de registros robusto (más de 180k filas), lo cual es ideal para modelos de Machine Learning robustos. Sin embargo, sufre de una alta dimensionalidad artificial provocada por datos planos ("xxx", 0) y una severa redundancia en la información geográfica de los clientes y las entregas.

Una vez aplicado este plan de limpieza, el dataset pasará de 53 columnas a un conjunto mucho más limpio, magro y optimizado para la fase de modelado predictivo o creación de dashboards.