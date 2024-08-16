from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_create_user():
    response = client.post(
        "/users/",
        json={"email": "user@example.com", "username": "user", "password": "password"},
    )
    assert response.status_code == 200
    assert response.json()["email"] == "user@example.com"
