USE food_orders_analytics_db;

-- 1. Total Order Value
SELECT SUM(`Order Value`) AS total_order_value
FROM cleaned_food_orders;


-- 2. Average Order Value
SELECT AVG(`Order Value`) AS average_order_value
FROM cleaned_food_orders;


-- 3. Most frequently used Payment Method
SELECT `Payment Method`, COUNT(*) AS total_orders
FROM cleaned_food_orders
GROUP BY `Payment Method`
ORDER BY total_orders DESC
LIMIT 1;


-- 4. Most frequently used Order Channel
SELECT `Order Channel`, COUNT(*) AS total_orders
FROM cleaned_food_orders
GROUP BY `Order Channel`
ORDER BY total_orders DESC
LIMIT 1;


-- 5. Average Delivery Time in Minutes
SELECT AVG(Delivery_Time_Minutes) AS average_delivery_minutes
FROM cleaned_food_orders;


-- 6. Total Platform Net Revenue
SELECT SUM(Platform_Net_Revenue) AS total_platform_net_revenue
FROM cleaned_food_orders;