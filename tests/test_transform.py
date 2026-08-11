import pandas as pd

from src.transform.data_cleaner import (
    clean_raw_data,
    build_star_schema_tables,
)


def test_clean_raw_data():

    df = pd.DataFrame({
        "Order ID": [1, 1],
        "Price": [100, 100],
        "Category": ["Phone", "Phone"]
    })

    cleaned = clean_raw_data(df)

    assert isinstance(cleaned, pd.DataFrame)
    assert "order_id" in cleaned.columns
    assert len(cleaned) == 1


def test_build_star_schema_tables():

    df = pd.DataFrame({
        "order_id": [1],
        "user_id": [1],
        "product_id": [1],
        "quantity": [2],
        "price": [1000],
        "discount_percentage": [10]
    })

    users = [
        {
            "id": 1,
            "firstName": "John",
            "lastName": "Doe",
            "email": "john@test.com",
            "gender": "male",
            "address": {
                "city": "Bangalore",
                "state": "Karnataka"
            }
        }
    ]

    products = [
        {
            "id": 1,
            "title": "iPhone",
            "category": "phones",
            "price": 1000
        }
    ]

    tables = build_star_schema_tables(
        df,
        users,
        products
    )

    assert isinstance(tables, dict)

    assert "dim_customers" in tables
    assert "dim_products" in tables
    assert "fact_sales" in tables

    assert len(tables["dim_customers"]) == 1
    assert len(tables["dim_products"]) == 1
    assert len(tables["fact_sales"]) == 1