from datetime import datetime, timezone

from backend.schemas.input_schema import InputSchema
from backend.schemas.simulation_schema import SimulationOutcome
from backend.schemas.state_schema import CognitiveState, StateRecord


class StateStore:
    """In-memory store for local prototype sessions."""

    def __init__(self) -> None:
        self._records: list[StateRecord] = []
        self._latest_simulations: dict[str, SimulationOutcome] | None = None

    def record(self, input_data: InputSchema, state: CognitiveState, features: list[float]) -> StateRecord:
        record = StateRecord(
            timestamp=datetime.now(timezone.utc),
            input_data=input_data,
            features=features,
            state=state,
        )
        self._records.append(record)
        self._latest_simulations = None
        return record

    def latest(self) -> StateRecord | None:
        if not self._records:
            return None
        return self._records[-1]

    def history(self, limit: int) -> list[StateRecord]:
        return self._records[-limit:]

    def set_simulations(self, simulations: dict[str, SimulationOutcome]) -> None:
        self._latest_simulations = simulations

    def latest_simulations(self) -> dict[str, SimulationOutcome] | None:
        return self._latest_simulations

    def clear(self) -> None:
        self._records.clear()
        self._latest_simulations = None


state_store = StateStore()
