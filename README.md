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
├── config/
├── dashboard/
│   └── streamlit_app.py
├── data/
│   ├── raw/
│   └── database/
├── docs/
│   └── data_dictionary.md
├── logs/
├── sql/
│   ├── ddl/
│   └── queries/
├── src/
│   ├── extract/
│   ├── transform/
│   ├── load/
│   ├── utils/
│   └── main.py
├── tests/
├── .github/
│   └── workflows/
├── requirements.txt
└── README.md
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

## Run Tests

```bash
pytest tests -v
```

Expected output

```
5 passed
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

Satish

Machine Learning & Data Engineering Enthusiast