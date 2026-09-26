"""Tests for the /api/health endpoint and DB connectivity."""
from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_health_returns_200_and_ok_status():
    response = client.get("/api/health")
    assert response.status_code == 200

    body = response.json()
    assert body["status"] == "ok"
    assert body["database"] == "ok"
    assert "service" in body
    assert "environment" in body


def test_unknown_route_returns_json_error_shape():
    response = client.get("/api/does-not-exist")
    assert response.status_code == 404
    body = response.json()
    assert "error" in body
    assert "message" in body["error"]
