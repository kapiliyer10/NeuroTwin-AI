from fastapi.testclient import TestClient

from backend.main import create_app
from backend.services.state_store import state_store


client = TestClient(create_app())


def setup_function() -> None:
    state_store.clear()


def test_ingest_simulate_recommend_flow() -> None:
    payload = {
        "typing_speed": 52,
        "pause_variance": 1.8,
        "sentiment": -0.2,
        "screen_time": 7,
    }

    ingest_response = client.post("/ingest", json=payload)
    assert ingest_response.status_code == 200
    state = ingest_response.json()["state"]
    assert set(state) == {"stress", "fatigue", "attention", "emotion"}

    state_response = client.get("/state")
    assert state_response.status_code == 200
    assert state_response.json()["state"] == state

    simulate_response = client.post("/simulate", json={})
    assert simulate_response.status_code == 200
    assert "short_break" in simulate_response.json()["simulations"]

    recommend_response = client.get("/recommend")
    assert recommend_response.status_code == 200
    assert recommend_response.json()["recommendation"] in {"continue", "short_break", "sleep"}


def test_state_requires_ingest_first() -> None:
    response = client.get("/state")
    assert response.status_code == 404
