import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_create_contact():
    response = client.post(
        "/contacts/",
        json={"first_name": "John", "last_name": "Doe", "email": "john@example.com", "phone": "1234567890"},
        headers={"Authorization": "Bearer testtoken"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["first_name"] == "John"
    assert data["last_name"] == "Doe"
    assert data["email"] == "john@example.com"
