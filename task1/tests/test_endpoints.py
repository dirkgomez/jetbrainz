import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_list_customers():
    r = client.get("/customers/")
    assert r.status_code == 200
    assert isinstance(r.json(), list)
    assert len(r.json()) >= 1

def test_create_customer():
    data = {"name": "Test", "surname": "User", "email": "testuser@example.com"}
    r = client.post("/customers/", json=data)
    assert r.status_code
    assert r.json()["email"] == data["email"]

def test_get_customer():
    r = client.get("/customers/1")
    assert r.status_code == 200
    assert "email" in r.json()

def test_update_customer():
    data = {"name": "Updated", "surname": "User", "email": "updated@example.com"}
    r = client.put("/customers/1", json=data)
    assert r.status_code == 200
    assert r.json()["name"] == "Updated"

def test_delete_customer():
    data = {"name": "Delete", "surname": "Me", "email": "deleteme@example.com"}
    r = client.post("/customers/", json=data)
    cid = r.json()["id"]
    r = client.delete(f"/customers/{cid}")
    assert r.status_code == 200
    r = client.get(f"/customers/{cid}")
    assert r.status_code == 404

def test_list_categories():
    r = client.get("/categories/")
    assert r.status_code == 200
    assert isinstance(r.json(), list)


def test_create_category():
    data = {"title": "TestCat", "description": "desc"}
    r = client.post("/categories/", json=data)
    assert r.status_code == 200
    assert r.json()["title"] == "TestCat"

def test_get_category():
    r = client.get("/categories/1")
    assert r.status_code == 200
    assert "title" in r.json()

def test_update_category():
    data = {"title": "UpdatedCat", "description": "desc2"}
    r = client.put("/categories/1", json=data)
    assert r.status_code == 200
    assert r.json()["title"] == "UpdatedCat"

def test_delete_category():
    data = {"title": "DeleteCat", "description": "desc"}
    r = client.post("/categories/", json=data)
    cid = r.json()["id"]
    r = client.delete(f"/categories/{cid}")
    assert r.status_code == 200
    r = client.get(f"/categories/{cid}")
    assert r.status_code == 404

def test_list_shop_items():
    r = client.get("/shop_items/")
    assert r.status_code == 200
    assert isinstance(r.json(), list)

def test_create_shop_item():
    # Use existing category id 1
    data = {"title": "TestItem", "description": "desc", "price": 10.0, "category_ids": [1]}
    r = client.post("/shop_items/", json=data)
    assert r.status_code == 200
    assert r.json()["title"] == "TestItem"

def test_get_shop_item():
    r = client.get("/shop_items/1")
    assert r.status_code == 200
    assert "title" in r.json()

def test_update_shop_item():
    data = {"title": "UpdatedItem", "description": "desc2", "price": 20.0, "category_ids": [1]}
    r = client.put("/shop_items/1", json=data)
    assert r.status_code == 200
    assert r.json()["title"] == "UpdatedItem"

def test_delete_shop_item():
    data = {"title": "DeleteItem", "description": "desc", "price": 5.0, "category_ids": [1]}
    r = client.post("/shop_items/", json=data)
    iid = r.json()["id"]
    r = client.delete(f"/shop_items/{iid}")
    assert r.status_code == 200
    r = client.get(f"/shop_items/{iid}")
    assert r.status_code == 404

def test_list_order_items():
    r = client.get("/order_items/")
    assert r.status_code == 200
    assert isinstance(r.json(), list)

def test_create_order_item():
    # Use existing shop_item_id 1
    data = {"shop_item_id": 1, "quantity": 3}
    r = client.post("/order_items/", json=data)
    assert r.status_code == 200
    assert r.json()["quantity"] == 3

def test_get_order_item():
    r = client.get("/order_items/1")
    assert r.status_code == 200
    assert "quantity" in r.json()

def test_update_order_item():
    data = {"shop_item_id": 1, "quantity": 5}
    r = client.put("/order_items/1", json=data)
    assert r.status_code == 200
    assert r.json()["quantity"] == 5

def test_delete_order_item():
    data = {"shop_item_id": 1, "quantity": 7}
    r = client.post("/order_items/", json=data)
    oid = r.json()["id"]
    r = client.delete(f"/order_items/{oid}")
    assert r.status_code == 200
    r = client.get(f"/order_items/{oid}")
    assert r.status_code == 404

def test_list_orders():
    r = client.get("/orders/")
    assert r.status_code == 200
    assert isinstance(r.json(), list)

def test_create_order():
    # Use existing customer_id 1 and order_item_id 1
    data = {"customer_id": 1, "item_ids": [1]}
    r = client.post("/orders/", json=data)
    assert r.status_code == 200
    assert r.json()["customer"]["id"] == 1

def test_get_order():
    r = client.get("/orders/1")
    assert r.status_code == 200
    assert "customer" in r.json()

def test_update_order():
    data = {"customer_id": 1, "item_ids": [1]}
    r = client.put("/orders/1", json=data)
    assert r.status_code == 200
    assert r.json()["customer"]["id"] == 1

def test_delete_order():
    # Create order to delete
    data = {"customer_id": 1, "item_ids": [1]}
    r = client.post("/orders/", json=data)
    oid = r.json()["id"]
    r = client.delete(f"/orders/{oid}")
    assert r.status_code == 200
    r = client.get(f"/orders/{oid}")
    assert r.status_code == 404