from typing import List, Dict, Any
from tools.logging_tool import log_event

class TestPlannerAgent:
    """Maps policy requirements + system inventory into a set of tests to run."""

    def __init__(self, policies: List[Dict[str, Any]], inventory: Dict[str, Any]):
        self.policies = policies
        self.inventory = inventory

    def run(self) -> List[Dict[str, Any]]:
        tests: List[Dict[str, Any]] = []

        for policy in self.policies:
            category = policy.get("category", "general")
            if category == "truthfulness":
                tests.append({
                    "id": f"test_truth_{policy['id']}",
                    "type": "hallucination",
                    "policy_id": policy["id"],
                })
            elif category == "bias":
                tests.append({
                    "id": f"test_bias_{policy['id']}",
                    "type": "bias",
                    "policy_id": policy["id"],
                })
            elif category == "safety":
                tests.append({
                    "id": f"test_safety_{policy['id']}",
                    "type": "safety",
                    "policy_id": policy["id"],
                })

        if not any(t["type"] == "hallucination" for t in tests):
            tests.append({"id": "test_truth_default", "type": "hallucination", "policy_id": None})
        if not any(t["type"] == "bias" for t in tests):
            tests.append({"id": "test_bias_default", "type": "bias", "policy_id": None})
        if not any(t["type"] == "safety" for t in tests):
            tests.append({"id": "test_safety_default", "type": "safety", "policy_id": None})

        log_event("TestPlannerAgent", "Planned tests", {"count": len(tests)})
        return tests
