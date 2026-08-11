import pandas as pd
import numpy as np
from src.utils.logger import setup_logger

logger = setup_logger()


def clean_raw_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Performs primary data hygiene on the flattened DataFrame:
    - Drops exact duplicate rows
    - Cleans column names (standardizes casing and spaces)
    - Fills or drops null values
    - Standardizes date formats and data types
    """
    logger.info("Starting raw data cleaning process...")
    
    # 1. Clean Column Names (e.g., " User ID " -> "user_id")
    df.columns = (
        df.columns.str.strip()
        .str.lower()
        .str.replace(" ", "_")
        .str.replace(".", "_")
    )
    
    # 2. Drop Exact Duplicates
    initial_rows = len(df)
    df = df.drop_duplicates().copy()
    dropped_dups = initial_rows - len(df)
    if dropped_dups > 0:
        logger.warning(f"Dropped {dropped_dups} duplicate row(s).")

    # 3. Handle Null Values
    # Fill missing text with 'Unknown' and missing numbers with 0
    string_cols = df.select_dtypes(include=['object']).columns
    df[string_cols] = df[string_cols].fillna("Unknown")
    
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    df[numeric_cols] = df[numeric_cols].fillna(0)

    logger.info(f"Primary cleaning complete. Rows remaining: {len(df)}")
    return df


def build_star_schema_tables(
        df: pd.DataFrame,
        users_json: list,
        products_json: list
    ) -> dict:
    """
    Splits the cleaned, flattened DataFrame into Dimension and Fact DataFrames 
    following a Star Schema design.

    Returns:
        dict: A dictionary containing 'dim_customers', 'dim_products', and 'fact_sales'.
    """
    logger.info("Transforming cleaned data into Star Schema tables...")

    try:
        users = users_json 

        products = products_json

        dim_customers = pd.DataFrame([
            {
                "user_id": user["id"],
                "first_name": user["firstName"],
                "last_name": user["lastName"],
                "email": user["email"],
                "gender": user["gender"],
                "city": user["address"]["city"],
                "state": user["address"]["state"],
                "customer_status": "Active"
            }
            for user in users
        ])

        logger.info(f"Built 'dim_customers' shape: {dim_customers.shape}")

        # Extract product specific attributes
        products_df = pd.DataFrame(products)

        dim_products = products_df[
            [
                "id",
                "title",
                "category",
                "price"
            ]
        ].copy()

        dim_products.rename(
            columns={
                "id": "product_id"
            },
            inplace=True
        )

        dim_products["price"] = pd.to_numeric(
            dim_products["price"],
            errors="coerce"
        ).fillna(0)

        logger.info(f"Built 'dim_products' shape: {dim_products.shape}")

        # Contains key transactional metrics and foreign keys
        fact_sales = pd.DataFrame()
        
        # Primary Keys & Foreign Keys
        fact_sales["order_id"] = (
            df["order_id"]
            if "order_id" in df.columns
            else range(1, len(df) + 1)
        )
        fact_sales["user_id"] = (
            df["user_id"]
            if "user_id" in df.columns
            else pd.Series(0, index=df.index)
        )
        fact_sales["product_id"] = (
            df["product_id"]
            if "product_id" in df.columns
            else df.get("id", pd.Series(0, index=df.index))
        )
        
        fact_sales["quantity"] = pd.to_numeric(
            df["quantity"] if "quantity" in df.columns else pd.Series(1, index=df.index),
            errors="coerce"
        ).fillna(1).astype(int)

        fact_sales["unit_price"] = pd.to_numeric(
            df["price"] if "price" in df.columns else pd.Series(0.0, index=df.index),
            errors="coerce"
        ).fillna(0.0).round(2)

        fact_sales["discount_percentage"] = pd.to_numeric(
            df["discount_percentage"] if "discount_percentage" in df.columns else pd.Series(0.0, index=df.index),
            errors="coerce"
        ).fillna(0.0)
        
        # Derived Metric Calculation (Business Logic)
        gross_amount = fact_sales['quantity'] * fact_sales['unit_price']
        discount_amount = gross_amount * (fact_sales['discount_percentage'] / 100.0)
        fact_sales['net_total'] = (gross_amount - discount_amount).round(2)
        fact_sales["gross_amount"] = gross_amount.round(2)
        fact_sales["discount_amount"] = discount_amount.round(2)
        fact_sales["net_total"] = (gross_amount - discount_amount).round(2)
        
        logger.info(f"Built 'fact_sales' shape: {fact_sales.shape}")

        return {
            "dim_customers": dim_customers,
            "dim_products": dim_products,
            "fact_sales": fact_sales
        }

    except Exception as e:
        logger.error(f"Error while building Star Schema tables: {e}")
        raise