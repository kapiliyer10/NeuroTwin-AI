RISK_TERMS = ("diagnosis", "diagnose", "treatment", "prescription", "disorder")


def validate_output(text: str) -> str:
    lowered = text.lower()
    if any(term in lowered for term in RISK_TERMS):
        return (
            "This system cannot provide medical diagnosis or treatment. "
            "Please consult a qualified professional for health-related concerns."
        )
    return text
