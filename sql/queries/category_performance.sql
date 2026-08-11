WITH category_sales AS (
    SELECT
        p.category,
        COUNT(DISTINCT f.order_id) AS total_orders,
        SUM(f.quantity) AS total_quantity,
        ROUND(SUM(f.net_total), 2) AS total_revenue
    FROM fact_sales f
    JOIN dim_products p
        ON f.product_id = p.product_id
    GROUP BY p.category
)
SELECT
    category,
    total_orders,
    total_quantity,
    total_revenue,
    RANK() OVER (ORDER BY total_revenue DESC) AS revenue_rank
FROM category_sales
ORDER BY revenue_rank;