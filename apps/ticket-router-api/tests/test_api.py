import pytest
from fastapi.testclient import TestClient
import sys
import os

# Ensure src module can be imported
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.api.main import app, load_ml_models

# We need to manually call the startup event since TestClient doesn't run startup events automatically in this configuration
load_ml_models()
client = TestClient(app)

def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"status": "online", "model": "CatBoost TF-IDF Routing Engine"}

def test_predict_refund():
    response = client.post(
        "/predict",
        json={"text": "I want my money back immediately!"}
    )
    assert response.status_code == 200
    data = response.json()
    assert "department" in data
    assert "confidence" in data
    assert data["department"] == "REFUND"
    assert data["confidence"] > 0.5

def test_predict_delivery():
    response = client.post(
        "/predict",
        json={"text": "Where is my package? It was supposed to arrive yesterday."}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["department"] == "DELIVERY"
