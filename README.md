Got you, let’s upgrade the README to include the Streamlit frontend ✨
Here’s a **full, copy-paste-ready `README.md`** for your project:

````markdown
# SAFE-GOV: Multi-Agent AI Governance & Safety Auditor  
**Track:** Enterprise Agents

SAFE-GOV is a **multi-agent system** that automatically audits an LLM-based application for:

- **Truthfulness / Hallucinations** (using a subset of **TruthfulQA**)  
- **Social Bias / Fairness** (using a subset of **CrowS-Pairs**)  
- **Safety / Toxicity Handling** (using a subset of **Jigsaw Toxic Comments**)

It produces:

- A **Markdown governance report** with risk scores  
- A detailed **evidence JSON** of tested cases  
- **Logs** for every agent step  
- A simple **Streamlit dashboard frontend** for interactive use

This project implements the key ideas from the **Google 5-Day AI Agents Intensive**: multi-agent orchestration, tools, memory, observability, and evaluation.

---

## 1. Problem & Motivation

Enterprises are rapidly deploying LLMs into production (customer support, internal tools, analytics), but:

- Models **hallucinate** and return incorrect facts  
- Outputs may contain **social bias**  
- Systems can respond **unsafely** to abusive or harmful prompts  

Manual auditing is:

- Slow  
- Inconsistent  
- Hard to scale  

> **Goal:** Build a reusable, automated **AI Governance Auditor** that can evaluate any LLM-based system on truthfulness, bias, and safety.

---

## 2. Solution: SAFE-GOV

SAFE-GOV is a **multi-agent governance pipeline** that:

1. Loads and interprets simple AI policy requirements  
2. Builds a system inventory (model, endpoint, use cases)  
3. Plans tests based on policies  
4. Runs:
   - Hallucination tests using **TruthfulQA subset**
   - Bias tests using **CrowS-Pairs subset**
   - Safety tests using **Jigsaw Toxic Comments subset**
5. Aggregates metrics into **risk scores**  
6. Stores evidence and risk history in a **memory bank**  
7. Generates a **human-readable markdown report**  
8. Provides a **Streamlit dashboard** for interactive exploration  

---

## 3. Architecture & Agents

SAFE-GOV consists of multiple cooperating agents:

- **PolicyLoaderAgent**  
  - Loads `data/sample_policies/sample_policy.md` and extracts requirements  
  - Infers categories: `safety`, `truthfulness`, `bias`, `privacy`, etc.

- **SystemInventoryAgent**  
  - Captures system config (model name, endpoint, use cases)

- **TestPlannerAgent**  
  - Maps policies to tests: hallucination / bias / safety

- **HallucinationTesterAgent**  
  - Uses `truthfulqa_small.json` subset  
  - Asks questions, judges truthfulness, outputs `metric_truthfulness`

- **BiasTesterAgent**  
  - Uses `crows_pairs_small.json` subset  
  - Compares stereotype vs anti-stereotype pairs, outputs `metric_bias_fairness`

- **SafetyTesterAgent**  
  - Uses `jigsaw_toxic_small.csv` subset  
  - Feeds toxic comments as prompts, evaluates model replies, outputs `metric_safety`

- **RiskScoringAgent**  
  - Aggregates metrics into an **overall risk score (0–100)**  
  - Stores history in `data/memory/memory.json`

- **EvidenceCollectorAgent**  
  - Saves example cases (hallucination, bias, safety) to `reports/evidence.json`

- **ReportAgent**  
  - Generates `reports/latest_report.md` summarizing policies, metrics, risks, and recommendations

- **EvaluationAgent**  
  - Checks if overall risk is below a threshold  
  - Returns `"acceptable"` or `"needs_mitigation"` with suggestions

All of these are orchestrated by:

- **Orchestrator** (`agents/orchestrator.py`)  
  - Runs the full pipeline sequentially and returns a structured result.

---

## 4. Datasets

SAFE-GOV uses **small, curated subsets** (created from Kaggle datasets) to keep the project light and reproducible:

- **Truthfulness / Hallucination**
  - Source: TruthfulQA (Kaggle)
  - Stored as: `data/hallucination/truthfulqa_small.json`  

- **Bias / Fairness**
  - Source: CrowS-Pairs (Kaggle)
  - Stored as: `data/bias/crows_pairs_small.json`  

- **Safety / Toxicity**
  - Source: Jigsaw Toxic Comment Classification (Kaggle)
  - Stored as: `data/safety/jigsaw_toxic_small.csv`  

A helper script `prepare_subsets.py` can create these small files from the original Kaggle CSVs.

---

## 5. Installation

Clone the repository and install dependencies:

```bash
pip install -r requirements.txt
````

This will install:

* `pandas`
* `numpy`
* `python-dateutil`
* `streamlit`
* and other lightweight dependencies

---

## 6. Preparing Dataset Subsets

If the small subsets are not already present, run:

```bash
python prepare_subsets.py
```

This script:

* Reads:

  * `data/hallucination/generation_validation.csv`
  * `data/bias/crows_pairs_anonymized.csv`
  * `data/safety/train.csv`
* Samples a limited number of rows
* Writes:

```text
data/hallucination/truthfulqa_small.json
data/bias/crows_pairs_small.json
data/safety/jigsaw_toxic_small.csv
```

If your column names differ from the defaults in `prepare_subsets.py`, adjust that script accordingly.

---

## 7. Running the Backend Audit (CLI)

To run the full multi-agent audit from the command line:

```bash
python main.py
```

This will:

* Run the full pipeline
* Print a short summary to the console
* Generate:

```text
reports/latest_report.md      # main audit report
reports/evidence.json         # detailed cases (hallucination, bias, safety)
logs/events.jsonl             # observability logs for each agent
data/memory/memory.json       # audit history (long-term memory)
```

You can open `reports/latest_report.md` in any markdown viewer or editor (VSCode, browser extension, etc.).

---

## 8. Streamlit Frontend (Dashboard)

SAFE-GOV includes a **simple, optional Streamlit dashboard** that makes the system feel like an internal governance tool.

Run:

```bash
streamlit run app.py
```

This will open a local web app with:

* A **“🚀 Run Audit”** button
* Top-level metrics for:

  * Overall risk (0–100)
  * Truthfulness score
  * Bias fairness score
  * Safety score
* Sample tables showing:

  * TruthfulQA questions, model answers, scores
  * CrowS-Pairs stereotype vs anti-stereotype sentences
  * Jigsaw toxic comments and model replies

At the bottom, the app links to:

* `reports/latest_report.md`
* `reports/evidence.json`

This frontend is purely **read/write on top of the same orchestrator**, so the core logic stays in the backend agents.

---

## 9. Model Backend (Mock vs Real)

By default, `tools/model_api_tool.py` uses a **mock model** so that the project:

* Runs everywhere
* Requires **no API keys**
* Is safe for offline execution

If desired, you can extend `call_model()` to integrate **Gemini** (or another LLM) via environment variables like:

```bash
export USE_GEMINI=1
export GOOGLE_API_KEY="your-key-here"
```

and update `model_api_tool.py` accordingly, while keeping mock mode as the default fallback.

---

## 10. Project Structure

```text
safe-gov/
│
├── agents/
│   ├── orchestrator.py
│   ├── policy_loader_agent.py
│   ├── system_inventory_agent.py
│   ├── test_planner_agent.py
│   ├── hallucination_tester_agent.py
│   ├── bias_tester_agent.py
│   ├── safety_tester_agent.py
│   ├── risk_scoring_agent.py
│   ├── evidence_collector_agent.py
│   ├── report_agent.py
│   └── evaluation_agent.py
│
├── tools/
│   ├── dataset_loader_tool.py
│   ├── model_api_tool.py
│   ├── logging_tool.py
│   └── storage_tool.py
│
├── data/
│   ├── hallucination/
│   ├── bias/
│   ├── safety/
│   └── memory/
│
├── reports/
├── logs/
├── main.py
├── app.py                  # Streamlit frontend
├── prepare_subsets.py
├── architecture.md
└── README.md
```

---

## 11. Features Mapped to Course Concepts

This project demonstrates **multiple** core features from the Agents Intensive:

* **Multi-Agent System**

  * Multiple cooperating agents with clear responsibilities
* **Tools**

  * Dataset loading, model abstraction, logging, storage / memory tools
* **Sessions & Memory**

  * Long-term risk history in `data/memory/memory.json`
* **Context Engineering / Compaction**

  * Uses dataset subsets and focused prompts per risk type
* **Observability**

  * Structured JSONL logs in `logs/events.jsonl`
* **Evaluation & A2A-style Flow**

  * `EvaluationAgent` controlling “acceptable vs needs mitigation” status
* **Deployment-Ready UX**

  * CLI entrypoint + Streamlit dashboard frontend

SAFE-GOV aims to look and behave like a realistic **internal AI governance tool** for enterprise teams.


