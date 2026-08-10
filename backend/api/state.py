from fastapi import APIRouter, HTTPException, Query

from backend.config import settings
from backend.schemas.state_schema import HistoryResponse, StateResponse, EvidenceReference
from backend.services.evidence import evidence_references
from backend.services.explainability import Explainability
from backend.services.intervention_engine import InterventionEngine
from backend.services.state_store import state_store

router = APIRouter(tags=["recovery"])


def _response(record) -> StateResponse:
    recommendation = "seek_urgent_care" if record.safety.seek_urgent_care else "pause_and_contact_professional" if record.safety.status == "contact_professional" else "continue_gently"
    return StateResponse(
        state=record.state,
        safety=record.safety,
        recommendation=recommendation,
        explanation=Explainability().generate(record.state, recommendation, record.safety),
        evidence=[EvidenceReference(**item) for item in evidence_references(record.input_data.purpose.value)],
        message="Latest recovery check-in returned.",
    )


@router.get("/state", response_model=StateResponse)
def get_latest_state(user_id: str = Query(default="demo-user", min_length=1, max_length=64)) -> StateResponse:
    latest = state_store.latest(user_id=user_id)
    if latest is None:
        raise HTTPException(status_code=404, detail="No check-in has been recorded yet.")
    return _response(latest)


@router.get("/state/history", response_model=HistoryResponse)
def get_state_history(
    limit: int = Query(default=settings.default_history_limit, ge=1, le=100),
    user_id: str = Query(default="demo-user", min_length=1, max_length=64),
) -> HistoryResponse:
    return HistoryResponse(records=state_store.history(limit=limit, user_id=user_id))


@router.delete("/state", status_code=204)
def delete_state(user_id: str = Query(default="demo-user", min_length=1, max_length=64)) -> None:
    state_store.delete_all(user_id=user_id)
