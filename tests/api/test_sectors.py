from fastapi.testclient import TestClient

from src.api.main import app

client = TestClient(app)


def test_sectors_endpoint_works():
    response = client.get("/api/v1/sectors")
    assert response.status_code == 200


def test_sector_companies_endpoint_works():
    response = client.get("/api/v1/sectors/Financials/companies")
    assert response.status_code == 200
