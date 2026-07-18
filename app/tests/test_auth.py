import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_register():
    response = client.post("/api/v1/auth/register", json={
        "email": "test@example.com",
        "username": "testuser",
        "password": "testpassword123",
        "full_name": "Test User"
    })
    assert response.status_code == 201

def test_login():
    response = client.post("/api/v1/auth/login", data={
        "username": "testuser",
        "password": "testpassword123"
    })
    assert response.status_code == 200
    assert "access_token" in response.json()
