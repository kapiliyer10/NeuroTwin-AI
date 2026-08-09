from pydantic import BaseModel

from backend.schemas.state_schema import RecoveryState


class SimulationOutcome(BaseModel):
    action: str
    label: str
    projected_symptom_burden: float
    projected_activity_tolerance: float
    safety_status: str
    summary: str


class SimulationRequest(BaseModel):
    state: RecoveryState | None = None


class SimulationResponse(BaseModel):
    baseline: RecoveryState
    simulations: dict[str, SimulationOutcome]


class RecommendationResponse(BaseModel):
    recommendation: str
    explanation: str
    safety: str
    evidence: list[dict[str, str]]
    simulations: dict[str, SimulationOutcome]
