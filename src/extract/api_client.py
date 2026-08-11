import os
import requests
from src.utils.logger import setup_logger

logger = setup_logger()

DEFAULT_API_URL = "https://dummyjson.com/carts"

def fetch_raw_api_data(endpoint_url: str = DEFAULT_API_URL) -> dict:
    """
    Sends an HTTP GET request to the specified API endpoint.
    
    Returns:
        dict/list: Raw JSON payload returned by the API.
    Raises:
        requests.exceptions.RequestException: If the HTTP request fails.
    """
    try:
        logger.info(f"Extracting data from API endpoint: {endpoint_url}")
        
        # Send HTTP GET request with a 10-second timeout
        response = requests.get(endpoint_url, timeout=10)
        
        # Raise an exception if the response status is 4xx or 5xx (e.g., 404, 500)
        response.raise_for_status()
        
        raw_data = response.json()
        logger.info(f"Successfully extracted raw payload from API.")
        return raw_data

    except requests.exceptions.Timeout:
        logger.error(f"API request timed out while connecting to {endpoint_url}")
        raise
    except requests.exceptions.HTTPError as http_err:
        logger.error(f"HTTP error occurred: {http_err} - Status Code: {response.status_code}")
        raise
    except requests.exceptions.RequestException as req_err:
        logger.error(f"Failed to fetch data from API: {req_err}")
        raise

def fetch_users_data() -> list:
    """
    Fetch customer information from DummyJSON users API.
    """

    users_url = "https://dummyjson.com/users"

    try:
        logger.info("Fetching customer data...")

        response = requests.get(users_url, timeout=10)
        response.raise_for_status()

        users = response.json()["users"]

        logger.info(f"Fetched {len(users)} users successfully.")

        return users

    except requests.exceptions.RequestException as e:
        logger.error(f"Failed to fetch users: {e}")
        raise

def fetch_products_data() -> list:
    """
    Fetch product information from DummyJSON products API.
    """

    products_url = "https://dummyjson.com/products?limit=200"

    try:
        logger.info("Fetching product data...")

        response = requests.get(products_url, timeout=10)
        response.raise_for_status()

        products = response.json()["products"]

        logger.info(f"Fetched {len(products)} products successfully.")

        return products

    except requests.exceptions.RequestException as e:
        logger.error(f"Failed to fetch products: {e}")
        raise