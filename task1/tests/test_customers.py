import pytest
from fastapi.testclient import TestClient

def test_create_customer(client: TestClient):
    customer_data = {
        "name": "Test",
        "surname": "User",
        "email": "test@example.com"
    }
    response = client.post("/customers/", json=customer_data)
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == customer_data["name"]
    assert data["surname"] == customer_data["surname"]
    assert data["email"] == customer_data["email"]
    assert "id" in data

def test_create_customer_duplicate_email(client: TestClient):
    customer_data = {
        "name": "Test",
        "surname": "User",
        "email": "test@example.com"
    }
    # Create first customer
    response = client.post("/customers/", json=customer_data)
    assert response.status_code == 200
    
    # Try to create customer with same email
    response = client.post("/customers/", json=customer_data)
    assert response.status_code == 400
    assert "Email already registered" in response.json()["detail"]

def test_read_customers(client: TestClient):
    # Create a customer first
    customer_data = {
        "name": "Test",
        "surname": "User",
        "email": "test@example.com"
    }
    client.post("/customers/", json=customer_data)
    
    response = client.get("/customers/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 1
    assert data[0]["name"] == customer_data["name"]

def test_read_customer(client: TestClient):
    # Create a customer first
    customer_data = {
        "name": "Test",
        "surname": "User",
        "email": "test@example.com"
    }
    create_response = client.post("/customers/", json=customer_data)
    customer_id = create_response.json()["id"]
    
    response = client.get(f"/customers/{customer_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == customer_data["name"]
    assert data["id"] == customer_id

def test_read_customer_not_found(client: TestClient):
    response = client.get("/customers/999")
    assert response.status_code == 404
    assert "Customer not found" in response.json()["detail"]

def test_update_customer(client: TestClient):
    # Create a customer first
    customer_data = {
        "name": "Test",
        "surname": "User",
        "email": "test@example.com"
    }
    create_response = client.post("/customers/", json=customer_data)
    customer_id = create_response.json()["id"]
    
    # Update the customer
    updated_data = {
        "name": "Updated",
        "surname": "User",
        "email": "updated@example.com"
    }
    response = client.put(f"/customers/{customer_id}", json=updated_data)
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == updated_data["name"]
    assert data["email"] == updated_data["email"]

def test_update_customer_not_found(client: TestClient):
    updated_data = {
        "name": "Updated",
        "surname": "User",
        "email": "updated@example.com"
    }
    response = client.put("/customers/999", json=updated_data)
    assert response.status_code == 404
    assert "Customer not found" in response.json()["detail"]

def test_delete_customer(client: TestClient):
    # Create a customer first
    customer_data = {
        "name": "Test",
        "surname": "User",
        "email": "test@example.com"
    }
    create_response = client.post("/customers/", json=customer_data)
    customer_id = create_response.json()["id"]
    
    # Delete the customer
    response = client.delete(f"/customers/{customer_id}")
    assert response.status_code == 200
    
    # Verify customer is deleted
    response = client.get(f"/customers/{customer_id}")
    assert response.status_code == 404

def test_delete_customer_not_found(client: TestClient):
    response = client.delete("/customers/999")
    assert response.status_code == 404
    assert "Customer not found" in response.json()["detail"]
