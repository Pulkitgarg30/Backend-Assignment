import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import pytest
from fastapi.testclient import TestClient
from main import app, validate_row

client = TestClient(app)

def test_validate_row_valid():
    row = {
        "sku": "TSHIRT-RED-001",
        "name": "Classic Cotton T-Shirt",
        "brand": "StreamThreads",
        "mrp": "799",
        "price": "499",
        "quantity": "20"
    }
    valid, errors = validate_row(row)
    assert valid is True
    assert errors == []

def test_validate_row_missing_fields():
    row = {
        "sku": "",
        "name": "Classic Cotton T-Shirt",
        "brand": "StreamThreads",
        "mrp": "799",
        "price": "499",
        "quantity": "20"
    }
    valid, errors = validate_row(row)
    assert valid is False
    assert "Missing sku" in errors

def test_validate_row_invalid_types():
    row = {
        "sku": "TSHIRT-RED-001",
        "name": "Classic Cotton T-Shirt",
        "brand": "StreamThreads",
        "mrp": "seven99",
        "price": "499",
        "quantity": "20"
    }
    valid, errors = validate_row(row)
    assert valid is False
    assert "mrp, price, quantity must be integers" in errors

def test_validate_row_price_greater_than_mrp():
    row = {
        "sku": "TSHIRT-RED-001",
        "name": "Classic Cotton T-Shirt",
        "brand": "StreamThreads",
        "mrp": "499",
        "price": "799",
        "quantity": "20"
    }
    valid, errors = validate_row(row)
    assert valid is False
    assert "price must be ≤ mrp" in errors

def test_validate_row_negative_quantity():
    row = {
        "sku": "TSHIRT-RED-001",
        "name": "Classic Cotton T-Shirt",
        "brand": "StreamThreads",
        "mrp": "799",
        "price": "499",
        "quantity": "-5"
    }
    valid, errors = validate_row(row)
    assert valid is False
    assert "quantity must be ≥ 0" in errors

def test_search_case_insensitive_brand(monkeypatch):
    # Mock DB query for case-insensitive brand search
    class DummyProduct:
        def __init__(self, brand):
            self.brand = brand
    class DummyQuery:
        def __init__(self, products):
            self.products = products
        def filter(self, *args, **kwargs):
            # Simulate case-insensitive filter
            self.products = [p for p in self.products if p.brand.lower() == "streamthreads".lower()]
            return self
        def all(self):
            return self.products
    monkeypatch.setattr("main.Product", DummyProduct)
    monkeypatch.setattr("main.Session", lambda: None)
    # This test is illustrative; actual DB tests should use a test DB

def test_upload_endpoint_exists():
    response = client.get("/upload")
    assert response.status_code == 405  # Method Not Allowed for GET

def test_root_endpoint():
    response = client.get("/")
    assert response.status_code == 200
    assert "Streamoid Product API" in response.json()["message"]