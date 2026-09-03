from uuid import uuid4

from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_get_profile():
    email = f"profile_{uuid4().hex[:8]}@example.com"
    password = "Test@12345"

    register_payload = {
        "full_name": "Profile Test User",
        "email": email,
        "password": password,
        "role": "customer",
    }

    register_response = client.post(
        "/auth/register",
        json=register_payload,
    )

    assert register_response.status_code == 201

    login_response = client.post(
        "/auth/login",
        json={
            "email": email,
            "password": password,
        },
    )

    assert login_response.status_code == 200

    token_data = login_response.json()

    assert "access_token" in token_data

    access_token = token_data["access_token"]

    profile_response = client.get(
        "/auth/profile",
        headers={
            "Authorization": f"Bearer {access_token}",
        },
    )

    assert profile_response.status_code == 200

    profile = profile_response.json()

    assert profile["email"] == email
    assert profile["full_name"] == "Profile Test User"
    assert profile["role"] == "customer"
    assert profile["is_active"] is True


def test_profile_without_token():
    response = client.get("/auth/profile")

    assert response.status_code in {401, 403}