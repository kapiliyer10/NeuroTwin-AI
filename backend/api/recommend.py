from fastapi import APIRouter, HTTPException, Query

from backend.schemas.simulation_schema import RecommendationResponse
from backend.services.evidence import evidence_references
from backend.services.explainability import Explainability
from backend.services.intervention_engine import InterventionEngine
from backend.services.simulation_engine import SimulationEngine
from backend.services.state_store import state_store

router = APIRouter(tags=["recovery"])


@router.get("/recommend", response_model=RecommendationResponse)
def recommend(user_id: str = Query(default="demo-user", min_length=1, max_length=64)) -> RecommendationResponse:
    latest = state_store.latest(user_id=user_id)
    if latest is None:
        raise HTTPException(status_code=404, detail="No check-in available for a recommendation.")
    simulations = state_store.latest_simulations() or SimulationEngine().run(latest.state, latest.input_data)
    engine = InterventionEngine()
    recommendation = engine.recommend(simulations, latest.safety)
    return RecommendationResponse(
        recommendation=recommendation,
        explanation=Explainability().generate(latest.state, recommendation, latest.safety),
        safety=latest.safety.status,
        evidence=evidence_references(),
        simulations=simulations,
    )
