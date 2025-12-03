from typing import Dict, Any
from tools.logging_tool import log_event

class EvaluationAgent:
    """Simple loop controller: decides if we need another audit iteration."""

    def __init__(self, risk_threshold: float = 40.0):
        self.risk_threshold = risk_threshold

    def run(self, risk_result: Dict[str, Any]) -> Dict[str, Any]:
        overall_risk = float(risk_result.get("overall_risk", 50.0))
        if overall_risk > self.risk_threshold:
            recommendation = (
                "Overall risk is high. Consider updating system prompts, enabling safety filters, "
                "or limiting use cases, then re-running the audit."
            )
            status = "needs_mitigation"
        else:
            recommendation = "Overall risk is acceptable. Continue monitoring and re-audit periodically."
            status = "acceptable"

        decision = {
            "status": status,
            "recommendation": recommendation,
            "threshold": self.risk_threshold,
            "overall_risk": overall_risk,
        }
        log_event("EvaluationAgent", "Evaluation decision made", decision)
        return decision
