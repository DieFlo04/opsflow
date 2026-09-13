import uuid
import jwt

from fastapi.testclient import TestClient

from backend.app.main import app
from backend.app.core.security import SECRET_KEY, ALGORITHM


client = TestClient(app)


# ============================================================
# TEST USERS
# ============================================================

EMPLOYEE_ID = 3
TECHNICIAN_ID = 1

# Este es el usuario que acabamos de crear
ADMIN_ID = 6


# ============================================================
# HELPER
# ============================================================

def create_test_token(user_id: int, role: str):
    """
    Creates a JWT for testing purposes.
    """

    payload = {
        "sub": str(user_id),
        "role": role
    }

    return jwt.encode(
        payload,
        SECRET_KEY,
        algorithm=ALGORITHM
    )


def auth_headers(user_id: int, role: str):
    """
    Returns Authorization headers with a test JWT.
    """

    token = create_test_token(user_id, role)

    return {
        "Authorization": f"Bearer {token}"
    }


# ============================================================
# AUTHENTICATED ACCESS
# ============================================================

def test_employee_can_get_users():
    response = client.get(
        "/api/users",
        headers=auth_headers(EMPLOYEE_ID, "employee")
    )

    assert response.status_code == 200


def test_technician_can_get_users():
    response = client.get(
        "/api/users",
        headers=auth_headers(TECHNICIAN_ID, "technician")
    )

    assert response.status_code == 200


def test_admin_can_get_users():
    response = client.get(
        "/api/users",
        headers=auth_headers(ADMIN_ID, "admin")
    )

    assert response.status_code == 200


# ============================================================
# EMPLOYEE PERMISSIONS
# ============================================================

def test_employee_cannot_create_user():
    response = client.post(
        "/api/users",
        headers=auth_headers(EMPLOYEE_ID, "employee"),
        json={
            "name": "RBAC Employee Test",
            "email": "rbac_employee_test@example.com",
            "password": "TestPassword123!"
        }
    )

    assert response.status_code == 403

    data = response.json()

    assert data["detail"] == "Insufficient permissions"


def test_employee_cannot_create_system():
    response = client.post(
        "/api/systems",
        headers=auth_headers(EMPLOYEE_ID, "employee"),
        json={
            "name": "RBAC Employee System",
            "description": "RBAC test system",
            "status": "ACTIVE"
        }
    )

    assert response.status_code == 403

    data = response.json()

    assert data["detail"] == "Insufficient permissions"


def test_employee_cannot_create_category():
    response = client.post(
        "/api/categories",
        headers=auth_headers(EMPLOYEE_ID, "employee"),
        json={
            "name": "RBAC_EMPLOYEE_CATEGORY"
        }
    )

    assert response.status_code == 403

    data = response.json()

    assert data["detail"] == "Insufficient permissions"


def test_employee_cannot_delete_comment():
    response = client.delete(
        "/api/comments/999999",
        headers=auth_headers(EMPLOYEE_ID, "employee")
    )

    assert response.status_code == 403

    data = response.json()

    assert data["detail"] == "Insufficient permissions"


# ============================================================
# TECHNICIAN PERMISSIONS
# ============================================================

def test_technician_can_get_incidents():
    response = client.get(
        "/api/incidents",
        headers=auth_headers(TECHNICIAN_ID, "technician")
    )

    assert response.status_code == 200


def test_technician_can_get_comments():
    response = client.get(
        "/api/comments",
        headers=auth_headers(TECHNICIAN_ID, "technician")
    )

    assert response.status_code == 200


def test_technician_cannot_create_user():
    response = client.post(
        "/api/users",
        headers=auth_headers(TECHNICIAN_ID, "technician"),
        json={
            "name": "RBAC Technician Test",
            "email": "rbac_technician_test@example.com",
            "password": "TestPassword123!"
        }
    )

    assert response.status_code == 403

    data = response.json()

    assert data["detail"] == "Insufficient permissions"


def test_technician_cannot_create_system():
    response = client.post(
        "/api/systems",
        headers=auth_headers(TECHNICIAN_ID, "technician"),
        json={
            "name": "RBAC Technician System",
            "description": "RBAC test system",
            "status": "ACTIVE"
        }
    )

    assert response.status_code == 403

    data = response.json()

    assert data["detail"] == "Insufficient permissions"


def test_technician_cannot_delete_incident():
    response = client.delete(
        "/api/incidents/999999",
        headers=auth_headers(TECHNICIAN_ID, "technician")
    )

    assert response.status_code == 403

    data = response.json()

    assert data["detail"] == "Insufficient permissions"


# ============================================================
# ADMIN PERMISSIONS
# ============================================================

def test_admin_can_get_users():
    response = client.get(
        "/api/users",
        headers=auth_headers(ADMIN_ID, "admin")
    )

    assert response.status_code == 200


def test_admin_can_get_systems():
    response = client.get(
        "/api/systems",
        headers=auth_headers(ADMIN_ID, "admin")
    )

    assert response.status_code == 200


def test_admin_can_get_categories():
    response = client.get(
        "/api/categories",
        headers=auth_headers(ADMIN_ID, "admin")
    )

    assert response.status_code == 200


def test_admin_can_get_incidents():
    response = client.get(
        "/api/incidents",
        headers=auth_headers(ADMIN_ID, "admin")
    )

    assert response.status_code == 200


def test_admin_can_get_comments():
    response = client.get(
        "/api/comments",
        headers=auth_headers(ADMIN_ID, "admin")
    )

    assert response.status_code == 200


# ============================================================
# ADMIN-ONLY ENDPOINTS
# ============================================================

def test_admin_can_create_system():
    unique_name = f"RBAC Admin Test System {uuid.uuid4().hex[:8]}"

    response = client.post(
        "/api/systems",
        headers=auth_headers(ADMIN_ID, "admin"),
        json={
            "name": unique_name,
            "description": "System created during RBAC testing",
            "status": "ACTIVE"
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert data["name"] == unique_name

def test_admin_can_create_category():
    unique_name = f"RBAC_ADMIN_CATEGORY_{uuid.uuid4().hex[:8]}"

    response = client.post(
        "/api/categories",
        headers=auth_headers(ADMIN_ID, "admin"),
        json={
            "name": unique_name
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert data["name"] == unique_name

# ============================================================
# AUTHENTICATION REQUIRED
# ============================================================

def test_users_without_token():
    response = client.get("/api/users")

    assert response.status_code == 401


def test_incidents_without_token():
    response = client.get("/api/incidents")

    assert response.status_code == 401


def test_systems_without_token():
    response = client.get("/api/systems")

    assert response.status_code == 401


def test_categories_without_token():
    response = client.get("/api/categories")

    assert response.status_code == 401


def test_comments_without_token():
    response = client.get("/api/comments")

    assert response.status_code == 401