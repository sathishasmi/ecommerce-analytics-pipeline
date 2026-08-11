import sqlite3
import pandas as pd
import streamlit as st
import plotly.express as px
from pathlib import Path

# Page Configuration
st.set_page_config(
    page_title="Live E-Commerce Analytics Dashboard",
    page_icon="📊",
    layout="wide"
)

st.title("📊 Live E-Commerce Analytics Dashboard")
st.markdown("---")

# Database Connection
BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "data" / "database" / "ecommerce_analytics.db"


@st.cache_resource
def get_connection():
    return sqlite3.connect(DB_PATH, check_same_thread=False)


conn = get_connection()


@st.cache_data
def load_query(query):
    return pd.read_sql_query(query, conn)


# Sidebar
st.sidebar.header("Filters")

category_df = load_query("""
SELECT DISTINCT category
FROM dim_products
WHERE category IS NOT NULL
ORDER BY category
""")

category_list = category_df["category"].tolist()

selected_categories = st.sidebar.multiselect(
    "Select Category",
    category_list,
    default=category_list
)

if len(selected_categories) == 0:
    selected_categories = category_list

category_filter = ",".join([f"'{c}'" for c in selected_categories])

# KPI Queries
revenue_query = f"""
SELECT COALESCE(ROUND(SUM(f.net_total), 2), 0.0) AS revenue
FROM fact_sales f
JOIN dim_products p ON f.product_id = p.product_id
WHERE p.category IN ({category_filter})
"""

orders_query = f"""
SELECT COUNT(DISTINCT f.order_id) AS orders
FROM fact_sales f
JOIN dim_products p ON f.product_id = p.product_id
WHERE p.category IN ({category_filter})
"""

customer_query = "SELECT COUNT(*) AS customers FROM dim_customers"

product_query = f"""
SELECT COUNT(DISTINCT p.product_id) AS products
FROM dim_products p
WHERE p.category IN ({category_filter})
"""

# Fetch KPI values safely
revenue = load_query(revenue_query).iloc[0, 0] or 0.0
orders = load_query(orders_query).iloc[0, 0] or 0
customers = load_query(customer_query).iloc[0, 0] or 0
products = load_query(product_query).iloc[0, 0] or 0

# KPI Cards
col1, col2, col3, col4 = st.columns(4)
col1.metric("💰 Total Revenue", f"${revenue:,.2f}")
col2.metric("🛒 Orders", f"{orders:,}")
col3.metric("👥 Customers", f"{customers:,}")
col4.metric("📦 Products", f"{products:,}")

st.markdown("---")

# Revenue by Category
category_query = f"""
SELECT 
    p.category,
    COUNT(DISTINCT f.order_id) AS total_orders,
    SUM(f.quantity) AS total_quantity,
    ROUND(SUM(f.net_total), 2) AS revenue
FROM fact_sales f
JOIN dim_products p ON f.product_id = p.product_id
WHERE p.category IN ({category_filter})
GROUP BY p.category
ORDER BY revenue DESC
"""

category_df = load_query(category_query)

fig1 = px.bar(
    category_df,
    x="category",
    y="revenue",
    color="revenue",
    text="revenue",
    title="Revenue by Category"
)
fig1.update_layout(xaxis_title="Category", yaxis_title="Revenue ($)")

fig2 = px.pie(
    category_df,
    names="category",
    values="revenue",
    title="Revenue Distribution"
)

left, right = st.columns(2)
with left:
    st.plotly_chart(fig1, use_container_width=True)
with right:
    st.plotly_chart(fig2, use_container_width=True)

# Customer Lifetime Value
clv_query = f"""
SELECT 
    c.user_id,
    c.first_name || ' ' || c.last_name AS customer,
    COUNT(DISTINCT f.order_id) AS total_orders,
    SUM(f.quantity) AS total_items,
    ROUND(SUM(f.net_total), 2) AS lifetime_value
FROM fact_sales f
JOIN dim_customers c ON f.user_id = c.user_id
JOIN dim_products p ON f.product_id = p.product_id
WHERE p.category IN ({category_filter})
GROUP BY c.user_id, customer
ORDER BY lifetime_value DESC
LIMIT 10
"""

clv_df = load_query(clv_query)

fig3 = px.bar(
    clv_df,
    x="lifetime_value",
    y="customer",
    orientation="h",
    color="lifetime_value",
    text="lifetime_value",
    title="Top 10 Customers by Lifetime Value"
)
fig3.update_layout(
    xaxis_title="Lifetime Value ($)",
    yaxis_title="",
    yaxis={'categoryorder': 'total ascending'}  # Keeps top customer at top
)

st.plotly_chart(fig3, use_container_width=True)

# Top Products
product_sales_query = f"""
SELECT 
    p.title,
    ROUND(SUM(f.net_total), 2) AS revenue
FROM fact_sales f
JOIN dim_products p ON f.product_id = p.product_id
WHERE p.category IN ({category_filter})
GROUP BY p.title
ORDER BY revenue DESC
LIMIT 10
"""

top_products = load_query(product_sales_query)

fig4 = px.bar(
    top_products,
    x="title",
    y="revenue",
    color="revenue",
    text="revenue",
    title="Top 10 Products by Revenue"
)
fig4.update_layout(xaxis_title="Product", yaxis_title="Revenue ($)")

st.plotly_chart(fig4, use_container_width=True)

# Recent Transactions
st.subheader("Recent Transactions")

transaction_query = f"""
SELECT 
    f.order_id,
    f.user_id,
    p.title,
    p.category,
    f.quantity,
    f.unit_price,
    f.discount_percentage,
    f.net_total
FROM fact_sales f
JOIN dim_products p ON f.product_id = p.product_id
WHERE p.category IN ({category_filter})
ORDER BY f.order_id DESC
LIMIT 20
"""

transactions = load_query(transaction_query)
st.dataframe(transactions, use_container_width=True, hide_index=True)

st.markdown("---")
st.caption("Built with Streamlit • SQLite • Plotly • Python")