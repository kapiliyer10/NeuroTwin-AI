from backend.schemas.input_schema import InputSchema
from backend.schemas.simulation_schema import SimulationOutcome
from backend.schemas.state_schema import RecoveryState


class SimulationEngine:
    """Project symptom-tolerated next steps; never grants medical clearance."""

    ACTIONS = {
        "continue_gently": ("Continue gently", -0.15, 0.2),
        "reduce_activity": ("Reduce activity", -0.55, -0.15),
        "rest_and_check_in": ("Rest and check in later", -0.85, -0.35),
    }

    def run(self, state: RecoveryState, data: InputSchema | None = None) -> dict[str, SimulationOutcome]:
        if data and data.symptoms_worsened:
            return {"rest_and_check_in": self.simulate(state, "rest_and_check_in", forced=True)}
        return {action: self.simulate(state, action) for action in self.ACTIONS}

    def simulate(self, state: RecoveryState, action: str, forced: bool = False) -> SimulationOutcome:
        label, burden_delta, tolerance_delta = self.ACTIONS[action]
        if state.purpose == "mental_wellbeing":
            label = {
                "continue_gently": "Take a gentle step",
                "reduce_activity": "Reduce pressure",
                "rest_and_check_in": "Pause and check in later",
            }[action]
        burden = max(0.0, min(10.0, state.symptom_burden + burden_delta))
        tolerance = max(0.0, min(10.0, state.activity_tolerance + tolerance_delta))
        status = "monitor"
        if forced or action == "rest_and_check_in":
            status = "pause_and_reassess"
        return SimulationOutcome(
            action=action,
            label=label,
            projected_symptom_burden=round(burden, 2),
            projected_activity_tolerance=round(tolerance, 2),
            safety_status=status,
            summary=self._summary(action, state.purpose),
        )

    def _summary(self, action: str, purpose: str = "concussion") -> str:
        if purpose == "mental_wellbeing":
            if action == "continue_gently":
                return "Choose one manageable task and notice how it affects your energy and stress."
            if action == "reduce_activity":
                return "Lower the pressure or shorten the task, then check in with yourself later."
            return "Pause, use a supportive coping step, and check in again when you feel ready."
        if action == "continue_gently":
            return "Keep the activity light and stop if symptoms increase more than mildly."
        if action == "reduce_activity":
            return "Shorten or simplify the activity, then compare symptoms with your baseline."
        return "Pause the activity, allow symptoms to settle, and check in again later."
