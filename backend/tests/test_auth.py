"""Tests for registration, login, and the /me endpoint."""


def test_register_new_user(client):
    response = client.post(
        "/api/v1/register",
        json={"email": "newuser@example.com", "full_name": "New User", "password": "supersecret123"},
    )
    assert response.status_code == 201
    body = response.json()
    assert "access_token" in body
    assert body["token_type"] == "bearer"


def test_register_duplicate_email_fails(client):
    payload = {"email": "dupe@example.com", "full_name": "Dupe User", "password": "supersecret123"}
    client.post("/api/v1/register", json=payload)
    response = client.post("/api/v1/register", json=payload)
    assert response.status_code == 409


def test_login_with_valid_credentials(client):
    client.post(
        "/api/v1/register",
        json={"email": "login@example.com", "full_name": "Login User", "password": "supersecret123"},
    )
    response = client.post(
        "/api/v1/login", json={"email": "login@example.com", "password": "supersecret123"}
    )
    assert response.status_code == 200
    assert "access_token" in response.json()


def test_login_with_invalid_password_fails(client):
    client.post(
        "/api/v1/register",
        json={"email": "wrongpass@example.com", "full_name": "User", "password": "supersecret123"},
    )
    response = client.post(
        "/api/v1/login", json={"email": "wrongpass@example.com", "password": "incorrect"}
    )
    assert response.status_code == 401


def test_me_requires_authentication(client):
    response = client.get("/api/v1/me")
    assert response.status_code == 401


def test_me_returns_current_user(client, auth_headers):
    response = client.get("/api/v1/me", headers=auth_headers)
    assert response.status_code == 200
    assert response.json()["email"] == "doctor@example.com"
