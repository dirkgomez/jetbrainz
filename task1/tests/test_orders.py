import pytest
from fastapi.testclient import TestClient

def test_create_order(client: TestClient):
    # Create a customer first
    customer_data = {
        "name": "Test",
        "surname": "User",
        "email": "test@example.com"
    }
    customer_response = client.post("/customers/", json=customer_data)
    customer_id = customer_response.json()["id"]
    
    # Create a shop item
    item_data = {
        "title": "Test Item",
        "description": "Test item description",
        "price": 99.99,
        "category_ids": []
    }
    item_response = client.post("/items/", json=item_data)
    item_id = item_response.json()["id"]
    
    # Create an order
    order_data = {
        "customer_id": customer_id,
        "items": [
            {"shop_item_id": item_id, "quantity": 2}
        ]
    }
    response = client.post("/orders/", json=order_data)
    assert response.status_code == 200
    data = response.json()
    assert data["customer_id"] == customer_id
    assert len(data["items"]) == 1
    assert data["items"][0]["shop_item_id"] == item_id
    assert data["items"][0]["quantity"] == 2
    assert "id" in data

def test_create_order_customer_not_found(client: TestClient):
    order_data = {
        "customer_id": 999,
        "items": []
    }
    response = client.post("/orders/", json=order_data)
    assert response.status_code == 404
    assert "Customer not found" in response.json()["detail"]

def test_create_order_item_not_found(client: TestClient):
    # Create a customer first
    customer_data = {
        "name": "Test",
        "surname": "User",
        "email": "test@example.com"
    }
    customer_response = client.post("/customers/", json=customer_data)
    customer_id = customer_response.json()["id"]
    
    order_data = {
        "customer_id": customer_id,
        "items": [
            {"shop_item_id": 999, "quantity": 1}
        ]
    }
    response = client.post("/orders/", json=order_data)
    assert response.status_code == 404
    assert "Shop item 999 not found" in response.json()["detail"]

def test_read_orders(client: TestClient):
    # Create a customer and item first
    customer_data = {
        "name": "Test",
        "surname": "User",
        "email": "test@example.com"
    }
    customer_response = client.post("/customers/", json=customer_data)
    customer_id = customer_response.json()["id"]
    
    item_data = {
        "title": "Test Item",
        "description": "Test item description",
        "price": 99.99,
        "category_ids": []
    }
    item_response = client.post("/items/", json=item_data)
    item_id = item_response.json()["id"]
    
    order_data = {
        "customer_id": customer_id,
        "items": [
            {"shop_item_id": item_id, "quantity": 1}
        ]
    }
    client.post("/orders/", json=order_data)
    
    response = client.get("/orders/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 1
    assert data[0]["customer_id"] == customer_id

def test_read_order(client: TestClient):
    # Create a customer and item first
    customer_data = {
        "name": "Test",
        "surname": "User",
        "email": "test@example.com"
    }
    customer_response = client.post("/customers/", json=customer_data)
    customer_id = customer_response.json()["id"]
    
    item_data = {
        "title": "Test Item",
        "description": "Test item description",
        "price": 99.99,
        "category_ids": []
    }
    item_response = client.post("/items/", json=item_data)
    item_id = item_response.json()["id"]
    
    order_data = {
        "customer_id": customer_id,
        "items": [
            {"shop_item_id": item_id, "quantity": 1}
        ]
    }
    create_response = client.post("/orders/", json=order_data)
    order_id = create_response.json()["id"]
    
    response = client.get(f"/orders/{order_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["customer_id"] == customer_id
    assert data["id"] == order_id

def test_read_order_not_found(client: TestClient):
    response = client.get("/orders/999")
    assert response.status_code == 404
    assert "Order not found" in response.json()["detail"]

def test_update_order(client: TestClient):
    # Create customers and items
    customer_data = {
        "name": "Test",
        "surname": "User",
        "email": "test@example.com"
    }
    customer_response = client.post("/customers/", json=customer_data)
    customer_id = customer_response.json()["id"]
    
    customer_data2 = {
        "name": "Test2",
        "surname": "User2",
        "email": "test2@example.com"
    }
    customer_response2 = client.post("/customers/", json=customer_data2)
    customer_id2 = customer_response2.json()["id"]
    
    item_data = {
        "title": "Test Item",
        "description": "Test item description",
        "price": 99.99,
        "category_ids": []
    }
    item_response = client.post("/items/", json=item_data)
    item_id = item_response.json()["id"]
    
    # Create order
    order_data = {
        "customer_id": customer_id,
        "items": [
            {"shop_item_id": item_id, "quantity": 1}
        ]
    }
    create_response = client.post("/orders/", json=order_data)
    order_id = create_response.json()["id"]
    
    # Update order
    updated_data = {
        "customer_id": customer_id2,
        "items": [
            {"shop_item_id": item_id, "quantity": 3}
        ]
    }
    response = client.put(f"/orders/{order_id}", json=updated_data)
    assert response.status_code == 200
    data = response.json()
    assert data["customer_id"] == customer_id2
    assert data["items"][0]["quantity"] == 3

def test_update_order_not_found(client: TestClient):
    updated_data = {
        "customer_id": 1,
        "items": []
    }
    response = client.put("/orders/999", json=updated_data)
    assert response.status_code == 404
    assert "Customer not found" in response.json()["detail"]

def test_delete_order(client: TestClient):
    # Create a customer and item first
    customer_data = {
        "name": "Test",
        "surname": "User",
        "email": "test@example.com"
    }
    customer_response = client.post("/customers/", json=customer_data)
    customer_id = customer_response.json()["id"]
    
    item_data = {
        "title": "Test Item",
        "description": "Test item description",
        "price": 99.99,
        "category_ids": []
    }
    item_response = client.post("/items/", json=item_data)
    item_id = item_response.json()["id"]
    
    order_data = {
        "customer_id": customer_id,
        "items": [
            {"shop_item_id": item_id, "quantity": 1}
        ]
    }
    create_response = client.post("/orders/", json=order_data)
    order_id = create_response.json()["id"]
    
    # Delete the order
    response = client.delete(f"/orders/{order_id}")
    assert response.status_code == 200
    
    # Verify order is deleted
    response = client.get(f"/orders/{order_id}")
    assert response.status_code == 404

def test_delete_order_not_found(client: TestClient):
    response = client.delete("/orders/999")
    assert response.status_code == 404
    assert "Order not found" in response.json()["detail"]
