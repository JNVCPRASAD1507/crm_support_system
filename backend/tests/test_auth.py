from uuid import uuid4

from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_register_user():
    email = f"testcustomer_{uuid4().hex[:8]}@example.com"

    payload = {
        "full_name": "Test Customer",
        "email": email,
        "password": "Test@12345",
        "role": "customer",
    }

    response = client.post(
        "/auth/register",
        json=payload,
    )

    assert response.status_code == 201

    data = response.json()

    assert data["full_name"] == "Test Customer"
    assert data["email"] == email
    assert data["role"] == "customer"
    assert "id" in data


def test_login_user():
    email = f"loginuser_{uuid4().hex[:8]}@example.com"

    register_payload = {
        "full_name": "Login Test User",
        "email": email,
        "password": "Test@12345",
        "role": "customer",
    }

    register_response = client.post(
        "/auth/register",
        json=register_payload,
    )

    assert register_response.status_code == 201

    login_payload = {
        "email": email,
        "password": "Test@12345",
    }

    response = client.post(
        "/auth/login",
        json=login_payload,
    )

    assert response.status_code == 200

    data = response.json()

    assert "access_token" in data
    assert data["token_type"] == "bearer"
    assert data["access_token"]


def test_login_with_wrong_password():
    email = f"wrongpassword_{uuid4().hex[:8]}@example.com"

    register_payload = {
        "full_name": "Wrong Password User",
        "email": email,
        "password": "Test@12345",
        "role": "customer",
    }

    register_response = client.post(
        "/auth/register",
        json=register_payload,
    )

    assert register_response.status_code == 201

    login_payload = {
        "email": email,
        "password": "WrongPassword123",
    }

    response = client.post(
        "/auth/login",
        json=login_payload,
    )

    assert response.status_code == 401