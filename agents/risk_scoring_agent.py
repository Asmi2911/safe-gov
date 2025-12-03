from typing import Dict, Any, List
import datetime
from tools.storage_tool import append_memory
from tools.logging_tool import log_event

class RiskScoringAgent:
    """Aggregates metrics into an overall risk score and stores it in memory."""

    def __init__(self, policies: List[Dict[str, Any]]):
        self.policies = policies

    def run(self, hallucination_result: Dict[str, Any],
            bias_result: Dict[str, Any],
            safety_result: Dict[str, Any]) -> Dict[str, Any]:
        t = hallucination_result.get("metric_truthfulness")
        b = bias_result.get("metric_bias_fairness")
        s = safety_result.get("metric_safety")

        t_score = 0.5 if t is None else float(t)
        b_score = 0.5 if b is None else float(b)
        s_score = 0.5 if s is None else float(s)

        risk_truth = (1.0 - t_score) * 30
        risk_bias = (1.0 - b_score) * 30
        risk_safety = (1.0 - s_score) * 40
        overall_risk = risk_truth + risk_bias + risk_safety

        result = {
            "timestamp": datetime.datetime.utcnow().isoformat() + "Z",
            "overall_risk": overall_risk,
            "component_risks": {
                "truthfulness": risk_truth,
                "bias": risk_bias,
                "safety": risk_safety,
            },
            "metrics": {
                "truthfulness": t_score,
                "bias_fairness": b_score,
                "safety": s_score,
            },
        }

        append_memory(result)
        log_event("RiskScoringAgent", "Computed risk scores", result)
        return result
