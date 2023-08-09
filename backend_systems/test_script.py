import requests
import random

# Base URL for the API endpoints
base_url = "http://127.0.0.1:8000/"

def test_register_user():
    endpoint = "/register"
    data = {
        "username": f"test_user_{random.randint(1, 1e6)}",
        "email": "test@example.com",
        "password": "test_password",
        "full_name": "Test User",
        "age": 30,
        "gender": "male"
    }
    response = requests.post(base_url + endpoint, json=data)
    assert response.status_code == 201  # Updated status code
    assert response.json()["message"] == "User successfully registered!"

def test_generate_token():
    endpoint = "/token"
    data = {
        "username": "test_user",
        "password": "test_password"
    }
    response = requests.post(base_url + endpoint, json=data)
    assert response.status_code == 200
    assert response.json()["message"] == "Access token generated successfully."
    return {"Authorization": f"Bearer {response.json()['data']['access_token']}"}

def test_store_data(headers):
    endpoint = "/data"
    data = {
        "key": f"test_key_{random.randint(1, 1e6)}",
        "value": "test_value"
    }
    response = requests.post(base_url + endpoint, json=data, headers=headers)
    assert response.status_code == 200
    assert response.json()["message"] == "Data stored successfully."

def test_retrieve_data(headers):
    key = "test_key"  # Use a key that you stored earlier
    endpoint = f"/data/{key}"
    response = requests.get(base_url + endpoint, headers=headers)
    assert response.status_code == 200
    assert response.json()["data"]["key"] == key
    assert response.json()["data"]["value"] == "test_value"

def test_update_data(headers):
    key = "test_key"  # Use the same key as in test_retrieve_data
    endpoint = f"/data/{key}"
    data = {
        "value": "new_test_value"
    }
    response = requests.put(base_url + endpoint, json=data, headers=headers)
    assert response.status_code == 200
    assert response.json()["message"] == "Data updated successfully."

def test_delete_data(headers):
    key = "test_key"  # Use the same key as in test_retrieve_data
    endpoint = f"/data/{key}"
    response = requests.delete(base_url + endpoint, headers=headers)
    assert response.status_code == 200
    assert response.json()["message"] == "Data deleted successfully."

def test_all():
    headers = test_generate_token()
    test_register_user()
    test_store_data(headers)
    test_retrieve_data(headers)
    test_update_data(headers)
    test_delete_data(headers)

if __name__ == "__main__":
    test_all()
