# Propuesta de Normalización de Base de Datos (Refinada V2) - DataCo Supply Chain

Esta propuesta ha sido refinada para capturar la complejidad real del dataset identificada en el EDA, separando las entidades lógicas (Departamentos) de las ubicaciones físicas (Lat/Long) para evitar la pérdida de datos.

## 1. Tabla: `locations` (Puntos de Venta / Ubicaciones)
Almacena las coordenadas geográficas únicas presentes en el dataset.
*   **location_id** (PK): Identificador autoincremental para cada par único de coordenadas.
*   **latitude**: Latitud de la ubicación.
*   **longitude**: Longitud de la ubicación.

## 2. Tabla: `departments` (Departamentos)
Entidades organizacionales de la empresa.
*   **department_id** (PK): Identificador del departamento (1-11).
*   **department_name**: Nombre del departamento (p. ej., Fitness, Fan Shop).

## 3. Tabla: `categories` (Categorías)
*   **category_id** (PK): Identificador de la categoría.
*   **category_name**: Nombre de la categoría.

## 4. Tabla: `products` (Productos)
*   **product_card_id** (PK): Identificador único del producto.
*   **product_name**: Nombre del producto.
*   **category_id** (FK): Referencia a `categories`.
*   **product_price**: Precio de lista.

## 5. Tabla: `customers` (Clientes)
Vincula a los compradores con su información demográfica y su ubicación fija.
*   **customer_id** (PK): Identificador único del cliente.
*   **location_id** (FK): Referencia a la tabla `locations`.
*   **customer_fname**: Nombre.
*   **customer_lname**: Apellido.
*   **customer_segment**: Segmento.
*   **customer_street**: Dirección.
*   **customer_city**: Ciudad.
*   **customer_state**: Estado.
*   **customer_country**: País.
*   **customer_zipcode**: Código postal.

## 6. Tabla: `orders` (Órdenes / Logística)
Gestiona la transacción y el flujo de envío hacia el destino.
*   **order_id** (PK): Identificador único del pedido.
*   **customer_id** (FK): Referencia a `customers`.
*   **department_id** (FK): Referencia a `departments`.
*   **type**: Método de pago.
*   **order_date**: Fecha.
*   **order_time**: Hora.
*   **order_status**: Estado administrativo.
*   **order_city**: Ciudad de destino.
*   **order_country**: País de destino.
*   **order_region**: Región geográfica.
*   **shipping_mode**: Modo de envío.
*   **delivery_date**: Fecha de entrega.
*   **days_for_shipping_real**: Días reales.
*   **days_for_shipment_scheduled**: Días programados.
*   **delivery_status**: Estado logístico.
*   **late_delivery_risk**: Riesgo de retraso.

## 7. Tabla: `order_items` (Métricas de Venta)
Métricas por cada producto vendido en una orden.
*   **order_item_id** (PK): Identificador de la línea.
*   **order_id** (FK): Referencia a `orders`.
*   **product_id** (FK): Referencia a `products`.
*   **order_item_quantity**: Cantidad.
*   **order_item_product_price**: Precio en transacción.
*   **order_item_discount**: Descuento.
*   **order_item_discount_rate**: % Descuento.
*   **sales**: Venta bruta.
*   **order_item_total**: Venta neta (Mapeado de `sales_per_customer`).
*   **order_item_profit_ratio**: Ratio de beneficio.
*   **benefit_per_order**: Beneficio neto (Mapeado de `order_profit_per_order`).

---

## Mapeo de Integridad (Columnas CSV vs Tablas)

| Columna Original CSV | Tabla Destino | Justificación |
| :--- | :--- | :--- |
| `latitude`, `longitude` | `locations` | Representan la ubicación física. |
| `department_id`, `department_name` | `departments` | Entidad organizacional. |
| `customer_id`, `customer_fname`, ... | `customers` | Datos del comprador. |
| `order_id`, `order_status`, `order_city`, ... | `orders` | Datos de la cabecera del pedido. |
| `order_item_id`, `sales`, `order_item_total`, ... | `order_items` | Métricas de la transacción. |
| `product_card_id`, `product_name`, ... | `products` | Catálogo de productos. |
| `category_id`, `category_name` | `categories` | Jerarquía de productos. |

## Notas Técnicas sobre la Normalización:
1.  **Resolución de la Ambigüedad Geo**: El EDA mostró que hay ~11k ubicaciones pero solo 11 departamentos. Al crear la tabla `locations`, evitamos el error de usar `department_id` como PK, lo cual habría causado una pérdida masiva de datos geográficos.
2.  **Relación Cliente-Ubicación**: Se detectó que cada `customer_id` tiene una única lat/long asociada. Por ello, la `location_id` se asocia directamente al cliente en esta fase.
3.  **Mantenimiento de Métricas**: Se han incluido todas las columnas de métricas del CSV para asegurar que los dashboards posteriores tengan acceso a la misma información que el archivo original.
