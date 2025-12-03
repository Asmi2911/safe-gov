from typing import Dict, Any

from agents.policy_loader_agent import PolicyLoaderAgent
from agents.system_inventory_agent import SystemInventoryAgent
from agents.test_planner_agent import TestPlannerAgent
from agents.hallucination_tester_agent import HallucinationTesterAgent
from agents.bias_tester_agent import BiasTesterAgent
from agents.safety_tester_agent import SafetyTesterAgent
from agents.risk_scoring_agent import RiskScoringAgent
from agents.evidence_collector_agent import EvidenceCollectorAgent
from agents.report_agent import ReportAgent
from agents.evaluation_agent import EvaluationAgent
from tools.logging_tool import log_event

class Orchestrator:
    """Coordinates the full SAFE-GOV multi-agent audit."""

    def __init__(self, system_config: Dict[str, Any] | None = None):
        self.system_config = system_config or {}

    def run_full_audit(self) -> Dict[str, Any]:
        log_event("Orchestrator", "Starting audit", self.system_config)

        policy_agent = PolicyLoaderAgent()
        policies = policy_agent.run()

        inventory_agent = SystemInventoryAgent(self.system_config)
        inventory = inventory_agent.run()

        planner = TestPlannerAgent(policies, inventory)
        tests = planner.run()

        hallucination_agent = HallucinationTesterAgent()
        bias_agent = BiasTesterAgent()
        safety_agent = SafetyTesterAgent()

        hallucination_result = hallucination_agent.run()
        bias_result = bias_agent.run()
        safety_result = safety_agent.run()

        risk_agent = RiskScoringAgent(policies)
        risk_result = risk_agent.run(
            hallucination_result=hallucination_result,
            bias_result=bias_result,
            safety_result=safety_result,
        )

        evidence_agent = EvidenceCollectorAgent()
        evidence_info = evidence_agent.run(
            hallucination_result=hallucination_result,
            bias_result=bias_result,
            safety_result=safety_result,
        )

        report_agent = ReportAgent()
        report_info = report_agent.run(
            policies=policies,
            inventory=inventory,
            risk_result=risk_result,
            hallucination_result=hallucination_result,
            bias_result=bias_result,
            safety_result=safety_result,
            evidence_info=evidence_info,
        )

        eval_agent = EvaluationAgent()
        evaluation = eval_agent.run(risk_result)

        result = {
            "policies": policies,
            "inventory": inventory,
            "tests": tests,
            "hallucination_result": hallucination_result,
            "bias_result": bias_result,
            "safety_result": safety_result,
            "risk_result": risk_result,
            "evidence_info": evidence_info,
            "report_info": report_info,
            "evaluation": evaluation,
        }
        log_event("Orchestrator", "Audit completed", {
            "report_path": report_info.get("path"),
            "overall_risk": risk_result.get("overall_risk"),
        })
        return result
