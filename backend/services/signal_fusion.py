from backend.schemas.input_schema import InputSchema


class SignalFusion:
    """Convert a check-in into transparent, concussion-relevant features."""

    def extract(self, data: InputSchema) -> dict[str, float]:
        symptom_values = [
            data.headache,
            data.dizziness,
            data.nausea,
            data.light_sensitivity,
            data.noise_sensitivity,
            data.fatigue,
            data.memory_difficulty,
            data.concentration_difficulty,
            data.balance_problem,
            data.mood_change,
        ]
        cognitive = [data.memory_difficulty, data.concentration_difficulty]
        return {
            "symptom_burden": sum(symptom_values) / len(symptom_values),
            "peak_symptom": float(max(symptom_values)),
            "cognitive_load": sum(cognitive) / len(cognitive),
            "fatigue": float(data.fatigue),
            "activity_load": min(data.activity_minutes / 60, 10),
            "post_activity_change": float(data.symptoms_after_activity),
        }
