from backend.schemas.state_schema import CognitiveState


def _clamp(value: float) -> float:
    return round(max(0.0, min(1.0, value)), 3)


class StateModel:
    """Deterministic starter model that can be swapped for a trained model later."""

    def predict(self, features: list[float]) -> CognitiveState:
        typing_norm, pause_norm, sentiment_norm, screen_norm = features

        stress = (pause_norm * 0.35) + (screen_norm * 0.25) + ((1 - sentiment_norm) * 0.35)
        fatigue = (screen_norm * 0.45) + (pause_norm * 0.3) + ((1 - typing_norm) * 0.15)
        attention = 1 - ((pause_norm * 0.4) + (fatigue * 0.35) + (stress * 0.15))
        emotion = sentiment_norm * 0.75 + (attention * 0.15) + ((1 - stress) * 0.1)

        return CognitiveState(
            stress=_clamp(stress),
            fatigue=_clamp(fatigue),
            attention=_clamp(attention),
            emotion=_clamp(emotion),
        )
