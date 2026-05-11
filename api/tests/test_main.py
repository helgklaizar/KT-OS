import pytest
from fastapi.testclient import TestClient
from main import app, init_db
import sqlite3
import os

# Override DB path for testing
os.environ["DB_PATH"] = "test_dispatcher.db"

client = TestClient(app)

@pytest.fixture(autouse=True)
def setup_database():
    # Setup
    if os.path.exists("test_dispatcher.db"):
        os.remove("test_dispatcher.db")
    
    # Overwrite DB_PATH in main
    import main
    main.DB_PATH = "test_dispatcher.db"
    main.init_db()
    
    yield
    
    # Teardown
    if os.path.exists("test_dispatcher.db"):
        os.remove("test_dispatcher.db")

def test_get_cards():
    response = client.get("/api/cards")
    assert response.status_code == 200
    cards = response.json()
    assert len(cards) >= 3  # Initial mock data should have 3 cards
    assert cards[0]["id"] == "101"

def test_update_card_status():
    response = client.put("/api/cards/105/status", json={"status": "To Do"})
    assert response.status_code == 200
    
    # Verify via GET
    get_response = client.get("/api/cards")
    cards = get_response.json()
    card_105 = next(c for c in cards if c["id"] == "105")
    assert card_105["status"] == "To Do"
