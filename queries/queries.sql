USE dataco;

SELECT days_for_shipping_real, days_for_shipment_scheduled, late_delivery_risk
	FROM orders;
    
/** Más de la mitad de los pedidos no cunmplen el plazo**/
SELECT late_delivery_risk, COUNT(*) AS total_pedidos, ROUND((COUNT(*) / (SELECT COUNT(*) FROM orders)) * 100, 2) AS porcentaje
FROM orders
GROUP BY late_delivery_risk;

SELECT customer_country, late_delivery_risk
	FROM customers, orders
		WHERE late_delivery_risk = 1;
 

SELECT 
    cu.customer_city, 
    cu.customer_state, 
    COUNT(*) AS total_pedidos, 
    ROUND((COUNT(*) / (SELECT COUNT(*) FROM orders)) * 100, 2) AS porcentaje
FROM customers AS cu
INNER JOIN orders AS ord
    ON cu.customer_id = ord.customer_id
WHERE ord.late_delivery_risk = 1 -- <--- El filtro va aquí, antes de agrupar
GROUP BY cu.customer_city, cu.customer_state
ORDER BY porcentaje desc;

/** ¿Qué porcentaje del TOTAL DE ENVIOS CON RETRASO se concentra en cada ciudad?
(Ideal para saber dónde se origina el grueso de tus problemas de distribución a nivel nacional).**/

SELECT 
    cu.customer_city, 
    cu.customer_state, 
    COUNT(*) AS total_pedidos, 
    -- Divide entre el total de pedidos que tienen riesgo = 1
    ROUND((COUNT(*) / (SELECT COUNT(*) FROM orders WHERE late_delivery_risk = 1)) * 100, 2) AS porcentaje
FROM customers AS cu
INNER JOIN orders AS ord
    ON cu.customer_id = ord.customer_id
WHERE ord.late_delivery_risk = 1 
GROUP BY cu.customer_city, cu.customer_state
ORDER BY porcentaje DESC;

/**¿Qué porcentaje de los pedidos DE ESA CIUDAD se entregan tarde?
(Ideal para saber qué tan eficiente es la logística local. Ej: "En Springfield el 80% de los envíos llegan tarde").**/

SELECT 
    cu.customer_city, 
    cu.customer_state, 
    SUM(CASE WHEN ord.late_delivery_risk = 1 THEN 1 ELSE 0 END) AS total_pedidos_retraso, 
    -- Divide los retrasos de la ciudad entre TODOS los pedidos de esa misma ciudad
    ROUND((SUM(CASE WHEN ord.late_delivery_risk = 1 THEN 1 ELSE 0 END) / COUNT(*)) * 100, 2) AS porcentaje_retraso_local
FROM customers AS cu
INNER JOIN orders AS ord
    ON cu.customer_id = ord.customer_id
GROUP BY cu.customer_city, cu.customer_state
ORDER BY porcentaje_retraso_local DESC;

/** ¿Qué porcentaje del TOTAL DE ENVIOS CON RETRASO se concentra en cada ciudad?
(Ideal para saber dónde se origina el grueso de tus problemas de distribución a nivel nacional). pero solo por estado**/

SELECT 
     
    cu.customer_state, 
    COUNT(*) AS total_pedidos, 
    -- Divide entre el total de pedidos que tienen riesgo = 1
    ROUND((COUNT(*) / (SELECT COUNT(*) FROM orders WHERE late_delivery_risk = 1)) * 100, 2) AS porcentaje
FROM customers AS cu
INNER JOIN orders AS ord
    ON cu.customer_id = ord.customer_id
WHERE ord.late_delivery_risk = 1 
GROUP BY cu.customer_state
ORDER BY porcentaje DESC;

/**¿Qué porcentaje de los pedidos DE ESA CIUDAD se entregan tarde?
(Ideal para saber qué tan eficiente es la logística local. Ej: "En Springfield el 80% de los envíos llegan tarde"). pero solo estado**/

SELECT 
     
    cu.customer_state, 
    SUM(CASE WHEN ord.late_delivery_risk = 1 THEN 1 ELSE 0 END) AS total_pedidos_retraso, 
    -- Divide los retrasos de la ciudad entre TODOS los pedidos de esa misma ciudad
    ROUND((SUM(CASE WHEN ord.late_delivery_risk = 1 THEN 1 ELSE 0 END) / COUNT(*)) * 100, 2) AS porcentaje_retraso_local
FROM customers AS cu
INNER JOIN orders AS ord
    ON cu.customer_id = ord.customer_id
GROUP BY  cu.customer_state
ORDER BY porcentaje_retraso_local DESC;


   





