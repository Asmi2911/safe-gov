from agents.orchestrator import Orchestrator

def main():
    system_config = {
        "model": "mock-llm",
        "endpoint": "local-mock",
        "use_cases": ["demo", "governance-audit"],
        "max_tokens": 256,
    }
    orchestrator = Orchestrator(system_config=system_config)
    result = orchestrator.run_full_audit()
    print("=== SAFE-GOV Audit Completed ===")
    print(f"Report: {result['report_info']['path']}")
    print(f"Overall risk: {result['risk_result']['overall_risk']}")
    print(f"Evaluation: {result['evaluation']['status']} - {result['evaluation']['recommendation']}")

if __name__ == "__main__":
    main()
