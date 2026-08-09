from backend.config import settings
from backend.schemas.state_schema import RecoveryState, SafetyAssessment


class Explainability:
    def generate(self, state: RecoveryState, recommendation: str, safety: SafetyAssessment) -> str:
        if safety.seek_urgent_care:
            return f"{safety.message} The app detected: {', '.join(safety.reasons)}. {settings.safety_disclaimer}"
        if safety.status == "contact_professional":
            return f"{safety.message} Your symptoms increased after activity, so the next step is to pause and reassess. {settings.safety_disclaimer}"
        return (
            f"Your symptom burden is {state.symptom_burden}/10 and your estimated activity tolerance is "
            f"{state.activity_tolerance}/10. The suggested next step is symptom-guided and does not provide diagnosis or clearance. "
            f"{settings.safety_disclaimer}"
        )
