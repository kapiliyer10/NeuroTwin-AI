from fastapi import APIRouter, HTTPException

from backend.schemas.simulation_schema import SimulationRequest, SimulationResponse
from backend.services.simulation_engine import SimulationEngine
from backend.services.state_store import state_store

router = APIRouter(tags=["simulation"])


@router.post("/simulate", response_model=SimulationResponse)
def simulate(data: SimulationRequest | None = None) -> SimulationResponse:
    state = data.state if data and data.state else None
    if state is None:
        latest = state_store.latest()
        if latest is None:
            raise HTTPException(status_code=404, detail="No state available to simulate.")
        state = latest.state

    results = SimulationEngine().run(state)
    state_store.set_simulations(results)
    return SimulationResponse(baseline=state, simulations=results)
