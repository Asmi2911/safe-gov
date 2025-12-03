from typing import Dict, Any
from pathlib import Path
import json
from tools.logging_tool import log_event

class EvidenceCollectorAgent:
    """Collects examples of violations and stores them as JSON for audit traceability."""

    def __init__(self, output_path: str = "reports/evidence.json"):
        self.output_path = Path(output_path)
        self.output_path.parent.mkdir(parents=True, exist_ok=True)

    def run(self,
            hallucination_result: Dict[str, Any],
            bias_result: Dict[str, Any],
            safety_result: Dict[str, Any]) -> Dict[str, Any]:
        evidence = {
            "hallucination_cases": hallucination_result.get("cases", [])[:20],
            "bias_cases": bias_result.get("cases", [])[:20],
            "safety_cases": safety_result.get("cases", [])[:20],
        }
        with self.output_path.open("w", encoding="utf-8") as f:
            json.dump(evidence, f, indent=2)
        log_event("EvidenceCollectorAgent", "Saved evidence", {"path": str(self.output_path)})
        return {"path": str(self.output_path)}
