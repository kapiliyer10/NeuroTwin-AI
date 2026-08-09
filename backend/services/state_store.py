import json
import sqlite3
from datetime import datetime, timezone
from pathlib import Path

from backend.config import settings
from backend.schemas.input_schema import InputSchema
from backend.schemas.state_schema import RecoveryState, SafetyAssessment, StateRecord


class StateStore:
    """Small SQLite-backed store for demo sessions with deletion support."""

    def __init__(self) -> None:
        self._latest_simulations = None
        Path(settings.data_dir).mkdir(parents=True, exist_ok=True)
        self._connection = sqlite3.connect(settings.database_path, check_same_thread=False)
        self._connection.execute(
            "CREATE TABLE IF NOT EXISTS checkins (id INTEGER PRIMARY KEY, user_id TEXT NOT NULL, timestamp TEXT, payload TEXT NOT NULL)"
        )
        columns = {row[1] for row in self._connection.execute("PRAGMA table_info(checkins)")}
        if "user_id" not in columns:
            self._connection.execute("ALTER TABLE checkins ADD COLUMN user_id TEXT NOT NULL DEFAULT 'demo-user'")
        self._connection.commit()

    def record(self, input_data: InputSchema, state: RecoveryState, safety: SafetyAssessment) -> StateRecord:
        record = StateRecord(
            timestamp=datetime.now(timezone.utc),
            input_data=input_data,
            state=state,
            safety=safety,
        )
        payload = json.dumps(record.model_dump(mode="json"))
        self._connection.execute(
            "INSERT INTO checkins(user_id, timestamp, payload) VALUES (?, ?, ?)",
            (input_data.user_id, record.timestamp.isoformat(), payload),
        )
        self._connection.commit()
        self._latest_simulations = None
        return record

    def latest(self, user_id: str = "demo-user") -> StateRecord | None:
        row = self._connection.execute(
            "SELECT payload FROM checkins WHERE user_id = ? ORDER BY id DESC LIMIT 1", (user_id,)
        ).fetchone()
        return StateRecord.model_validate_json(row[0]) if row else None

    def history(self, limit: int, user_id: str = "demo-user") -> list[StateRecord]:
        rows = self._connection.execute(
            "SELECT payload FROM checkins WHERE user_id = ? ORDER BY id DESC LIMIT ?", (user_id, limit)
        ).fetchall()
        return [StateRecord.model_validate_json(row[0]) for row in reversed(rows)]

    def set_simulations(self, simulations) -> None:
        self._latest_simulations = simulations

    def latest_simulations(self):
        return self._latest_simulations

    def delete_all(self, user_id: str | None = None) -> None:
        if user_id is None:
            self._connection.execute("DELETE FROM checkins")
        else:
            self._connection.execute("DELETE FROM checkins WHERE user_id = ?", (user_id,))
        self._connection.commit()
        self._latest_simulations = None

    def clear(self) -> None:
        self.delete_all()


state_store = StateStore()
