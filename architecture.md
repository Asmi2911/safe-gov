# SAFE-GOV Architecture

## Overview

SAFE-GOV is designed as a **multi-agent governance pipeline**:

1. **PolicyLoaderAgent** – Parses markdown policy files into structured requirements.
2. **SystemInventoryAgent** – Describes the audited system (model, endpoint, use cases).
3. **TestPlannerAgent** – Maps policies into planned test types.
4. **HallucinationTesterAgent** – Uses TruthfulQA-style questions to test truthfulness.
5. **BiasTesterAgent** – Uses CrowS-Pairs-style pairs to test social bias.
6. **SafetyTesterAgent** – Uses Jigsaw toxic comments to simulate adversarial abuse inputs.
7. **RiskScoringAgent** – Aggregates metrics into an overall risk score and stores history in a memory JSON.
8. **EvidenceCollectorAgent** – Saves example cases as JSON evidence.
9. **ReportAgent** – Generates a human-readable Markdown governance report.
10. **EvaluationAgent** – Decides whether the risk is acceptable or another mitigation loop is needed.

## Data Flow

User / CLI → Orchestrator → PolicyLoaderAgent → SystemInventoryAgent → TestPlannerAgent →  
HallucinationTesterAgent + BiasTesterAgent + SafetyTesterAgent → RiskScoringAgent →  
EvidenceCollectorAgent → ReportAgent → EvaluationAgent

All agents write logs to `logs/events.jsonl`, and the risk history is stored in `data/memory/memory.json`.
