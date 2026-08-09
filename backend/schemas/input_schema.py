from pydantic import BaseModel, Field


class InputSchema(BaseModel):
    typing_speed: float = Field(..., ge=0, le=200, description="Words or characters per minute proxy.")
    pause_variance: float = Field(..., ge=0, le=10, description="Variance in pauses between user actions.")
    sentiment: float = Field(..., ge=-1, le=1, description="Sentiment score from -1 to 1.")
    screen_time: float = Field(..., ge=0, le=24, description="Recent screen time in hours.")
