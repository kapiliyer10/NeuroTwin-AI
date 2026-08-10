from backend.schemas.input_schema import InputSchema
from backend.schemas.simulation_schema import SimulationOutcome
from backend.schemas.state_schema import SafetyAssessment


class InterventionEngine:
    def assess_safety(self, data: InputSchema) -> SafetyAssessment:
        reasons: list[str] = []
        if data.severe_or_worsening_headache:
            reasons.append("severe or worsening headache")
        if data.repeated_vomiting:
            reasons.append("repeated vomiting")
        if data.seizure_or_fainting:
            reasons.append("seizure or fainting")
        if data.confusion_or_slurred_speech:
            reasons.append("confusion or slurred speech")
        if data.weakness_numbness_or_vision_change:
            reasons.append("weakness, numbness, or vision change")

        if reasons:
            return SafetyAssessment(
                status="urgent",
                message="Stop the activity and seek urgent medical care now.",
                reasons=reasons,
                seek_urgent_care=True,
            )
        if data.activity_type.value == "sport" and (not data.clinician_evaluated or data.recovery_stage < 4):
            return SafetyAssessment(
                status="contact_professional",
                message="Do not use this app as sport clearance. Stop contact-risk activity and follow your healthcare professional's return-to-sport plan.",
                reasons=["sport activity requires a healthcare professional's clearance"],
            )
        high_symptoms = []
        if data.headache >= 7:
            high_symptoms.append("headache is 7/10 or higher")
        if data.dizziness >= 7:
            high_symptoms.append("dizziness is 7/10 or higher")
        if data.balance_problem >= 7:
            high_symptoms.append("balance problems are 7/10 or higher")
        if high_symptoms:
            return SafetyAssessment(
                status="contact_professional",
                message="Pause the activity and contact your healthcare professional about these symptoms.",
                reasons=high_symptoms,
            )
        if data.symptoms_worsened or data.symptoms_after_activity >= 3:
            return SafetyAssessment(
                status="contact_professional",
                message="Pause or reduce the activity and contact your healthcare professional if symptoms persist or worsen.",
                reasons=["symptoms increased after activity"],
            )
        return SafetyAssessment(
            status="monitor",
            message="Continue monitoring symptoms and follow your healthcare professional's plan.",
        )

    def recommend(self, simulations: dict[str, SimulationOutcome], safety: SafetyAssessment) -> str:
        if safety.seek_urgent_care:
            return "seek_urgent_care"
        if safety.status == "contact_professional":
            return "pause_and_contact_professional"
        action_cost = {"continue_gently": 0.0, "reduce_activity": 0.55, "rest_and_check_in": 1.0}
        return min(
            simulations,
            key=lambda action: (
                simulations[action].projected_symptom_burden * 0.7
                + ((10 - simulations[action].projected_activity_tolerance) * 0.2)
                + action_cost.get(action, 0.5)
            ),
        )
