from backend.schemas.input_schema import InputSchema, Purpose


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
        features = {
            "symptom_burden": sum(symptom_values) / len(symptom_values),
            "peak_symptom": float(max(symptom_values)),
            "cognitive_load": sum(cognitive) / len(cognitive),
            "fatigue": float(data.fatigue),
            "activity_load": min(data.activity_minutes / 60, 10),
            "post_activity_change": float(data.symptoms_after_activity),
        }
        if data.purpose == Purpose.mental_wellbeing:
            wellbeing_values = [
                data.stress_level,
                10 - data.mood,
                10 - data.sleep_quality,
                data.concentration_difficulty,
                data.workload_pressure,
                10 - data.social_connection,
            ]
            features.update(
                symptom_burden=sum(wellbeing_values) / len(wellbeing_values),
                peak_symptom=float(max(wellbeing_values)),
                cognitive_load=float(data.concentration_difficulty),
                fatigue=float(max(data.fatigue, 10 - data.sleep_quality)),
            )
        return features
