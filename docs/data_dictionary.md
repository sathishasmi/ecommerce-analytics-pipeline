# Data Dictionary: E-Commerce Analytics Star Schema

## 1. Overview

This document describes the database schema, columns, data types, keys,
nullability rules, and business calculations used by the Live E-Commerce
Data Pipeline & Analytics Engine.

The pipeline transforms raw e-commerce API data into a dimensional
Star Schema consisting of:

- fact_sales - Fact table containing transactional sales metrics.
- dim_customers - Customer dimension containing customer information.
- dim_products - Product dimension containing product information.

---

# 2. Database Schema

## 2.1 Star Schema Overview

The database follows a Star Schema design.

```text
                         ┌──────────────────────┐
                         │    dim_customers     │
                         ├──────────────────────┤
                         │ PK user_id           │
                         │ first_name           │
                         │ last_name            │
                         │ email                │
                         │ gender               │
                         │ city                 │
                         │ state                │
                         │ customer_status      │
                         └──────────┬───────────┘
                                    │
                                    │ user_id
                                    │
                                    ▼
                         ┌──────────────────────┐
                         │     fact_sales       │
                         ├──────────────────────┤
                         │ PK order_id          │
                         │ FK user_id           │
                         │ FK product_id        │
                         │ quantity             │
                         │ unit_price           │
                         │ discount_percentage  │
                         │ gross_amount         │
                         │ discount_amount      │
                         │ net_total            │
                         └──────────┬───────────┘
                                    │
                                    │ product_id
                                    │
                                    ▼
                         ┌──────────────────────┐
                         │     dim_products     │
                         ├──────────────────────┤
                         │ PK product_id        │
                         │ title                │
                         │ category             │
                         │ price                │
                         └──────────────────────┘
```

# 3. Table Specifications

## 3.1 fact_sales (Fact Table)
Description:
Contains transactional sales information and calculated business metrics.

Grain:
One row represents one product line item within an order.

Primary Key:
order_id

Foreign Keys:

1. user_id references dim_customers.user_id
2. product_id references dim_products.product_id


| Column Name           | Data Type | Key Type | Nullable | Description / Business Rule                                                              |
| --------------------- | --------- | -------- | -------- | ---------------------------------------------------------------------------------------- |
| `order_id`            | INTEGER   | PK       | No       | Unique identifier for each order.                                                        |
| `user_id`             | INTEGER   | FK       | No       | Customer identifier associated with the order.                                           |
| `product_id`          | INTEGER   | FK       | No       | Product identifier associated with the order line.                                       |
| `quantity`            | INTEGER   | —        | No       | Number of units purchased. Missing values are standardized to `1`.                       |
| `unit_price`          | REAL      | —        | No       | Price of one unit of the product. Missing values are standardized to `0.0`.              |
| `discount_percentage` | REAL      | —        | No       | Discount percentage applied to the order line. Missing values are standardized to `0.0`. |
| `gross_amount`        | REAL      | —        | No       | Total amount before applying the discount.                                               |
| `discount_amount`     | REAL      | —        | No       | Monetary discount calculated from the gross amount.                                      |
| `net_total`           | REAL      | —        | No       | Final transaction value after applying the discount.                                     |


## 3.2 dim_products (Dimension Table)

Description:
Contains descriptive information about products available on the platform.

Grain:
One row per unique product.

Primary Key:
product_id

| Column Name  | Data Type | Key Type | Nullable | Description / Business Rule                                                      |
| ------------ | --------- | -------- | -------- | -------------------------------------------------------------------------------- |
| `product_id` | INTEGER   | PK       | No       | Unique identifier for each product.                                              |
| `title`      | TEXT      | —        | No       | Full product name or description.                                                |
| `category`   | TEXT      | —        | No       | Product classification category, such as `smartphones` or `laptops`.             |
| `price`      | REAL      | —        | No       | Standard list price of the product. Invalid numeric values are converted to `0`. |


# 3.3 dim_customers (Dimension Table)

Description:
Contains demographic and profile information for registered platform users.

Grain:
One row per unique customer/user ID.

Primary Key:
user_id

| Column Name       | Data Type | Key Type | Nullable | Description / Business Rule                                                       |
| ----------------- | --------- | -------- | -------- | --------------------------------------------------------------------------------- |
| `user_id`         | INTEGER   | PK       | No       | Unique identifier for each registered customer.                                   |
| `first_name`      | TEXT      | —        | No       | Customer's first name.                                                            |
| `last_name`       | TEXT      | —        | No       | Customer's last name.                                                             |
| `email`           | TEXT      | —        | No       | Customer's primary contact email address.                                         |
| `gender`          | TEXT      | —        | Yes      | Customer gender attribute provided by the source API.                             |
| `city`            | TEXT      | —        | Yes      | Primary residential city extracted from the address payload.                      |
| `state`           | TEXT      | —        | Yes      | Primary residential state extracted from the address payload.                     |
| `customer_status` | TEXT      | —        | No       | Customer status. The current transformation assigns `Active` to loaded customers. |

---

# 4. Relationships

The Star Schema uses the fact_sales table as the central transactional
table.

Customer Relationship
```text
dim_customers.user_id
        │
        │ 1
        │
        │
        │ N
        ▼
fact_sales.user_id
```

One customer can have multiple sales transactions.

Product Relationship
```text
dim_products.product_id
        │
        │ 1
        │
        │
        │ N
        ▼
fact_sales.product_id
```
One product can appear in multiple sales transactions.

# 5. Business Calculation Rules

## 5.1 Gross Amount

The gross amount represents the total sales value before applying any
discount.

gross_amount = quantity × unit_price

Example:

quantity   = 2
unit_price = 1000

gross_amount = 2 × 1000
             = 2000

## 5.2 Discount Amount

The discount amount is calculated from the gross amount and the
discount percentage.

discount_amount =
    gross_amount × (discount_percentage / 100)

Example:

gross_amount        = 2000
discount_percentage = 10

discount_amount = 2000 × (10 / 100)
                = 200

## 5.3 Net Total

The net total represents the final sales amount after applying the discount.

net_total = gross_amount - discount_amount

Equivalent formula:

net_total =
    (quantity × unit_price)
    × (1 - discount_percentage / 100)

Example:
gross_amount    = 2000
discount_amount = 200

net_total = 2000 - 200
          = 1800

# 6. Data Cleaning Rules

The pipeline performs several data-quality operations before loading
data into the analytical model.

## 6.1 Column Name Standardization

Column names are standardized by:

1. Removing leading and trailing spaces.
2. Converting names to lowercase.
3. Replacing spaces with underscores.
4. Replacing hyphens with underscores.

Example:
" User ID "

becomes:
"user_id"

## 6.2 Duplicate Removal
Exact duplicate rows are removed from the dataset.
df.drop_duplicates()
This prevents duplicate records from affecting analytical results.

## 6.3 Missing Text Values

Missing values in text/object columns are replaced with:
Unknown

Example:
city = NULL

becomes:
city = "Unknown"

## 6.4 Missing Numeric Values
Missing numeric values are replaced with:
0

This prevents null values from causing calculation or aggregation
problems.

## 6.5 Quantity 
When transaction quantity is missing or invalid:
quantity = 1

This provides a safe default for transaction calculations.

## 6.6 Price Default
When a product or transaction price is missing or invalid:
price = 0.0
Invalid numeric values are converted using numeric coercion.

## 6.7 Discount Default

When the discount percentage is missing:
discount_percentage = 0.0

This means no discount is applied.

# 7. Data Type Standardization

The transformation layer standardizes important analytical fields.
| Field                 | Final Data Type |
| --------------------- | --------------- |
| `order_id`            | INTEGER         |
| `user_id`             | INTEGER         |
| `product_id`          | INTEGER         |
| `quantity`            | INTEGER         |
| `unit_price`          | REAL            |
| `discount_percentage` | REAL            |
| `gross_amount`        | REAL            |
| `discount_amount`     | REAL            |
| `net_total`           | REAL            |

Numeric conversion uses Pandas numeric coercion to safely handle
invalid input values.

# 8. Analytical Metrics

The Star Schema supports several analytical metrics.

## 8.1 Total Revenue
Total Revenue = SUM(net_total)

## 8.2 Total Orders
Total Orders = COUNT(DISTINCT order_id)

## 8.3 Total Quantity Sold
Total Quantity Sold = SUM(quantity)

## 8.4 Average Order Value
Average Order Value =
    SUM(net_total) / COUNT(DISTINCT order_id)

## 8.5 Total Discount
Total Discount = SUM(discount_amount)

## 8.6 Customer Lifetime Value
Customer Lifetime Value is calculated as the total net revenue
generated by each customer.

CLV = SUM(net_total)
      GROUP BY user_id

## 8.7 Revenue by Product

Revenue by Product =
    SUM(net_total)
    GROUP BY product_id

## 8.8 Revenue by Category

Revenue can be analyzed by joining:
```text
fact_sales
    ↓
product_id
    ↓
dim_products
    ↓
category
```
Then:

Revenue by Category =
    SUM(net_total)
    GROUP BY category

# 9. Data Flow
The pipeline follows the following process:
```text
1. Extract
   ↓
2. Receive JSON from API
   ↓
3. Flatten nested JSON
   ↓
4. Clean and validate data
   ↓
5. Build dimension tables
   ↓
6. Build fact table
   ↓
7. Calculate business metrics
   ↓
8. Load into SQLite
   ↓
9. Query analytical data
   ↓
10. Display results in Streamlit dashboard
```
# 10. Data Quality Rules

The pipeline is designed to protect downstream analytics from bad
input data.

The following checks and transformations are performed:

* HTTP API errors are detected.
* Request failures are handled.
* Duplicate rows are removed.
* Column names are standardized.
* Missing text values are replaced with Unknown.
* Missing numeric values are replaced with 0.
* Invalid numeric values are safely coerced.
* Quantity values default to 1 when unavailable.
* Discount values default to 0.
* Price values default to 0.
* Derived financial metrics are calculated consistently.

# 11. Testing
The project uses pytest for automated testing.

Tests cover:

* API status/error handling.
* Raw API extraction.
* User data extraction.
* Product data extraction.
* JSON flattening.
* Data cleaning.
* Duplicate removal.
* Null-value handling.
* Star Schema transformation.

Run the complete test suite using:
pytest tests -v

Expected result:
5 passed

or more tests depending on the current test suite.

# 12. Database Technology

The project currently uses:
SQLite

The database file is:
data/database/ecommerce_analytics.db

SQLite is used because it is lightweight, portable, and suitable for
local analytical workloads and project demonstrations.

# 13. Source Data

The pipeline uses the DummyJSON REST API as the source system.

The API provides:

* Customer/user information.
* Product information.
* E-commerce cart/order information.

The extracted JSON is transformed into an analytical Star Schema before
being loaded into the SQLite database.

# 14. Schema Summary
```text
| Table           | Type      | Primary Key  | Purpose                     |
| --------------- | --------- | ------------ | --------------------------- |
| `fact_sales`    | Fact      | `order_id`   | Transactional sales metrics |
| `dim_customers` | Dimension | `user_id`    | Customer information        |
| `dim_products`  | Dimension | `product_id` | Product information         |
```

# 15. Design Summary

The Star Schema separates:

Measures
Stored in:
fact_sales

Examples

quantity
unit_price
gross_amount
discount_amount
net_total

Descriptive Attributes

Stored in:

dim_customers
dim_products

This design makes analytical queries easier and supports dashboard

metrics such as:
1. Revenue
2. Orders
3. Discounts
4. Customer Lifetime Value
5. Product performance
6. Category performance
7. Customer analysis
