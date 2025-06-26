import pytest
from fastapi.testclient import TestClient

def test_create_category(client: TestClient):
    category_data = {
        "title": "Test Category",
        "description": "Test category description"
    }
    response = client.post("/categories/", json=category_data)
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == category_data["title"]
    assert data["description"] == category_data["description"]
    assert "id" in data

def test_read_categories(client: TestClient):
    # Create a category first
    category_data = {
        "title": "Test Category",
        "description": "Test category description"
    }
    client.post("/categories/", json=category_data)
    
    response = client.get("/categories/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 1
    assert data[0]["title"] == category_data["title"]

def test_read_category(client: TestClient):
    # Create a category first
    category_data = {
        "title": "Test Category",
        "description": "Test category description"
    }
    create_response = client.post("/categories/", json=category_data)
    category_id = create_response.json()["id"]
    
    response = client.get(f"/categories/{category_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == category_data["title"]
    assert data["id"] == category_id

def test_read_category_not_found(client: TestClient):
    response = client.get("/categories/999")
    assert response.status_code == 404
    assert "Category not found" in response.json()["detail"]

def test_update_category(client: TestClient):
    # Create a category first
    category_data = {
        "title": "Test Category",
        "description": "Test category description"
    }
    create_response = client.post("/categories/", json=category_data)
    category_id = create_response.json()["id"]
    
    # Update the category
    updated_data = {
        "title": "Updated Category",
        "description": "Updated description"
    }
    response = client.put(f"/categories/{category_id}", json=updated_data)
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == updated_data["title"]
    assert data["description"] == updated_data["description"]

def test_update_category_not_found(client: TestClient):
    updated_data = {
        "title": "Updated Category",
        "description": "Updated description"
    }
    response = client.put("/categories/999", json=updated_data)
    assert response.status_code == 404
    assert "Category not found" in response.json()["detail"]

def test_delete_category(client: TestClient):
    # Create a category first
    category_data = {
        "title": "Test Category",
        "description": "Test category description"
    }
    create_response = client.post("/categories/", json=category_data)
    category_id = create_response.json()["id"]
    
    # Delete the category
    response = client.delete(f"/categories/{category_id}")
    assert response.status_code == 200
    
    # Verify category is deleted
    response = client.get(f"/categories/{category_id}")
    assert response.status_code == 404

def test_delete_category_not_found(client: TestClient):
    response = client.delete("/categories/999")
    assert response.status_code == 404
    assert "Category not found" in response.json()["detail"]
