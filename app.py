import streamlit as st
import json
import pandas as pd

from pipeline import extract_intent, system_design, generate_schema
from validator import validate_config, repair_config
from runtime import simulate_runtime
from evaluator import evaluate_prompt
from sample_prompts import PRODUCT_PROMPTS, EDGE_CASES


st.set_page_config(
    page_title="BuildForge AI",
    page_icon="✨",
    layout="wide"
)

st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #f8fafc, #eef2ff, #fdf2f8);
    color: #1e293b;
}

.block-container {
    padding-top: 2rem;
}

h1, h2, h3, p, label {
    color: #1e293b !important;
}

.main-title {
    font-size: 50px;
    font-weight: 900;
    text-align: center;
    background: linear-gradient(90deg, #2563eb, #7c3aed, #db2777);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.subtitle {
    text-align: center;
    font-size: 18px;
    color: #475569 !important;
    margin-bottom: 30px;
}

.hero-card {
    background: rgba(255, 255, 255, 0.9);
    padding: 26px;
    border-radius: 24px;
    border: 1px solid #e2e8f0;
    box-shadow: 0 14px 40px rgba(99, 102, 241, 0.18);
    margin-bottom: 24px;
}

.stage {
    background: #ffffff;
    padding: 18px;
    border-radius: 18px;
    border-left: 6px solid #7c3aed;
    box-shadow: 0 8px 24px rgba(124, 58, 237, 0.12);
    margin-top: 20px;
    margin-bottom: 14px;
}

.success-box {
    background: #ecfdf5;
    border: 1px solid #22c55e;
    padding: 15px;
    border-radius: 14px;
    color: #166534;
    font-weight: 600;
}

.error-box {
    background: #fef2f2;
    border: 1px solid #ef4444;
    padding: 15px;
    border-radius: 14px;
    color: #991b1b;
    font-weight: 600;
}

.info-box {
    background: #eff6ff;
    border: 1px solid #93c5fd;
    padding: 15px;
    border-radius: 14px;
    color: #1e40af;
    font-weight: 600;
}

div.stButton > button {
    background: linear-gradient(90deg, #2563eb, #7c3aed, #db2777);
    color: white;
    border: none;
    border-radius: 16px;
    padding: 0.8rem 1.6rem;
    font-weight: 800;
    font-size: 16px;
    box-shadow: 0 8px 20px rgba(124, 58, 237, 0.25);
}

div.stButton > button:hover {
    background: linear-gradient(90deg, #1d4ed8, #6d28d9, #be185d);
    color: white;
    transform: scale(1.02);
}

textarea {
    border-radius: 16px !important;
    border: 1px solid #c7d2fe !important;
    background-color: #ffffff !important;
    color: #1e293b !important;
}

[data-testid="stMetric"] {
    background: #ffffff;
    padding: 18px;
    border-radius: 18px;
    border: 1px solid #e0e7ff;
    box-shadow: 0 8px 24px rgba(37, 99, 235, 0.12);
}

[data-testid="stMetricValue"] {
    color: #7c3aed;
}

[data-testid="stTabs"] button {
    color: #1e293b;
    font-weight: 700;
}

pre {
    border-radius: 16px !important;
}
</style>
""", unsafe_allow_html=True)


st.markdown('<div class="main-title">BuildForge AI</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="subtitle">Forge complete app blueprints from natural language using structured JSON, validation, repair, and runtime simulation.</div>',
    unsafe_allow_html=True
)

tab1, tab2 = st.tabs(["🚀 Generate App Config", "📊 Evaluation Metrics"])


with tab1:
    st.markdown('<div class="hero-card">', unsafe_allow_html=True)

    user_prompt = st.text_area(
        "Enter Product Requirement",
        value="Build a CRM with login, contacts, dashboard, role-based access, premium plan with payments, and admin analytics.",
        height=130
    )

    generate_btn = st.button("✨ Generate Application Config")

    st.markdown('</div>', unsafe_allow_html=True)

    if generate_btn:
        intent = extract_intent(user_prompt)
        design = system_design(intent)
        config = generate_schema(intent, design)

        st.markdown('<div class="stage"><h3>Stage 1: Intent Extraction</h3></div>', unsafe_allow_html=True)
        st.json(intent)

        st.markdown('<div class="stage"><h3>Stage 2: System Design Layer</h3></div>', unsafe_allow_html=True)
        st.json(design)

        st.markdown('<div class="stage"><h3>Stage 3: Schema Generation</h3></div>', unsafe_allow_html=True)
        st.json(config)

        st.markdown('<div class="stage"><h3>Stage 4: Validation + Repair Engine</h3></div>', unsafe_allow_html=True)

        is_valid, errors, validated = validate_config(config)

        if is_valid:
            st.markdown(
                '<div class="success-box">✅ Config is valid. No repair required.</div>',
                unsafe_allow_html=True
            )
        else:
            st.markdown(
                '<div class="error-box">❌ Validation failed. Repair engine started.</div>',
                unsafe_allow_html=True
            )
            st.write(errors)

            config = repair_config(config)
            is_valid, errors, validated = validate_config(config)

            if is_valid:
                st.markdown(
                    '<div class="success-box">✅ Config repaired successfully.</div>',
                    unsafe_allow_html=True
                )
            else:
                st.markdown(
                    '<div class="error-box">❌ Repair failed.</div>',
                    unsafe_allow_html=True
                )
                st.write(errors)

        st.markdown('<div class="stage"><h3>Stage 5: Runtime Simulation</h3></div>', unsafe_allow_html=True)

        runtime_ok, runtime_message = simulate_runtime(config)

        if runtime_ok:
            st.markdown(
                f'<div class="success-box">✅ {runtime_message}</div>',
                unsafe_allow_html=True
            )
        else:
            st.markdown(
                f'<div class="error-box">❌ {runtime_message}</div>',
                unsafe_allow_html=True
            )

        st.markdown('<div class="stage"><h3>Final Executable JSON Output</h3></div>', unsafe_allow_html=True)
        st.code(json.dumps(config, indent=4), language="json")


with tab2:
    st.markdown('<div class="hero-card">', unsafe_allow_html=True)

    st.subheader("Evaluation Framework")
    st.markdown(
        '<div class="info-box">Runs real product prompts and edge cases to measure success rate, retries, failures, and latency.</div>',
        unsafe_allow_html=True
    )

    st.write("")

    if st.button("📊 Run Evaluation"):
        prompts = PRODUCT_PROMPTS + EDGE_CASES
        results = []

        for prompt in prompts:
            results.append(evaluate_prompt(prompt))

        df = pd.DataFrame(results)

        success_rate = round((df["success"].sum() / len(df)) * 100, 2)
        avg_retries = round(df["retries"].mean(), 2)
        avg_latency = round(df["latency_seconds"].mean(), 4)

        col1, col2, col3 = st.columns(3)
        col1.metric("Success Rate", f"{success_rate}%")
        col2.metric("Average Retries", avg_retries)
        col3.metric("Average Latency", avg_latency)

        st.dataframe(df, use_container_width=True)

    st.markdown('</div>', unsafe_allow_html=True)