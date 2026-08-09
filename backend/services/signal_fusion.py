from backend.schemas.input_schema import InputSchema


class SignalFusion:
    """Convert raw behavioral signals into model-ready features."""

    def extract(self, data: InputSchema) -> list[float]:
        typing_norm = min(data.typing_speed / 100, 1.0)
        pause_norm = min(data.pause_variance / 5, 1.0)
        sentiment_norm = (data.sentiment + 1) / 2
        screen_norm = min(data.screen_time / 12, 1.0)
        return [typing_norm, pause_norm, sentiment_norm, screen_norm]
