# Propuesta de Normalización de Base de Datos - DataCo Supply Chain

Para transformar el archivo plano `dataco_supply_chain.csv` en un sistema de base de datos relacional profesional, se recomienda una arquitectura normalizada (3NF) que elimine la redundancia y garantice la integridad de los datos.

A continuación, se detalla la división en tablas sugerida:

## 1. Tabla: `customers` (Clientes)
Almacena la información demográfica y de contacto de los clientes.
*   **customer_id** (PK): Identificador único del cliente.
*   **first_name**: Nombre del cliente.
*   **last_name**: Apellido del cliente.
*   **segment**: Segmento del cliente (Consumer, Corporate, Home Office).
*   **street**: Dirección del cliente.
*   **city**: Ciudad del cliente.
*   **state**: Estado/Provincia.
*   **country**: País.
*   **zipcode**: Código postal.

## 2. Tabla: `departments` (Departamentos)
Organización de alto nivel de los productos.
*   **department_id** (PK): Identificador del departamento.
*   **department_name**: Nombre del departamento (p. ej., Fitness, Fan Shop).

## 3. Tabla: `categories` (Categorías)
Subdivisión de los departamentos.
*   **category_id** (PK): Identificador de la categoría.
*   **category_name**: Nombre de la categoría.
*   **department_id** (FK): Referencia a la tabla `departments`.

## 4. Tabla: `products` (Productos)
Catálogo de productos disponibles.
*   **product_id** (PK): Identificador único del producto (`product_card_id`).
*   **product_name**: Nombre del producto.
*   **category_id** (FK): Referencia a la tabla `categories`.
*   **price**: Precio unitario estándar.

## 5. Tabla: `orders` (Órdenes/Cabecera de Pedido)
Contiene la información general de la transacción.
*   **order_id** (PK): Identificador único del pedido.
*   **customer_id** (FK): Referencia al cliente que realizó el pedido.
*   **order_date**: Fecha del pedido.
*   **order_time**: Hora del pedido.
*   **order_status**: Estado actual (COMPLETE, PENDING, etc.).
*   **type**: Tipo de transacción (DEBIT, CASH, etc.).
*   **shipping_date**: Fecha real de envío.
*   **shipping_mode**: Modo de envío (Standard, First Class, etc.).
*   **order_region**: Región geográfica de entrega.
*   **order_city**: Ciudad de entrega.
*   **order_country**: País de entrega.
*   **days_for_shipping_real**: Días reales de envío.
*   **days_for_shipment_scheduled**: Días programados.
*   **delivery_status**: Estado de la entrega.
*   **late_delivery_risk**: Indicador de riesgo de retraso.

## 6. Tabla: `order_items` (Detalle de Pedido)
Relación entre productos y órdenes, con métricas financieras específicas de la línea.
*   **order_item_id** (PK): Identificador único del ítem.
*   **order_id** (FK): Referencia a la orden.
*   **product_id** (FK): Referencia al producto.
*   **quantity**: Cantidad comprada.
*   **unit_price**: Precio al momento de la compra (`order_item_product_price`).
*   **discount**: Monto del descuento aplicado.
*   **discount_rate**: Porcentaje de descuento.
*   **total_item_value**: Valor total de la línea (`order_item_total`).
*   **profit_ratio**: Ratio de beneficio del ítem.
*   **benefit_per_order**: Beneficio atribuido a este ítem.

---

## Ventajas de este Modelo:
1.  **Reducción de Redundancia**: El nombre del producto o la categoría no se repite en cada fila de venta, ahorrando espacio.
2.  **Integridad Referencial**: Asegura que no existan pedidos de clientes que no están registrados o productos en categorías inexistentes.
3.  **Flexibilidad**: Facilita actualizaciones masivas (por ejemplo, cambiar el nombre de una categoría en un solo lugar).
4.  **Escalabilidad**: Permite agregar fácilmente nuevas entidades como `stores` (tiendas) o `suppliers` (proveedores) sin afectar la estructura actual.
