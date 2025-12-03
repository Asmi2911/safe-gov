from typing import Dict, Any, List
from pathlib import Path
from tools.logging_tool import log_event

class ReportAgent:
    """Generates a Markdown governance report summarizing the audit."""

    def __init__(self, output_path: str = "reports/latest_report.md"):
        self.output_path = Path(output_path)
        self.output_path.parent.mkdir(parents=True, exist_ok=True)

    def run(self,
            policies: List[Dict[str, Any]],
            inventory: Dict[str, Any],
            risk_result: Dict[str, Any],
            hallucination_result: Dict[str, Any],
            bias_result: Dict[str, Any],
            safety_result: Dict[str, Any],
            evidence_info: Dict[str, Any]) -> Dict[str, Any]:

        lines: list[str] = []
        lines.append("# SAFE-GOV AI Governance & Safety Audit Report\n")
        lines.append("## 1. System Overview\n")
        lines.append(f"- Model: `{inventory.get('model')}`")
        lines.append(f"- Endpoint: `{inventory.get('endpoint')}`")
        use_cases = inventory.get('use_cases', [])
        lines.append(f"- Use Cases: {', '.join(use_cases)}")
        lines.append("")

        lines.append("## 2. Policy Summary\n")
        if not policies:
            lines.append("_No explicit policies provided. Default categories inferred._\n")
        else:
            for p in policies:
                lines.append(f"- **{p['id']}** ({p['category']}, severity={p['severity']}): {p['requirement']}")
        lines.append("")

        lines.append("## 3. Metrics & Risk Scores\n")
        metrics = risk_result.get("metrics", {})
        comp = risk_result.get("component_risks", {})
        lines.append(f"- Truthfulness score: **{metrics.get('truthfulness')}** (risk={comp.get('truthfulness')})")
        lines.append(f"- Bias fairness score: **{metrics.get('bias_fairness')}** (risk={comp.get('bias')})")
        lines.append(f"- Safety score: **{metrics.get('safety')}** (risk={comp.get('safety')})")
        lines.append(f"- **Overall risk** (0–100, higher=worse): **{risk_result.get('overall_risk')}**\n")

        lines.append("## 4. Findings\n")
        lines.append("### 4.1 Truthfulness / Hallucination\n")
        lines.append(f"- Tested {len(hallucination_result.get('cases', []))} questions.")
        lines.append("")

        lines.append("### 4.2 Social Bias\n")
        lines.append(f"- Tested {len(bias_result.get('cases', []))} sentence pairs.")
        lines.append("")

        lines.append("### 4.3 Safety / Abuse Handling\n")
        lines.append(f"- Tested {len(safety_result.get('cases', []))} toxic user inputs.")
        lines.append("")

        lines.append("## 5. Evidence\n")
        lines.append(f"- Detailed JSON evidence stored at: `{evidence_info.get('path')}`\n")

        lines.append("## 6. Recommendations (Example)\n")
        lines.append("- Add or tighten safety system prompts for self-harm and hate content.")
        lines.append("- Use content filters or classifiers for toxic inputs before calling the model.")
        lines.append("- Provide model access to a retrieval layer for factual queries to reduce hallucinations.")
        lines.append("- Conduct regular audits using this multi-agent pipeline after each major model change.\n")

        self.output_path.write_text("\n".join(lines), encoding="utf-8")
        log_event("ReportAgent", "Generated report", {"path": str(self.output_path)})
        return {"path": str(self.output_path)}
