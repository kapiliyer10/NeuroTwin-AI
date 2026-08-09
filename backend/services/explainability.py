from backend.config import settings
from backend.schemas.state_schema import CognitiveState
from backend.utils.safety import validate_output


class Explainability:
    """Generate concise, non-clinical explanations for recommendations."""

    def generate(self, state: CognitiveState, recommendation: str) -> str:
        drivers = []
        if state.stress >= 0.65:
            drivers.append("stress is elevated")
        if state.fatigue >= 0.65:
            drivers.append("fatigue is elevated")
        if state.attention <= 0.4:
            drivers.append("attention is reduced")
        if not drivers:
            drivers.append("the current state appears relatively balanced")

        action = recommendation.replace("_", " ")
        text = (
            f"Recommended action: {action}. This is based on {', '.join(drivers)} "
            f"and the simulated recovery profile. {settings.safety_disclaimer}"
        )
        return validate_output(text)
