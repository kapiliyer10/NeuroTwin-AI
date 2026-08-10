from fastapi.testclient import TestClient

from backend.main import create_app
from backend.services.state_store import state_store


client = TestClient(create_app())


def setup_function() -> None:
    state_store.clear()


def test_concussion_checkin_flow() -> None:
    payload = {
        "user_id": "test-user",
        "clinician_evaluated": True,
        "recovery_stage": 2,
        "activity_type": "school",
        "activity_minutes": 30,
        "headache": 3,
        "fatigue": 4,
        "concentration_difficulty": 4,
        "symptoms_after_activity": 1,
    }

    ingest_response = client.post("/ingest", json=payload)
    assert ingest_response.status_code == 200
    body = ingest_response.json()
    assert set(body["state"]) == {
        "symptom_burden",
        "fatigue",
        "cognitive_load",
        "activity_tolerance",
        "trend",
        "risk_level",
        "stage",
    }
    assert body["evidence"]
    assert body["safety"]["status"] == "monitor"

    state_response = client.get("/state?user_id=test-user")
    assert state_response.status_code == 200
    assert state_response.json()["state"] == body["state"]

    simulate_response = client.post("/simulate?user_id=test-user", json={})
    assert simulate_response.status_code == 200
    assert "reduce_activity" in simulate_response.json()["simulations"]

    recommend_response = client.get("/recommend?user_id=test-user")
    assert recommend_response.status_code == 200
    assert recommend_response.json()["recommendation"] in {
        "continue_gently",
        "reduce_activity",
        "rest_and_check_in",
    }


def test_red_flags_override_recommendation() -> None:
    response = client.post(
        "/ingest",
        json={"severe_or_worsening_headache": True, "headache": 8},
    )
    assert response.status_code == 200
    body = response.json()
    assert body["safety"]["status"] == "urgent"
    assert body["safety"]["seek_urgent_care"] is True
    assert body["recommendation"] == "seek_urgent_care"


def test_state_requires_ingest_first() -> None:
    response = client.get("/state")
    assert response.status_code == 404


def test_delete_state_removes_health_records() -> None:
    client.post("/ingest", json={"headache": 2})
    response = client.delete("/state")
    assert response.status_code == 204
    assert client.get("/state").status_code == 404


def test_users_do_not_share_recovery_history() -> None:
    client.post("/ingest", json={"user_id": "alice", "headache": 2})
    client.post("/ingest", json={"user_id": "bob", "headache": 7})
    alice = client.get("/state?user_id=alice")
    bob = client.get("/state?user_id=bob")
    assert alice.status_code == 200
    assert bob.status_code == 200
    assert alice.json()["state"]["symptom_burden"] < bob.json()["state"]["symptom_burden"]


def test_sport_activity_never_implies_clearance() -> None:
    response = client.post(
        "/ingest",
        json={"activity_type": "sport", "recovery_stage": 3, "clinician_evaluated": False},
    )
    assert response.status_code == 200
    body = response.json()
    assert body["safety"]["status"] == "contact_professional"
    assert body["recommendation"] == "pause_and_contact_professional"


def test_high_symptom_values_trigger_caution_without_checkbox() -> None:
    response = client.post("/ingest", json={"headache": 7, "activity_type": "work"})
    assert response.status_code == 200
    body = response.json()
    assert body["safety"]["status"] == "contact_professional"
    assert body["recommendation"] == "pause_and_contact_professional"
    assert body["state"]["symptom_burden"] >= 4.9
    assert "increased after activity" not in body["explanation"]
