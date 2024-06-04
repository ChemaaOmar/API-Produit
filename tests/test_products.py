# tests/test_products.py

import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

@pytest.fixture(scope='module')
def test_client():
    with TestClient(app) as c:
        yield c

def test_create_product(test_client):
    response = test_client.post(
        "/products/",
        json={"name": "Test Product", "description": "Test Description", "price": 10.0, "stock": 100},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Test Product"
    assert data["description"] == "Test Description"
    assert data["price"] == 10.0
    assert data["stock"] == 100
    assert "id" in data

def test_read_product(test_client):
    response = test_client.get("/products/1")
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Test Product"
    assert data["description"] == "Test Description"
    assert data["price"] == 10.0
    assert data["stock"] == 100
    assert "id" in data

def test_read_products(test_client):
    response = test_client.get("/products/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) > 0

def test_delete_product(test_client):
    response = test_client.delete("/products/1")
    assert response.status_code == 200
