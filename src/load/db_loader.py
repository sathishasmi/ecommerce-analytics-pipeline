import os
import sqlite3
import pandas as pd
from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError
from src.utils.logger import setup_logger

logger = setup_logger()


class DatabaseLoader:
    """Handles database connections, table creation, and bulk data loading."""

    def __init__(self, db_uri: str = "sqlite:///data/database/ecommerce_analytics.db"):
        """
        Initializes the DatabaseLoader engine.
        
        Args:
            db_uri (str): SQLAlchemy database connection string.
                          Defaults to local SQLite database in data/ directory.
        """
        self.db_uri = db_uri
        
        # Ensure directory exists if using default SQLite
        if db_uri.startswith("sqlite"):
            os.makedirs("data/database", exist_ok=True)
            
        try:
            self.engine = create_engine(self.db_uri, echo=False)
            logger.info(f"Connected to database engine: {self.db_uri.split('://')[0]}")
        except Exception as e:
            logger.error(f"Failed to create database engine: {e}")
            raise

    def initialize_schema(self, ddl_file_path: str = "sql/ddl/create_tables.sql") -> None:
        """
        Executes DDL statements from an SQL file to initialize tables and indexes.
        """
        if not os.path.exists(ddl_file_path):
            logger.error(f"DDL script not found at path: {ddl_file_path}")
            raise FileNotFoundError(f"DDL script missing: {ddl_file_path}")

        logger.info(f"Executing DDL schema setup from: {ddl_file_path}...")
        
        try:
            with open(ddl_file_path, "r") as file:
                sql_script = file.read()

            # Split statements by semicolon for clean execution
            statements = [stmt.strip() for stmt in sql_script.split(";") if stmt.strip()]

            with self.engine.begin() as connection:
                for statement in statements:
                    connection.execute(text(statement))
                    
            logger.info("Database schema initialized successfully.")

        except SQLAlchemyError as e:
            logger.error(f"Error initializing database schema: {e}")
            raise

    def load_table(self, df: pd.DataFrame, table_name: str, if_exists: str = "append") -> None:
        """
        Loads a Pandas DataFrame into the specified database table.

        Args:
            df (pd.DataFrame): The DataFrame to load.
            table_name (str): Name of the target SQL table.
            if_exists (str): 'append', 'replace', or 'fail'. Defaults to 'append'.
        """
        if df.empty:
            logger.warning(f"DataFrame for table '{table_name}' is empty. Skipping load.")
            return

        logger.info(f"Loading {len(df)} row(s) into target table '{table_name}'...")
        
        try:
            # Load data using SQLAlchemy engine
            df.to_sql(
                name=table_name,
                con=self.engine,
                if_exists=if_exists,
                index=False,
                chunksize=500,  # Batch insert for memory efficiency
                method="multi"
            )
            logger.info(f"Successfully loaded {len(df)} row(s) into '{table_name}'.")

        except SQLAlchemyError as e:
            logger.error(f"Failed to load data into table '{table_name}': {e}")
            raise

    def load_star_schema(self, tables_dict: dict, if_exists: str = "append") -> None:
        """
        Loads all Star Schema tables in corzrect dependency order:
        1. Dimension Tables (dim_customers, dim_products)
        2. Fact Table (fact_sales)
        """
        # Order matters due to foreign key constraints
        load_order = ["dim_customers", "dim_products", "fact_sales"]

        logger.info("Starting batch load for Star Schema tables...")
        for table_name in load_order:
            if table_name in tables_dict:
                self.load_table(tables_dict[table_name], table_name, if_exists=if_exists)
            else:
                logger.warning(f"Table '{table_name}' missing from payload dictionary.")
                
        logger.info("Star Schema loading process finished.")


# Quick test execution
if __name__ == "__main__":
    loader = DatabaseLoader()
    loader.initialize_schema()