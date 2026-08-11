from unittest.mock import patch
from src.extract.api_client import (
    fetch_raw_api_data,
    fetch_users_data,
    fetch_products_data,
)


@patch("src.extract.api_client.requests.get")
def test_fetch_raw_api_data(mock_get):
    mock_get.return_value.status_code = 200
    mock_get.return_value.raise_for_status.return_value = None
    mock_get.return_value.json.return_value = {
        "carts": [
            {"id": 1}
        ]
    }

    data = fetch_raw_api_data()

    assert isinstance(data, dict)
    assert "carts" in data
    assert data["carts"][0]["id"] == 1


@patch("src.extract.api_client.requests.get")
def test_fetch_users_data(mock_get):
    mock_get.return_value.status_code = 200
    mock_get.return_value.raise_for_status.return_value = None
    mock_get.return_value.json.return_value = {
        "users": [
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
    }

    users = fetch_users_data()

    assert isinstance(users, list)
    assert len(users) == 1
    assert users[0]["firstName"] == "John"


@patch("src.extract.api_client.requests.get")
def test_fetch_products_data(mock_get):
    mock_get.return_value.status_code = 200
    mock_get.return_value.raise_for_status.return_value = None
    mock_get.return_value.json.return_value = {
        "products": [
            {
                "id": 1,
                "title": "iPhone",
                "category": "phones",
                "price": 999
            }
        ]
    }

    products = fetch_products_data()

    assert isinstance(products, list)
    assert len(products) == 1
    assert products[0]["title"] == "iPhone"