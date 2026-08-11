from fastapi.testclient import TestClient

from src.api.main import app

client = TestClient(app)


def test_companies_returns_canonical_universe():
    response = client.get("/api/v1/companies")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0


def test_company_lookup_returns_actual_company():
    response = client.get("/api/v1/companies/TCS")
    assert response.status_code == 200
