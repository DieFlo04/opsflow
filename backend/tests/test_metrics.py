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


def test_get_incident_metrics_authenticated():
    response = client.get(
        "/api/metrics/incidents",
        headers=auth_headers()
    )

    assert response.status_code == 200

    data = response.json()

    assert "total" in data
    assert "open" in data
    assert "in_progress" in data
    assert "resolved" in data
    assert "closed" in data

    assert isinstance(data["total"], int)
    assert isinstance(data["open"], int)
    assert isinstance(data["in_progress"], int)
    assert isinstance(data["resolved"], int)
    assert isinstance(data["closed"], int)


def test_get_incident_metrics_without_authentication():
    response = client.get("/api/metrics/incidents")

    assert response.status_code == 401


def test_get_incidents_by_priority_authenticated():
    response = client.get(
        "/api/metrics/incidents/by-priority",
        headers=auth_headers()
    )

    assert response.status_code == 200

    data = response.json()

    assert isinstance(data, dict)

    for priority, count in data.items():
        assert isinstance(priority, str)
        assert isinstance(count, int)


def test_get_incidents_by_status_authenticated():
    response = client.get(
        "/api/metrics/incidents/by-status",
        headers=auth_headers()
    )

    assert response.status_code == 200

    data = response.json()

    assert isinstance(data, dict)

    for status, count in data.items():
        assert isinstance(status, str)
        assert isinstance(count, int)


def test_get_incidents_by_system_authenticated():
    response = client.get(
        "/api/metrics/incidents/by-system",
        headers=auth_headers()
    )

    assert response.status_code == 200

    data = response.json()

    assert isinstance(data, dict)

    for system_name, count in data.items():
        assert isinstance(system_name, str)
        assert isinstance(count, int)


def test_get_incidents_by_category_authenticated():
    response = client.get(
        "/api/metrics/incidents/by-category",
        headers=auth_headers()
    )

    assert response.status_code == 200

    data = response.json()

    assert isinstance(data, dict)

    for category_name, count in data.items():
        assert isinstance(category_name, str)
        assert isinstance(count, int)


def test_get_critical_incidents_authenticated():
    response = client.get(
        "/api/metrics/incidents/critical",
        headers=auth_headers()
    )

    assert response.status_code == 200

    data = response.json()

    assert isinstance(data, list)

    for incident in data:
        assert "id" in incident
        assert "title" in incident
        assert "priority" in incident
        assert "status" in incident


def test_get_open_incidents_authenticated():
    response = client.get(
        "/api/metrics/incidents/open",
        headers=auth_headers()
    )

    assert response.status_code == 200

    data = response.json()

    assert isinstance(data, list)

    for incident in data:
        assert "id" in incident
        assert "title" in incident
        assert "priority" in incident
        assert "status" in incident

        assert incident["status"] in [
            "OPEN",
            "IN_PROGRESS"
        ]


def test_get_incident_age_authenticated():
    response = client.get(
        "/api/metrics/incidents/age",
        headers=auth_headers()
    )

    assert response.status_code == 200

    data = response.json()

    assert isinstance(data, list)

    for incident in data:
        assert "id" in incident
        assert "title" in incident
        assert "status" in incident
        assert "priority" in incident
        assert "created_at" in incident
        assert "age_hours" in incident

        assert isinstance(incident["age_hours"], (int, float))
        assert incident["age_hours"] >= 0


def test_get_incident_analysis_authenticated():
    response = client.get(
        "/api/metrics/analysis",
        headers=auth_headers()
    )

    assert response.status_code == 200

    data = response.json()

    assert "total_open_incidents" in data
    assert "critical_incidents" in data
    assert "old_incidents" in data
    assert "alerts" in data

    assert isinstance(data["total_open_incidents"], int)
    assert isinstance(data["critical_incidents"], int)
    assert isinstance(data["old_incidents"], int)
    assert isinstance(data["alerts"], list)

    for alert in data["alerts"]:
        assert "type" in alert
        assert "severity" in alert
        assert "incident_id" in alert
        assert "message" in alert


def test_get_resolution_times_authenticated():
    response = client.get(
        "/api/metrics/incidents/resolution-times",
        headers=auth_headers()
    )

    assert response.status_code == 200

    data = response.json()

    assert isinstance(data, list)

    for incident in data:
        assert "id" in incident
        assert "title" in incident
        assert "priority" in incident
        assert "created_at" in incident
        assert "resolved_at" in incident
        assert "resolution_hours" in incident

        assert isinstance(
            incident["resolution_hours"],
            (int, float)
        )

        assert incident["resolution_hours"] >= 0


def test_get_average_resolution_time_authenticated():
    response = client.get(
        "/api/metrics/incidents/average-resolution-time",
        headers=auth_headers()
    )

    assert response.status_code == 200

    data = response.json()

    assert "resolved_incidents" in data
    assert "average_resolution_hours" in data

    assert isinstance(data["resolved_incidents"], int)
    assert isinstance(
        data["average_resolution_hours"],
        (int, float)
    )

    assert data["resolved_incidents"] >= 0
    assert data["average_resolution_hours"] >= 0


def test_metrics_without_authentication():
    endpoints = [
        "/api/metrics/incidents/by-priority",
        "/api/metrics/incidents/by-status",
        "/api/metrics/incidents/by-system",
        "/api/metrics/incidents/by-category",
        "/api/metrics/incidents/critical",
        "/api/metrics/incidents/open",
        "/api/metrics/incidents/age",
        "/api/metrics/analysis",
        "/api/metrics/incidents/resolution-times",
        "/api/metrics/incidents/average-resolution-time",
    ]

    for endpoint in endpoints:
        response = client.get(endpoint)

        assert response.status_code == 401