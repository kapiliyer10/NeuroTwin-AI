from backend.schemas.input_schema import InputSchema
from backend.schemas.state_schema import RecoveryState
from backend.services.signal_fusion import SignalFusion


class RecoveryStateModel:
    """Interpretable symptom model; it is not a diagnostic or clearance model."""

    def predict(self, data: InputSchema, previous: RecoveryState | None = None) -> RecoveryState:
        features = SignalFusion().extract(data)
        burden = features["symptom_burden"]
        activity_effect = min(features["post_activity_change"] * 0.35, 2.5)
        cognitive_load = min(10.0, features["cognitive_load"] + activity_effect)
        tolerance = max(0.0, min(10.0, 10 - burden - activity_effect))

        if previous and data.symptoms_worsened:
            trend = "worsening"
        elif previous and burden < previous.symptom_burden - 0.35:
            trend = "improving"
        elif previous:
            trend = "stable"
        else:
            trend = "baseline"

        risk_level = "high" if data.symptoms_worsened else "moderate" if burden >= 5 else "low"
        return RecoveryState(
            symptom_burden=round(burden, 2),
            fatigue=round(features["fatigue"], 2),
            cognitive_load=round(cognitive_load, 2),
            activity_tolerance=round(tolerance, 2),
            trend=trend,
            risk_level=risk_level,
            stage=data.recovery_stage,
        )
