from datetime import date
from enum import Enum

from pydantic import BaseModel, Field


class ActivityType(str, Enum):
    daily = "daily"
    school = "school"
    work = "work"
    screen = "screen"
    walking = "walking"
    exercise = "exercise"
    sport = "sport"


class InputSchema(BaseModel):
    user_id: str = Field(default="demo-user", min_length=1, max_length=64)
    injury_date: date | None = None
    clinician_evaluated: bool = False
    recovery_stage: int = Field(default=1, ge=1, le=6)
    activity_type: ActivityType = ActivityType.daily
    activity_minutes: int = Field(default=0, ge=0, le=1440)
    headache: int = Field(default=0, ge=0, le=10)
    dizziness: int = Field(default=0, ge=0, le=10)
    nausea: int = Field(default=0, ge=0, le=10)
    light_sensitivity: int = Field(default=0, ge=0, le=10)
    noise_sensitivity: int = Field(default=0, ge=0, le=10)
    fatigue: int = Field(default=0, ge=0, le=10)
    sleep_quality: int = Field(default=5, ge=0, le=10)
    memory_difficulty: int = Field(default=0, ge=0, le=10)
    concentration_difficulty: int = Field(default=0, ge=0, le=10)
    balance_problem: int = Field(default=0, ge=0, le=10)
    mood_change: int = Field(default=0, ge=0, le=10)
    symptoms_after_activity: int = Field(default=0, ge=0, le=10)
    symptoms_worsened: bool = False
    severe_or_worsening_headache: bool = False
    repeated_vomiting: bool = False
    seizure_or_fainting: bool = False
    confusion_or_slurred_speech: bool = False
    weakness_numbness_or_vision_change: bool = False
