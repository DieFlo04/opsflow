import os

from dotenv import load_dotenv
from fastapi.testclient import TestClient

from backend.app.main import app


load_dotenv()

client = TestClient(app)


# ============================================================
# TEST DATA
# ============================================================

TEST_EMAIL = os.getenv("TEST_EMAIL")
TEST_PASSWORD = os.getenv("TEST_PASSWORD")


# ============================================================
# HELPER
# ============================================================

def login():
    """
    Performs a login using the test credentials
    and returns the JWT access token.
    """

    response = client.post(
        "/api/auth/login",
        data={
            "username": TEST_EMAIL,
            "password": TEST_PASSWORD
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert "access_token" in data
    assert data["token_type"] == "bearer"

    return data["access_token"]


# ============================================================
# BASIC API TEST
# ============================================================

def test_health_check():
    response = client.get("/health")

    assert response.status_code == 200

    data = response.json()

    assert data["status"] == "ok"


# ============================================================
# AUTHENTICATION TESTS
# ============================================================

def test_get_current_user_without_token():
    response = client.get("/api/auth/me")

    assert response.status_code == 401

    data = response.json()

    assert data["detail"] == "Not authenticated"


def test_login_with_invalid_password():
    response = client.post(
        "/api/auth/login",
        data={
            "username": TEST_EMAIL,
            "password": "password_incorrecto"
        }
    )

    assert response.status_code == 401

    data = response.json()

    assert data["detail"] == "Invalid email or password"


def test_login_with_nonexistent_user():
    response = client.post(
        "/api/auth/login",
        data={
            "username": "usuario_que_no_existe@opsflow.com",
            "password": "password_incorrecto"
        }
    )

    assert response.status_code == 401

    data = response.json()

    assert data["detail"] == "Invalid email or password"


def test_login_success():
    response = client.post(
        "/api/auth/login",
        data={
            "username": TEST_EMAIL,
            "password": TEST_PASSWORD
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert "access_token" in data
    assert data["token_type"] == "bearer"


def test_get_current_user_with_token():
    token = login()

    response = client.get(
        "/api/auth/me",
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert "id" in data
    assert "name" in data
    assert "email" in data
    assert "role" in data


# ============================================================
# RBAC - AUTHENTICATION REQUIRED
# ============================================================

def test_get_users_without_token():
    response = client.get("/api/users")

    assert response.status_code == 401

    data = response.json()

    assert data["detail"] == "Not authenticated"


def test_get_incidents_without_token():
    response = client.get("/api/incidents")

    assert response.status_code == 401

    data = response.json()

    assert data["detail"] == "Not authenticated"


def test_get_systems_without_token():
    response = client.get("/api/systems")

    assert response.status_code == 401

    data = response.json()

    assert data["detail"] == "Not authenticated"


def test_get_categories_without_token():
    response = client.get("/api/categories")

    assert response.status_code == 401

    data = response.json()

    assert data["detail"] == "Not authenticated"


def test_get_comments_without_token():
    response = client.get("/api/comments")

    assert response.status_code == 401

    data = response.json()

    assert data["detail"] == "Not authenticated"