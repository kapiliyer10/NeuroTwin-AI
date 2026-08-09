from pydantic import BaseModel


class Settings(BaseModel):
    app_name: str = "NeuroTwin AI"
    app_version: str = "0.1.0"
    cors_origins: list[str] = ["http://localhost:3000", "http://127.0.0.1:3000"]
    default_history_limit: int = 25
    safety_disclaimer: str = (
        "NeuroTwin AI is a wellness prototype and does not provide medical diagnosis or treatment."
    )


settings = Settings()
