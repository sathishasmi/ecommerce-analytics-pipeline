
-- Clean up existing tables (Drop in reverse order of foreign key dependencies)
DROP TABLE IF EXISTS fact_sales;
DROP TABLE IF EXISTS dim_products;
DROP TABLE IF EXISTS dim_customers;


-- 1. DIMENSION TABLE: Customers (dim_customers)
-- Stores descriptive attributes about the users/customers

CREATE TABLE dim_customers (
    user_id          INTEGER PRIMARY KEY,
    first_name       VARCHAR(100),
    last_name        VARCHAR(100),
    email            VARCHAR(255),
    gender           VARCHAR(20),
    city             VARCHAR(100),
    state            VARCHAR(100),
    customer_status  VARCHAR(50) DEFAULT 'Active',
    created_at       TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


-- 2. DIMENSION TABLE: Products (dim_products)
-- Stores product metadata, pricing, and category classifications

CREATE TABLE dim_products (

    product_id INTEGER PRIMARY KEY,

    title VARCHAR(255),

    category VARCHAR(255),
    
    price NUMERIC(10,2),

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


-- 3. FACT TABLE: Sales Transactions (fact_sales)
-- Stores transaction metrics and references Dimension keys

CREATE TABLE fact_sales (

    sale_id INTEGER PRIMARY KEY AUTOINCREMENT,
    
    order_id INTEGER,

    user_id INTEGER,

    product_id INTEGER,

    quantity INTEGER,

    unit_price NUMERIC(10,2),

    discount_percentage NUMERIC(5,2),

    gross_amount NUMERIC(10,2),

    discount_amount NUMERIC(10,2),

    net_total NUMERIC(10,2),

    order_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY(user_id)
        REFERENCES dim_customers(user_id),

    FOREIGN KEY(product_id)
        REFERENCES dim_products(product_id)
);


-- PERFORMANCE INDEXES
-- Accelerate heavy JOINs and aggregation queries in analytical engines

-- Foreign Key Indexes on the Fact Table
CREATE INDEX idx_fact_sales_user ON fact_sales(user_id);
CREATE INDEX idx_fact_sales_product ON fact_sales(product_id);