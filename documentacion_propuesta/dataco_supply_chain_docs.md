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
