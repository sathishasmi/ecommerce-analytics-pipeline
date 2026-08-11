import pandas as pd
from src.utils.logger import setup_logger

logger = setup_logger()


def flatten_json_data(raw_json: list) -> pd.DataFrame:
    """
    Flatten the DummyJSON carts API response.

    Each product inside a cart becomes one row.

    Input:
    [
        {
            "id": 1,
            "userId": 33,
            "products": [...],
            "total": 168,
            ...
        }
    ]

    Output:
        DataFrame with one row per purchased product.
    """

    logger.info("Flattening nested JSON payload...")

    records = []

    for cart in raw_json:
        cart_id = cart.get("id")
        user_id = cart.get("userId")
        cart_total = cart.get("total")
        discounted_total = cart.get("discountedTotal")
        total_products = cart.get("totalProducts")
        total_quantity = cart.get("totalQuantity")

        for product in cart.get("products", []):

            records.append({
                "order_id": cart_id,
                "user_id": user_id,

                "product_id": product.get("id"),
                "title": product.get("title"),
                "price": product.get("price"),
                "quantity": product.get("quantity"),
                "total": product.get("total"),
                "discount_percentage": product.get("discountPercentage"),
                
                "cart_total": cart_total,
                "discounted_total": discounted_total,
                "total_products": total_products,
                "total_quantity": total_quantity
            })

    df_flat = pd.DataFrame(records)

    logger.info(f"Flattened DataFrame shape: {df_flat.shape}")

    # Debugging
    print("\nColumns:")
    print(df_flat.columns.tolist())

    print("\nNull values:")
    print(df_flat.isnull().sum())

    return df_flat

