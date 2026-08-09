from backend.schemas.simulation_schema import SimulationOutcome
from backend.schemas.state_schema import CognitiveState


def _clamp(value: float) -> float:
    return round(max(0.0, min(1.0, value)), 3)


class SimulationEngine:
    """Project likely state changes for simple intervention choices."""

    ACTION_EFFECTS = {
        "continue": {"stress": 0.15, "fatigue": 0.12, "attention": -0.08, "emotion": -0.04},
        "short_break": {"stress": -0.18, "fatigue": -0.08, "attention": 0.14, "emotion": 0.08},
        "sleep": {"stress": -0.35, "fatigue": -0.42, "attention": 0.28, "emotion": 0.12},
    }

    def run(self, state: CognitiveState) -> dict[str, SimulationOutcome]:
        return {action: self.simulate(state, action) for action in self.ACTION_EFFECTS}

    def simulate(self, state: CognitiveState, action: str) -> SimulationOutcome:
        effect = self.ACTION_EFFECTS[action]
        next_state = {
            "stress": _clamp(state.stress + effect["stress"]),
            "fatigue": _clamp(state.fatigue + effect["fatigue"]),
            "attention": _clamp(state.attention + effect["attention"]),
            "emotion": _clamp(state.emotion + effect["emotion"]),
        }
        return SimulationOutcome(
            **next_state,
            summary=self._summary(action, next_state),
        )

    def _summary(self, action: str, state: dict[str, float]) -> str:
        if action == "continue":
            return "Continuing may preserve momentum but is likely to increase stress and fatigue."
        if action == "short_break":
            return "A short break is projected to reduce stress while improving attention."
        return "Sleep is projected to produce the strongest recovery when fatigue is elevated."
