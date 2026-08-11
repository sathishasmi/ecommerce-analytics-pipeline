# Live E-Commerce Data Pipeline & Analytics Engine

## Overview

This project is an end-to-end Data Engineering pipeline that extracts e-commerce transaction data from the DummyJSON API, transforms it into a Star Schema, stores it in SQLite, and visualizes business insights using Streamlit.

---

## Architecture

```
DummyJSON API
       │
       ▼
Extract (API Client)
       │
       ▼
Flatten JSON
       │
       ▼
Data Cleaning
       │
       ▼
Star Schema Transformation
       │
       ▼
SQLite Database
       │
       ▼
Streamlit Dashboard
```

---

## Project Structure

```
.
ecommerce-analytics-pipeline/
├── .github/
│   └── workflows/
│       └── pipeline_ci.yml          # GitHub Actions workflow for automated testing
├── config/
│   ├── config.yaml                  # Global pipeline settings
│   └── db_config.ini                # DB connection & API endpoint configuration
├── data/
│   └── database/
│       └── ecommerce_analytics.db   # SQLite database file storing Star Schema
├── docs/
│   └── data_dictionary.md           # Schema definitions for fact & dimension tables
├── logs/
│   └── pipeline.log                 # Automated execution logs and error traces
├── src/
│   ├── __init__.py
│   ├── extract/
│   │   ├── __init__.py
│   │   └── api_client.py            # API requests, retries, and rate limiting
│   ├── transform/
│   │   ├── __init__.py
│   │   ├── flattener.py             # Unnests complex JSON payloads
│   │   └── data_cleaner.py          # Type casting, null handling, & deduplication
│   ├── load/
│   │   ├── __init__.py
│   │   └── db_loader.py             # SQLite loader for Star Schema tables
│   ├── utils/
│   │   ├── __init__.py
│   │   └── logger.py                # Centralized pipeline logger setup
│   └── main.py                      # Core ETL orchestration entry point
├── sql/
│   ├── ddl/
│   │   └── create_tables.sql        # DDL scripts for Star Schema tables
│   └── queries/
│       ├── category_performance.sql # SQL business performance queries
│       └── customer_clv.sql         # Advanced SQL queries (CTEs/Window functions)
├── dashboard/
│   ├── streamlit_app.py             # Interactive Streamlit analytics application
│   └── components/                  # Custom dashboard components and styling
├── tests/
│   ├── __init__.py
│   ├── test_extract.py              # Unit tests for API endpoints & mocking
│   └── test_transform.py            # Unit tests for flattening & data cleaning
├── .env.example                     # Environment variables template
├── .gitignore                       # Excludes temporary files, DBs, and virtual envs
├── README.md                        # Portfolio documentation & setup instructions
└── requirements.txt                 # Project dependencies
```

---

## Technologies Used

- Python 3.10+
- Pandas
- SQLite
- Streamlit
- Plotly
- Requests
- Pytest
- GitHub Actions

---

## Features

- Extract data from DummyJSON REST API
- Flatten nested JSON
- Clean raw datasets
- Handle missing values
- Build Star Schema
- Store data in SQLite
- Interactive Streamlit Dashboard
- Automated Unit Testing
- Continuous Integration using GitHub Actions

---

## Database Schema

### Fact Table

```
fact_sales
```

Contains:

- order_id
- user_id
- product_id
- quantity
- unit_price
- discount_percentage
- gross_amount
- discount_amount
- net_total

### Dimension Tables

```
dim_customers
```

- user_id
- first_name
- last_name
- email
- gender
- city
- state

```
dim_products
```

- product_id
- title
- category
- price

---

## ER Diagram

```
             dim_customers
             --------------
             user_id (PK)
                    │
                    │
                    ▼
fact_sales ---------------- dim_products
-----------                 -------------
order_id                    product_id (PK)
user_id (FK) --------------►
product_id(FK)-------------►
quantity
unit_price
discount_percentage
gross_amount
discount_amount
net_total
```

---

## Installation

Clone the repository

```bash
git clone <repository-url>
```

Create a virtual environment

```bash
python -m venv .venv
```

Activate

Windows

```bash
.venv\Scripts\activate
```

Linux/Mac

```bash
source .venv/bin/activate
```

Install dependencies

```bash
pip install -r requirements.txt
```

---

## Run Pipeline

```bash
python src/main.py
```

---

## Launch Dashboard

```bash
streamlit run dashboard/streamlit_app.py
```

---

## Dashboard

Displays

- Revenue
- Orders
- Customers
- Products
- Revenue by Category
- Customer Lifetime Value
- Top Products
- Recent Transactions

---

## Future Improvements

- Docker Support
- PostgreSQL
- Apache Airflow
- AWS Deployment
- Power BI Integration

---

## Author

Satheesh

Machine Learning & Data Engineering Enthusiast