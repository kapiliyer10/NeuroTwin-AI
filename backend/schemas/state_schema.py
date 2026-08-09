from datetime import datetime

from pydantic import BaseModel, Field

from backend.schemas.input_schema import InputSchema


class RecoveryState(BaseModel):
    symptom_burden: float = Field(..., ge=0, le=10)
    fatigue: float = Field(..., ge=0, le=10)
    cognitive_load: float = Field(..., ge=0, le=10)
    activity_tolerance: float = Field(..., ge=0, le=10)
    trend: str
    risk_level: str
    stage: int = Field(..., ge=1, le=6)


class SafetyAssessment(BaseModel):
    status: str
    message: str
    reasons: list[str] = Field(default_factory=list)
    seek_urgent_care: bool = False


class EvidenceReference(BaseModel):
    title: str
    publisher: str
    url: str
    reviewed: str


class StateRecord(BaseModel):
    timestamp: datetime
    input_data: InputSchema
    state: RecoveryState
    safety: SafetyAssessment


class StateResponse(BaseModel):
    state: RecoveryState
    safety: SafetyAssessment
    recommendation: str
    explanation: str
    evidence: list[EvidenceReference]
    message: str


class HistoryResponse(BaseModel):
    records: list[StateRecord]
