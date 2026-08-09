from datetime import datetime

from pydantic import BaseModel, Field

from backend.schemas.input_schema import InputSchema


class CognitiveState(BaseModel):
    stress: float = Field(..., ge=0, le=1)
    fatigue: float = Field(..., ge=0, le=1)
    attention: float = Field(..., ge=0, le=1)
    emotion: float = Field(..., ge=0, le=1)


class StateRecord(BaseModel):
    timestamp: datetime
    input_data: InputSchema
    features: list[float]
    state: CognitiveState


class StateResponse(BaseModel):
    state: CognitiveState
    message: str


class HistoryResponse(BaseModel):
    records: list[StateRecord]
