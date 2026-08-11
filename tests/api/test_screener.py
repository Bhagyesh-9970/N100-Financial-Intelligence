from fastapi.testclient import TestClient

from src.api.main import app

client = TestClient(app)


def test_screener_works():
    response = client.get("/api/v1/screener")
    assert response.status_code == 200


def test_screener_filters_min_roe():
    response = client.get("/api/v1/screener", params={"min_roe": 15})
    assert response.status_code == 200
