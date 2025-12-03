# SAFE-GOV AI Governance & Safety Audit Report

## 1. System Overview

- Model: `mock-llm`
- Endpoint: `local-mock`
- Use Cases: demo, governance-audit

## 2. Policy Summary

- **policy_1** (safety, severity=critical): The model must not encourage self-harm or suicide.
- **policy_2** (privacy, severity=critical): The model must not reveal personal identifiable information (PII).
- **policy_3** (safety, severity=high): The model should avoid reinforcing harmful stereotypes or bias.
- **policy_4** (truthfulness, severity=high): The model should aim to provide truthful, fact-based information and avoid hallucinations.

## 3. Metrics & Risk Scores

- Truthfulness score: **0.5** (risk=15.0)
- Bias fairness score: **1.0** (risk=0.0)
- Safety score: **1.0** (risk=0.0)
- **Overall risk** (0–100, higher=worse): **15.0**

## 4. Findings

### 4.1 Truthfulness / Hallucination

- Tested 50 questions.

### 4.2 Social Bias

- Tested 50 sentence pairs.

### 4.3 Safety / Abuse Handling

- Tested 50 toxic user inputs.

## 5. Evidence

- Detailed JSON evidence stored at: `reports\evidence.json`

## 6. Recommendations (Example)

- Add or tighten safety system prompts for self-harm and hate content.
- Use content filters or classifiers for toxic inputs before calling the model.
- Provide model access to a retrieval layer for factual queries to reduce hallucinations.
- Conduct regular audits using this multi-agent pipeline after each major model change.
