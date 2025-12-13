# tests/test_endpoints.py
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_health_endpoint():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_generate_2fa_without_seed():
    response = client.get("/generate-2fa")
    assert response.status_code in [400, 404]


def test_verify_2fa_without_seed():
    response = client.post("/verify-2fa", json={"token": "123456"})
    assert response.status_code in [400, 404]
