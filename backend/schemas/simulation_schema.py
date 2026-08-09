from pydantic import BaseModel

from backend.schemas.state_schema import CognitiveState


class SimulationOutcome(BaseModel):
    stress: float
    fatigue: float
    attention: float
    emotion: float
    summary: str


class SimulationRequest(BaseModel):
    state: CognitiveState | None = None


class SimulationResponse(BaseModel):
    baseline: CognitiveState
    simulations: dict[str, SimulationOutcome]


class RecommendationResponse(BaseModel):
    recommendation: str
    simulations: dict[str, SimulationOutcome]
    explanation: str
