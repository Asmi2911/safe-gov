import streamlit as st
from agents.orchestrator import Orchestrator

st.set_page_config(page_title="SAFE-GOV Auditor", layout="wide")

st.title("SAFE-GOV: AI Governance & Safety Auditor")

st.markdown(
"""
This app runs a **multi-agent audit** of an LLM-based system on:

- Truthfulness / hallucination (TruthfulQA)
- Social bias (CrowS-Pairs)
- Safety / toxicity handling (Jigsaw)

Click **Run Audit** to execute the full pipeline.
"""
)

if "last_result" not in st.session_state:
    st.session_state.last_result = None

if st.button("🚀 Run Audit"):
    with st.spinner("Running multi-agent audit..."):
        system_config = {
            "model": "mock-llm",
            "endpoint": "local-mock",
            "use_cases": ["demo", "governance-audit"],
            "max_tokens": 256,
        }
        orchestrator = Orchestrator(system_config=system_config)
        result = orchestrator.run_full_audit()
        st.session_state.last_result = result
    st.success("Audit completed!")

result = st.session_state.last_result

if result is not None:
    risk = result["risk_result"]
    metrics = risk["metrics"]
    comp_risks = risk["component_risks"]

    st.subheader("Overall Risk Summary")

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Overall Risk (0–100)", f"{risk['overall_risk']:.1f}")
    with col2:
        st.metric("Truthfulness", f"{metrics['truthfulness']:.2f}")
    with col3:
        st.metric("Bias Fairness", f"{metrics['bias_fairness']:.2f}")
    with col4:
        st.metric("Safety", f"{metrics['safety']:.2f}")

    st.markdown("---")
    st.subheader("Evaluation Decision")
    eval_res = result["evaluation"]
    st.write(f"**Status:** {eval_res['status']}")
    st.write(eval_res["recommendation"])

    st.markdown("---")
    st.subheader("Sample Findings")

    import pandas as pd

    # Show a few hallucination cases
    hallu_cases = result["hallucination_result"].get("cases", [])[:5]
    if hallu_cases:
        st.markdown("### Truthfulness / Hallucination (sample)")
        st.dataframe(pd.DataFrame(hallu_cases)[["question", "model_answer", "true_answer", "score"]])

    bias_cases = result["bias_result"].get("cases", [])[:5]
    if bias_cases:
        st.markdown("### Social Bias (sample)")
        st.dataframe(pd.DataFrame(bias_cases)[["bias_type", "stereotype_sentence", "anti_stereotype_sentence", "score"]])

    safety_cases = result["safety_result"].get("cases", [])[:5]
    if safety_cases:
        st.markdown("### Safety / Toxicity Handling (sample)")
        st.dataframe(pd.DataFrame(safety_cases)[["user_comment", "model_reply", "safety_label"]])

    st.markdown("---")
    st.markdown(
        f"📄 Full markdown report written to: `reports/latest_report.md`  \n"
        f"🧾 Evidence JSON written to: `reports/evidence.json`"
    )
else:
    st.info("Click **Run Audit** to generate the first report.")
