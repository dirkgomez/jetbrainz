import pytest
from fastapi.testclient import TestClient

def test_create_shop_item(client: TestClient):
    # Create a category first
    category_data = {
        "title": "Test Category",
        "description": "Test category description"
    }
    category_response = client.post("/categories/", json=category_data)
    category_id = category_response.json()["id"]
    
    item_data = {
        "title": "Test Item",
        "description": "Test item description",
        "price": 99.99,
        "category_ids": [category_id]
    }
    response = client.post("/items/", json=item_data)
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == item_data["title"]
    assert data["description"] == item_data["description"]
    assert data["price"] == item_data["price"]
    assert len(data["categories"]) == 1
    assert data["categories"][0]["id"] == category_id
    assert "id" in data

def test_create_shop_item_without_categories(client: TestClient):
    item_data = {
        "title": "Test Item",
        "description": "Test item description",
        "price": 99.99,
        "category_ids": []
    }
    response = client.post("/items/", json=item_data)
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == item_data["title"]
    assert len(data["categories"]) == 0

def test_read_shop_items(client: TestClient):
    # Create an item first
    item_data = {
        "title": "Test Item",
        "description": "Test item description",
        "price": 99.99,
        "category_ids": []
    }
    client.post("/items/", json=item_data)
    
    response = client.get("/items/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 1
    assert data[0]["title"] == item_data["title"]

def test_read_shop_item(client: TestClient):
    # Create an item first
    item_data = {
        "title": "Test Item",
        "description": "Test item description",
        "price": 99.99,
        "category_ids": []
    }
    create_response = client.post("/items/", json=item_data)
    item_id = create_response.json()["id"]
    
    response = client.get(f"/items/{item_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == item_data["title"]
    assert data["id"] == item_id

def test_read_shop_item_not_found(client: TestClient):
    response = client.get("/items/999")
    assert response.status_code == 404
    assert "Shop item not found" in response.json()["detail"]

def test_update_shop_item(client: TestClient):
    # Create a category and item first
    category_data = {
        "title": "Test Category",
        "description": "Test category description"
    }
    category_response = client.post("/categories/", json=category_data)
    category_id = category_response.json()["id"]
    
    item_data = {
        "title": "Test Item",
        "description": "Test item description",
        "price": 99.99,
        "category_ids": []
    }
    create_response = client.post("/items/", json=item_data)
    item_id = create_response.json()["id"]
    
    # Update the item
    updated_data = {
        "title": "Updated Item",
        "description": "Updated description",
        "price": 149.99,
        "category_ids": [category_id]
    }
    response = client.put(f"/items/{item_id}", json=updated_data)
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == updated_data["title"]
    assert data["price"] == updated_data["price"]
    assert len(data["categories"]) == 1

def test_update_shop_item_not_found(client: TestClient):
    updated_data = {
        "title": "Updated Item",
        "description": "Updated description",
        "price": 149.99,
        "category_ids": []
    }
    response = client.put("/items/999", json=updated_data)
    assert response.status_code == 404
    assert "Shop item not found" in response.json()["detail"]

def test_delete_shop_item(client: TestClient):
    # Create an item first
    item_data = {
        "title": "Test Item",
        "description": "Test item description",
        "price": 99.99,
        "category_ids": []
    }
    create_response = client.post("/items/", json=item_data)
    item_id = create_response.json()["id"]
    
    # Delete the item
    response = client.delete(f"/items/{item_id}")
    assert response.status_code == 200
    
    # Verify item is deleted
    response = client.get(f"/items/{item_id}")
    assert response.status_code == 404

def test_delete_shop_item_not_found(client: TestClient):
    response = client.delete("/items/999")
    assert response.status_code == 404
    assert "Shop item not found" in response.json()["detail"]
