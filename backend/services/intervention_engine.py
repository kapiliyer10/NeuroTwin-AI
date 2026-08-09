from backend.schemas.simulation_schema import SimulationOutcome


class InterventionEngine:
    """Choose the intervention with the best balance of lower strain and higher attention."""

    def recommend(self, simulations: dict[str, SimulationOutcome]) -> str:
        return min(simulations, key=lambda action: self._score(simulations[action]))

    def _score(self, outcome: SimulationOutcome) -> float:
        return (outcome.stress * 0.45) + (outcome.fatigue * 0.35) + ((1 - outcome.attention) * 0.2)
