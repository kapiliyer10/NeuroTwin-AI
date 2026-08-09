from fastapi import APIRouter, HTTPException, Query

from backend.config import settings
from backend.schemas.state_schema import HistoryResponse, StateResponse
from backend.services.state_store import state_store

router = APIRouter(tags=["state"])


@router.get("/state", response_model=StateResponse)
def get_latest_state() -> StateResponse:
    latest = state_store.latest()
    if latest is None:
        raise HTTPException(status_code=404, detail="No state has been recorded yet.")
    return StateResponse(state=latest.state, message="Latest cognitive state returned.")


@router.get("/state/history", response_model=HistoryResponse)
def get_state_history(
    limit: int = Query(default=settings.default_history_limit, ge=1, le=100),
) -> HistoryResponse:
    return HistoryResponse(records=state_store.history(limit=limit))
