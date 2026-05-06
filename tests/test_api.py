"""Sample tests for API endpoints."""

import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


@pytest.mark.unit
def test_health_check():
    """Test health check endpoint."""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


@pytest.mark.unit
def test_root_endpoint():
    """Test root endpoint."""
    response = client.get("/")
    assert response.status_code == 200
    assert "message" in response.json()


@pytest.mark.integration
def test_register_user():
    """Test user registration."""
    response = client.post(
        "/api/v1/users/register",
        json={
            "email": "test@example.com",
            "full_name": "Test User",
            "password": "test_password_123",
        },
    )
    assert response.status_code == 201
    assert "access_token" in response.json()
    assert response.json()["token_type"] == "bearer"


@pytest.mark.integration
def test_register_duplicate_email():
    """Test registration with duplicate email."""
    email = "duplicate@example.com"
    
    # First registration should succeed
    client.post(
        "/api/v1/users/register",
        json={
            "email": email,
            "full_name": "User One",
            "password": "password123",
        },
    )
    
    # Second registration with same email should fail
    response = client.post(
        "/api/v1/users/register",
        json={
            "email": email,
            "full_name": "User Two",
            "password": "password123",
        },
    )
    assert response.status_code == 409


@pytest.mark.integration
def test_login_user():
    """Test user login."""
    email = "login_test@example.com"
    password = "secure_password_123"
    
    # Register user
    client.post(
        "/api/v1/users/register",
        json={
            "email": email,
            "full_name": "Login Test User",
            "password": password,
        },
    )
    
    # Login
    response = client.post(
        "/api/v1/users/login",
        json={"email": email, "password": password},
    )
    assert response.status_code == 200
    assert "access_token" in response.json()


@pytest.mark.integration
def test_invalid_credentials():
    """Test login with invalid credentials."""
    response = client.post(
        "/api/v1/users/login",
        json={
            "email": "nonexistent@example.com",
            "password": "wrong_password",
        },
    )
    assert response.status_code == 401
