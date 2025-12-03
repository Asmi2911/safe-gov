from pathlib import Path
from typing import List, Dict

from tools.logging_tool import log_event

class PolicyLoaderAgent:
    """Loads policy documents and extracts a simple structured list of requirements."""

    def __init__(self, policy_path: str = "data/sample_policies/sample_policy.md"):
        self.policy_path = Path(policy_path)

    def run(self) -> List[Dict]:
        if not self.policy_path.exists():
            log_event("PolicyLoaderAgent", "Policy file not found", {"path": str(self.policy_path)})
            return []

        text = self.policy_path.read_text(encoding="utf-8")
        policies: List[Dict] = []
        for line in text.splitlines():
            stripped = line.strip()
            if stripped.startswith(("-", "*")) and len(stripped) > 2:
                requirement = stripped.lstrip("-* ").strip()
                policies.append({
                    "id": f"policy_{len(policies)+1}",
                    "requirement": requirement,
                    "category": self._infer_category(requirement),
                    "severity": self._infer_severity(requirement),
                })

        log_event("PolicyLoaderAgent", "Extracted policies", {"count": len(policies)})
        return policies

    @staticmethod
    def _infer_category(requirement: str) -> str:
        r = requirement.lower()
        if "harm" in r or "self-harm" in r or "violence" in r:
            return "safety"
        if "pii" in r or "privacy" in r or "personal data" in r:
            return "privacy"
        if "bias" in r or "fair" in r or "discrimination" in r:
            return "bias"
        if "truth" in r or "hallucination" in r:
            return "truthfulness"
        return "general"

    @staticmethod
    def _infer_severity(requirement: str) -> str:
        r = requirement.lower()
        if any(word in r for word in ["must not", "never", "prohibited", "forbidden"]):
            return "critical"
        if any(word in r for word in ["should not", "avoid"]):
            return "high"
        return "medium"
