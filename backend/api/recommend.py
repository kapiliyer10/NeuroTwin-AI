from fastapi import APIRouter, HTTPException

from backend.schemas.simulation_schema import RecommendationResponse
from backend.services.explainability import Explainability
from backend.services.intervention_engine import InterventionEngine
from backend.services.simulation_engine import SimulationEngine
from backend.services.state_store import state_store

router = APIRouter(tags=["recommendation"])


@router.get("/recommend", response_model=RecommendationResponse)
def recommend() -> RecommendationResponse:
    latest = state_store.latest()
    if latest is None:
        raise HTTPException(status_code=404, detail="No state available for recommendations.")

    simulations = state_store.latest_simulations() or SimulationEngine().run(latest.state)
    recommendation = InterventionEngine().recommend(simulations)
    explanation = Explainability().generate(latest.state, recommendation)

    return RecommendationResponse(
        recommendation=recommendation,
        simulations=simulations,
        explanation=explanation,
    )
