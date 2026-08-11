import pandas as pd
from fastapi.testclient import TestClient

from src.api.main import app

client = TestClient(app)


def test_health_endpoint():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_companies_endpoint():
    response = client.get("/companies")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0


def test_screener_endpoint():
    response = client.get("/screener")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0


def test_portfolio_cluster_endpoint():
    response = client.get("/portfolio/clusters")
    assert response.status_code == 200
    payload = response.json()
    assert "clusters" in payload
    assert isinstance(payload["clusters"], list)
