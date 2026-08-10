from fastapi import APIRouter

from backend.schemas.input_schema import InputSchema
from backend.schemas.state_schema import EvidenceReference, StateResponse
from backend.services.evidence import evidence_references
from backend.services.explainability import Explainability
from backend.services.intervention_engine import InterventionEngine
from backend.services.state_model import RecoveryStateModel
from backend.services.simulation_engine import SimulationEngine
from backend.services.state_store import state_store

router = APIRouter(tags=["check-in"])


@router.post("/ingest", response_model=StateResponse)
def ingest_data(data: InputSchema) -> StateResponse:
    previous = state_store.latest(user_id=data.user_id)
    model = RecoveryStateModel()
    state = model.predict(data, previous.state if previous else None)
    safety = InterventionEngine().assess_safety(data)
    simulations = SimulationEngine().run(state, data)
    engine = InterventionEngine()
    recommendation = engine.recommend(simulations, safety)
    state_store.record(input_data=data, state=state, safety=safety)
    state_store.set_simulations(simulations)
    explanation = Explainability().generate(state, recommendation, safety)
    return StateResponse(
        state=state,
        safety=safety,
        recommendation=recommendation,
        explanation=explanation,
        evidence=[EvidenceReference(**item) for item in evidence_references()],
        message="Check-in recorded. Follow your healthcare professional's plan.",
    )
