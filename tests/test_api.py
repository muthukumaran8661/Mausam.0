"""Integration tests for FastAPI endpoints."""

import pytest
from starlette.testclient import TestClient
from app.main import app
from app.database import init_db
from seed import seed_database

client = TestClient(app)


@pytest.fixture(scope="module", autouse=True)
def setup_db():
    init_db()
    seed_database()


def test_health_endpoint():
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert data["app"] == "Mausam"


def test_get_user_preferences():
    response = client.get("/api/users/1/preferences")
    assert response.status_code == 200
    data = response.json()
    assert data["user_id"] == 1
    assert data["units"] in ("metric", "imperial")
    assert "commute" in data["interests"]


def test_update_user_preferences():
    payload = {
        "units": "metric",
        "language": "hi",
        "interests": ["commute", "fitness", "farming"],
        "sensitivities": ["heat"],
        "commute_morning": "09:00",
        "commute_evening": "18:30",
    }
    response = client.put("/api/users/1/preferences", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["language"] == "hi"
    assert "farming" in data["interests"]
    assert data["commute_morning"] == "09:00"

    # Reset back to en
    client.put("/api/users/1/preferences", json={"language": "en"})


def test_saved_cities_crud():
    # 1. List cities
    get_res = client.get("/api/users/1/cities")
    assert get_res.status_code == 200
    initial_cities = get_res.json()
    assert len(initial_cities) >= 2

    # 2. Add city (Chennai)
    new_city = {
        "name": "Chennai",
        "state": "Tamil Nadu",
        "country": "India",
        "lat": 13.0827,
        "lon": 80.2707,
        "is_favorite": False,
        "display_order": 5,
    }
    post_res = client.post("/api/users/1/cities", json=new_city)
    assert post_res.status_code == 201
    created = post_res.json()
    city_id = created["id"]
    assert created["name"] == "Chennai"

    # 3. Delete city
    del_res = client.delete(f"/api/users/1/cities/{city_id}")
    assert del_res.status_code == 204


def test_geocoding_search():
    res = client.get("/api/geocode?q=Mumbai")
    assert res.status_code == 200
    results = res.json()
    assert len(results) > 0
    assert any("Mumbai" in r["name"] for r in results)


def test_alerts_endpoint():
    res = client.get("/api/alerts?lat=28.6139&lon=77.2090")
    assert res.status_code == 200
    alerts = res.json()
    assert isinstance(alerts, list)
    assert len(alerts) >= 1
    assert "title" in alerts[0]
    assert "severity" in alerts[0]


def test_home_aggregated_api_with_user():
    res = client.get("/api/home?user_id=1")
    assert res.status_code == 200
    data = res.json()

    # Verify structure
    assert data["location_name"] is not None
    assert "current" in data
    assert "hourly" in data
    assert "daily" in data
    assert "metrics" in data
    assert "insights_top" in data
    assert "insights_all" in data
    assert len(data["insights_top"]) <= 3
    assert len(data["hourly"]) >= 12
    assert len(data["daily"]) == 7
    assert len(data["saved_cities"]) >= 2
    assert data["freshness_text"] is not None


def test_home_aggregated_api_anonymous():
    res = client.get("/api/home?lat=19.0760&lon=72.8777&city_name=Mumbai")
    assert res.status_code == 200
    data = res.json()
    assert data["location_name"] == "Mumbai"
    assert len(data["insights_top"]) <= 3
    assert data["current"]["temp"] is not None
