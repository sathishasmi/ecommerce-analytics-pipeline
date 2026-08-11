WITH customer_sales AS (
    SELECT
        c.user_id,
        c.first_name || ' ' || c.last_name AS customer_name,
        COUNT(DISTINCT f.order_id) AS total_orders,
        SUM(f.quantity) AS total_items,
        ROUND(SUM(f.net_total), 2) AS lifetime_value
    FROM fact_sales f
    JOIN dim_customers c
        ON f.user_id = c.user_id
    GROUP BY
        c.user_id,
        customer_name
)

SELECT
    user_id,
    customer_name,
    total_orders,
    total_items,
    lifetime_value,
    RANK() OVER (
        ORDER BY lifetime_value DESC
    ) AS customer_rank
FROM customer_sales
ORDER BY customer_rank;