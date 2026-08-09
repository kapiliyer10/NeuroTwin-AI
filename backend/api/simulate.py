from fastapi import APIRouter, HTTPException, Query

from backend.schemas.simulation_schema import SimulationRequest, SimulationResponse
from backend.services.simulation_engine import SimulationEngine
from backend.services.state_store import state_store

router = APIRouter(tags=["recovery"])


@router.post("/simulate", response_model=SimulationResponse)
def simulate(
    data: SimulationRequest | None = None,
    user_id: str = Query(default="demo-user", min_length=1, max_length=64),
) -> SimulationResponse:
    state = data.state if data and data.state else None
    latest = state_store.latest(user_id=user_id)
    if state is None and latest is None:
        raise HTTPException(status_code=404, detail="No check-in available to simulate.")
    state = state or latest.state
    results = SimulationEngine().run(state, latest.input_data if latest else None)
    state_store.set_simulations(results)
    return SimulationResponse(baseline=state, simulations=results)
