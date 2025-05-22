from fastapi.testclient import TestClient

from app import app

client = TestClient(app)


def test_get_country():
    response = client.get("/countries/USA")
    assert response.status_code == 200
    assert response.json() == {"cities": ["New York", "Los Angeles", "Chicago"]}

def test_get_country_not_found():
    response = client.get("/countries/NonExistentCountry")
    assert response.status_code == 404
    assert response.json() == {"detail": "Country not found"}

def test_get_country_spain():
    response = client.get("/countries/Spain")
    assert response.status_code == 404
    assert response.json() == {"detail": "Country not found"}