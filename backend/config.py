from pydantic import BaseModel


class Settings(BaseModel):
    app_name: str = "NeuroTwin AI"
    app_version: str = "0.2.0"
    cors_origins: list[str] = ["http://localhost:3000", "http://127.0.0.1:3000"]
    default_history_limit: int = 25
    data_dir: str = ".data"
    database_path: str = ".data/neurotwin.sqlite3"
    safety_disclaimer: str = "This prototype does not diagnose concussion, provide treatment, or clear anyone for sport."


settings = Settings()
