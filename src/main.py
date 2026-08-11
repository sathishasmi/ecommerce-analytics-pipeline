from src.extract.api_client import (
    fetch_raw_api_data,
    fetch_users_data,
    fetch_products_data,
)
from src.transform.flattener import flatten_json_data
from src.transform.data_cleaner import (
    clean_raw_data,
    build_star_schema_tables,
)
from src.load.db_loader import DatabaseLoader
from src.utils.logger import setup_logger


logger = setup_logger()


def run_pipeline():
    """Runs the complete ETL Pipeline."""

    logger.info("=" * 70)
    logger.info("Starting Live E-Commerce ETL Pipeline")
    logger.info("=" * 70)

    try:
        # 1. Extract
        logger.info("Step 1/6 : Extracting data from API...")

        raw_data = fetch_raw_api_data(
            "https://dummyjson.com/carts"
        )

        users_json = fetch_users_data()
        
        products = fetch_products_data()

        logger.info("API data extracted successfully.")

        # 2. Flatten JSON
        logger.info("Step 2/6 : Flattening JSON data...")

        df_flat = flatten_json_data(raw_data["carts"])

        logger.info(
            f"Flattened dataframe shape: {df_flat.shape}"
        )

        # 3. Clean Data
        logger.info("Step 3/6 : Cleaning data...")

        df_clean = clean_raw_data(df_flat)

        logger.info(
            f"Clean dataframe shape: {df_clean.shape}"
        )

        # 4. Build Star Schema
        logger.info("Step 4/6 : Building Star Schema...")

        star_tables = build_star_schema_tables(
            df_clean,
            users_json,
            products
        )

        logger.info("Star Schema created successfully.")

        logger.info(
            f"dim_customers : {len(star_tables['dim_customers'])} rows"
        )
        logger.info(
            f"dim_products : {len(star_tables['dim_products'])} rows"
        )
        logger.info(
            f"fact_sales : {len(star_tables['fact_sales'])} rows"
        )

        # 5. Initialize Database
        logger.info("Step 5/6 : Creating database schema...")

        loader = DatabaseLoader()

        loader.initialize_schema()

        logger.info("Database schema initialized.")

        # 6. Load Data
        logger.info("Step 6/6 : Loading data into database...")

        loader.load_star_schema(star_tables)

        logger.info("Database loading completed.")

        logger.info("=" * 70)
        logger.info("ETL Pipeline Completed Successfully")
        logger.info("=" * 70)

    except Exception as e:
        logger.exception(f"Pipeline Failed: {e}")
        raise


if __name__ == "__main__":
    run_pipeline()