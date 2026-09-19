import os

from dotenv import load_dotenv
from fastapi.testclient import TestClient

from backend.app.main import app


load_dotenv()

client = TestClient(app)

TEST_EMAIL = os.getenv("TEST_EMAIL")
TEST_PASSWORD = os.getenv("TEST_PASSWORD")


def get_token():
    response = client.post(
        "/api/auth/login",
        data={
            "username": TEST_EMAIL,
            "password": TEST_PASSWORD
        }
    )

    assert response.status_code == 200

    return response.json()["access_token"]


def auth_headers():
    token = get_token()

    return {
        "Authorization": f"Bearer {token}"
    }


def test_get_incidents_returns_pagination_structure():
    response = client.get(
        "/api/incidents/",
        headers=auth_headers()
    )

    assert response.status_code == 200

    data = response.json()

    assert "items" in data
    assert "total" in data
    assert "page" in data
    assert "page_size" in data
    assert "total_pages" in data

    assert isinstance(data["items"], list)
    assert isinstance(data["total"], int)
    assert isinstance(data["page"], int)
    assert isinstance(data["page_size"], int)
    assert isinstance(data["total_pages"], int)


def test_filter_incidents_by_status():
    response = client.get(
        "/api/incidents/?status=OPEN",
        headers=auth_headers()
    )

    assert response.status_code == 200

    data = response.json()

    for incident in data["items"]:
        assert incident["status"] == "OPEN"


def test_filter_incidents_by_priority():
    response = client.get(
        "/api/incidents/?priority=CRITICAL",
        headers=auth_headers()
    )

    assert response.status_code == 200

    data = response.json()

    for incident in data["items"]:
        assert incident["priority"] == "CRITICAL"


def test_filter_incidents_by_system():
    response = client.get(
        "/api/incidents/?system_id=2",
        headers=auth_headers()
    )

    assert response.status_code == 200

    data = response.json()

    for incident in data["items"]:
        assert incident["system_id"] == 2


def test_filter_incidents_by_category():
    response = client.get(
        "/api/incidents/?category_id=1",
        headers=auth_headers()
    )

    assert response.status_code == 200

    data = response.json()

    for incident in data["items"]:
        assert incident["category_id"] == 1


def test_filter_incidents_with_multiple_filters():
    response = client.get(
        "/api/incidents/?status=OPEN&priority=CRITICAL",
        headers=auth_headers()
    )

    assert response.status_code == 200

    data = response.json()

    for incident in data["items"]:
        assert incident["status"] == "OPEN"
        assert incident["priority"] == "CRITICAL"


def test_incidents_pagination_page_size():
    response = client.get(
        "/api/incidents/?page=1&page_size=1",
        headers=auth_headers()
    )

    assert response.status_code == 200

    data = response.json()

    assert data["page"] == 1
    assert data["page_size"] == 1
    assert len(data["items"]) <= 1


def test_incidents_pagination_second_page():
    response = client.get(
        "/api/incidents/?page=2&page_size=1",
        headers=auth_headers()
    )

    assert response.status_code == 200

    data = response.json()

    assert data["page"] == 2
    assert data["page_size"] == 1
    assert len(data["items"]) <= 1


def test_invalid_page_returns_422():
    response = client.get(
        "/api/incidents/?page=0",
        headers=auth_headers()
    )

    assert response.status_code == 422


def test_invalid_page_size_returns_422():
    response = client.get(
        "/api/incidents/?page_size=0",
        headers=auth_headers()
    )

    assert response.status_code == 422


def test_page_size_above_limit_returns_422():
    response = client.get(
        "/api/incidents/?page_size=101",
        headers=auth_headers()
    )

    assert response.status_code == 422


def test_incidents_without_authentication():
    response = client.get("/api/incidents/")

    assert response.status_code == 401
    

def test_search_incidents_by_title():
    response = client.get(
        "/api/incidents/?search=servidor",
        headers=auth_headers()
    )

    assert response.status_code == 200

    data = response.json()

    for incident in data["items"]:
        text = f"{incident['title']} {incident['description']}".lower()
        assert "servidor" in text


def test_search_incidents_is_case_insensitive():
    response = client.get(
        "/api/incidents/?search=SERVIDOR",
        headers=auth_headers()
    )

    assert response.status_code == 200

    data = response.json()

    for incident in data["items"]:
        text = f"{incident['title']} {incident['description']}".lower()
        assert "servidor" in text


def test_search_incidents_without_authentication():
    response = client.get(
        "/api/incidents/?search=servidor"
    )

    assert response.status_code == 401
    

def test_sort_incidents_by_title_ascending():
    response = client.get(
        "/api/incidents/?sort_by=title&sort_order=asc",
        headers=auth_headers()
    )

    assert response.status_code == 200

    data = response.json()
    titles = [incident["title"] for incident in data["items"]]

    assert titles == sorted(titles)


def test_sort_incidents_by_title_descending():
    response = client.get(
        "/api/incidents/?sort_by=title&sort_order=desc",
        headers=auth_headers()
    )

    assert response.status_code == 200

    data = response.json()
    titles = [incident["title"] for incident in data["items"]]

    assert titles == sorted(titles, reverse=True)


def test_invalid_sort_field_returns_422():
    response = client.get(
        "/api/incidents/?sort_by=password_hash",
        headers=auth_headers()
    )

    assert response.status_code == 422


def test_invalid_sort_order_returns_422():
    response = client.get(
        "/api/incidents/?sort_order=random",
        headers=auth_headers()
    )

    assert response.status_code == 422
    

def test_filter_incidents_by_created_from():
    response = client.get(
        "/api/incidents/?created_from=2026-01-01",
        headers=auth_headers()
    )

    assert response.status_code == 200

    data = response.json()

    for incident in data["items"]:
        assert incident["created_at"] >= "2026-01-01"


def test_filter_incidents_by_created_to():
    response = client.get(
        "/api/incidents/?created_to=2030-12-31",
        headers=auth_headers()
    )

    assert response.status_code == 200

    data = response.json()

    for incident in data["items"]:
        assert incident["created_at"] < "2031-01-01"


def test_filter_incidents_by_created_date_range():
    response = client.get(
        "/api/incidents/?created_from=2026-01-01&created_to=2030-12-31",
        headers=auth_headers()
    )

    assert response.status_code == 200

    data = response.json()

    for incident in data["items"]:
        assert incident["created_at"] >= "2026-01-01"
        assert incident["created_at"] < "2031-01-01"


def test_filter_incidents_with_date_range_and_status():
    response = client.get(
        "/api/incidents/?created_from=2026-01-01&created_to=2030-12-31&status=OPEN",
        headers=auth_headers()
    )

    assert response.status_code == 200

    data = response.json()

    for incident in data["items"]:
        assert incident["created_at"] >= "2026-01-01"
        assert incident["created_at"] < "2031-01-01"
        assert incident["status"] == "OPEN"
        
def test_filter_incidents_by_created_by():
    response = client.get(
        "/api/incidents/?created_by=1",
        headers=auth_headers()
    )

    assert response.status_code == 200

    data = response.json()

    for incident in data["items"]:
        assert incident["created_by"] == 1


def test_filter_incidents_by_assigned_to():
    response = client.get(
        "/api/incidents/?assigned_to=1",
        headers=auth_headers()
    )

    assert response.status_code == 200

    data = response.json()

    for incident in data["items"]:
        assert incident["assigned_to"] == 1


def test_filter_incidents_by_created_by_and_assigned_to():
    response = client.get(
        "/api/incidents/?created_by=1&assigned_to=1",
        headers=auth_headers()
    )

    assert response.status_code == 200

    data = response.json()

    for incident in data["items"]:
        assert incident["created_by"] == 1
        assert incident["assigned_to"] == 1