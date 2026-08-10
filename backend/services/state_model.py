from backend.schemas.input_schema import InputSchema
from backend.schemas.state_schema import RecoveryState
from backend.services.signal_fusion import SignalFusion


class RecoveryStateModel:
    """Interpretable symptom model; it is not a diagnostic or clearance model."""

    def predict(self, data: InputSchema, previous: RecoveryState | None = None) -> RecoveryState:
        features = SignalFusion().extract(data)
        # A high individual symptom should remain visible even when other symptoms are low.
        burden = max(features["symptom_burden"], features["peak_symptom"] * 0.7)
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
            purpose=data.purpose.value,
            symptom_burden=round(burden, 2),
            fatigue=round(features["fatigue"], 2),
            cognitive_load=round(cognitive_load, 2),
            activity_tolerance=round(tolerance, 2),
            trend=trend,
            risk_level=risk_level,
            stage=data.recovery_stage,
        )
