# src/person_b/app.py
# ──────────────────────────────────────────────────────────────
# Task 5 config flag — flip to True once Person A delivers
# scoring_service.py, then the real ML model + BigQuery are used.
# ──────────────────────────────────────────────────────────────
import sys
import os
import time

# Ensure imports resolve regardless of how streamlit is launched
sys.path.insert(0, os.path.dirname(__file__))
# Allow importing from src directory (for person_b packages)
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
# Allow importing from root directory (for src.person_a imports)
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

# Real ML model + BigQuery scoring from Person A
from src.person_a.scoring_service import score_applicant, get_cohort_default_rate

from person_b.explain_api import explain_risk
from person_b.decision_engine import recommend_decision

import streamlit as st

# ──────────────────────────────────────────────────────────────
# Page config & custom CSS
# ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Loan Underwriting Decision Analyzer",
    page_icon="🏦",
    layout="wide",
)

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

    /* ── Global reset ─────────────────────────────────── */
    html, body, [class*="st-"] {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }
    .block-container { padding-top: 1.5rem; }
    h1, h2, h3, h4, h5, h6 {
        font-family: 'Inter', sans-serif !important;
        font-weight: 600 !important;
        color: #1e293b;
    }

    /* ── Header ───────────────────────────────────────── */
    .main-header {
        background: linear-gradient(135deg, #0f172a 0%, #1e293b 50%, #334155 100%);
        padding: 1.6rem 2rem;
        border-radius: 14px;
        margin-bottom: 1.5rem;
        color: white;
        box-shadow: 0 4px 24px rgba(15, 23, 42, 0.18);
    }
    .main-header h1 {
        margin: 0; font-size: 1.7rem; font-weight: 700;
        letter-spacing: -0.4px;
    }
    .main-header p {
        margin: 0.3rem 0 0 0; opacity: 0.7; font-size: 0.85rem;
        font-weight: 400; letter-spacing: 0.2px;
    }

    /* ── Metric cards ─────────────────────────────────── */
    .metric-card {
        background: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 10px;
        padding: 1.1rem 1.2rem;
        text-align: center;
        box-shadow: 0 1px 4px rgba(0,0,0,0.04);
        transition: transform 0.15s ease, box-shadow 0.15s ease;
    }
    .metric-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(0,0,0,0.08);
    }
    .metric-card .label {
        font-size: 0.7rem; text-transform: uppercase;
        letter-spacing: 0.8px; color: #64748b;
        margin-bottom: 0.25rem; font-weight: 500;
    }
    .metric-card .value {
        font-size: 2rem; font-weight: 700; line-height: 1.1;
    }

    /* ── Decision badges ──────────────────────────────── */
    .decision-badge {
        display: inline-block;
        padding: 0.5rem 1.4rem;
        border-radius: 50px;
        font-weight: 700;
        font-size: 1rem;
        letter-spacing: 0.4px;
    }
    .badge-approve  { background: #d1fae5; color: #065f46; border: 2px solid #6ee7b7; }
    .badge-review   { background: #fef3c7; color: #92400e; border: 2px solid #fcd34d; }
    .badge-decline  { background: #fee2e2; color: #991b1b; border: 2px solid #fca5a5; }

    /* ── Explanation box ──────────────────────────────── */
    .explanation-box {
        background: #f8fafc;
        border-left: 3px solid #6366f1;
        border-radius: 0 8px 8px 0;
        padding: 1rem 1.2rem;
        font-size: 0.9rem;
        line-height: 1.65;
        color: #334155;
    }

    /* ── Confidence tag ───────────────────────────────── */
    .confidence-tag {
        display: inline-block;
        padding: 0.2rem 0.6rem;
        border-radius: 5px;
        font-size: 0.75rem;
        font-weight: 600;
    }
    .conf-high   { background: #dbeafe; color: #1e40af; }
    .conf-medium { background: #fef9c3; color: #854d0e; }
    .conf-low    { background: #fce7f3; color: #9d174d; }

    /* ── Form styling ─────────────────────────────────── */
    div[data-testid="stForm"] {
        background: #f8fafc;
        border: 1px solid #e2e8f0;
        border-radius: 12px;
        padding: 1.4rem;
    }

    /* ── Button ───────────────────────────────────────── */
    .stButton > button {
        background: linear-gradient(135deg, #4f46e5, #7c3aed);
        color: white;
        border: none;
        padding: 0.65rem 2rem;
        border-radius: 8px;
        font-weight: 600;
        font-size: 0.95rem;
        letter-spacing: 0.2px;
        transition: all 0.2s ease;
        width: 100%;
    }
    .stButton > button:hover {
        transform: translateY(-1px);
        box-shadow: 0 4px 14px rgba(79, 70, 229, 0.35);
    }

    /* ── Agent pipeline tracker ───────────────────────── */
    .pipeline-tracker {
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 0;
        margin: 0.8rem 0 1.2rem 0;
        padding: 0.8rem 0.5rem;
        background: #f8fafc;
        border: 1px solid #e2e8f0;
        border-radius: 10px;
    }
    .pipeline-step {
        display: flex;
        flex-direction: column;
        align-items: center;
        gap: 0.3rem;
        min-width: 80px;
    }
    .pipeline-circle {
        width: 32px; height: 32px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 0.7rem;
        font-weight: 700;
        color: #94a3b8;
        background: #e2e8f0;
        border: 2px solid #cbd5e1;
        transition: all 0.2s ease;
    }
    .pipeline-circle.active {
        background: #4f46e5;
        color: #ffffff;
        border-color: #4f46e5;
        box-shadow: 0 0 0 3px rgba(79, 70, 229, 0.2);
    }
    .pipeline-circle.done {
        background: #d1fae5;
        color: #065f46;
        border-color: #6ee7b7;
    }
    .pipeline-label {
        font-size: 0.6rem;
        font-weight: 500;
        color: #64748b;
        text-align: center;
        letter-spacing: 0.2px;
        line-height: 1.2;
    }
    .pipeline-label.active-label {
        color: #4f46e5;
        font-weight: 700;
    }
    .pipeline-line {
        width: 28px; height: 2px;
        background: #cbd5e1;
        margin: 0 2px;
        margin-bottom: 1.2rem;
    }
    .pipeline-line.done {
        background: #6ee7b7;
    }

    /* ── Timing badge ─────────────────────────────────── */
    .timing-badge {
        display: inline-flex;
        align-items: center;
        gap: 0.35rem;
        padding: 0.25rem 0.7rem;
        border-radius: 5px;
        font-size: 0.72rem;
        font-weight: 500;
        background: #f0fdf4;
        color: #166534;
        border: 1px solid #bbf7d0;
    }

    /* ── Sidebar styling ──────────────────────────────── */
    .sidebar-section-title {
        font-size: 0.8rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.8px;
        color: #64748b;
        margin-bottom: 0.4rem;
    }
    .backend-badge {
        display: inline-flex;
        align-items: center;
        gap: 0.4rem;
        padding: 0.4rem 0.8rem;
        border-radius: 6px;
        font-size: 0.78rem;
        font-weight: 500;
        background: #f0fdf4;
        color: #166534;
        border: 1px solid #bbf7d0;
    }
    .backend-badge .dot {
        width: 7px; height: 7px;
        border-radius: 50%;
        background: #22c55e;
        display: inline-block;
        animation: pulse-dot 2s infinite;
    }
    @keyframes pulse-dot {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.4; }
    }

    /* ── Profile selector styling ─────────────────────── */
    .profile-card {
        display: flex;
        align-items: center;
        gap: 0.5rem;
        padding: 0.55rem 0.8rem;
        border-radius: 8px;
        font-size: 0.82rem;
        font-weight: 500;
        cursor: pointer;
        border: 1px solid #e2e8f0;
        margin-bottom: 0.35rem;
        background: #ffffff;
        transition: all 0.15s ease;
    }
    .profile-card:hover {
        border-color: #94a3b8;
        background: #f8fafc;
    }
    .profile-dot {
        width: 10px; height: 10px;
        border-radius: 50%;
        display: inline-block;
        flex-shrink: 0;
    }
    .dot-green  { background: #22c55e; }
    .dot-amber  { background: #f59e0b; }
    .dot-red    { background: #ef4444; }
    .dot-neutral { background: #94a3b8; }

    /* ── Input field labels ────────────────────────────── */
    .input-label {
        font-size: 0.78rem;
        font-weight: 600;
        color: #475569;
        margin-bottom: 0.15rem;
        letter-spacing: 0.2px;
    }
</style>
""", unsafe_allow_html=True)

# ──────────────────────────────────────────────────────────────
# Header
# ──────────────────────────────────────────────────────────────
st.markdown("""
<div class="main-header">
    <h1>🏦 Loan Underwriting Decision Analyzer</h1>
    <p>GPU-accelerated ML risk scoring · Gemini-powered explanations · Real-time cohort analysis</p>
</div>
""", unsafe_allow_html=True)

# ──────────────────────────────────────────────────────────────
# Sidebar – preset profiles & backend status
# ──────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown('<div class="sidebar-section-title">📋 Quick-Load Profiles</div>', unsafe_allow_html=True)
    st.caption("Select a demo profile or enter custom values below.")

    profile = st.radio(
        "Choose profile",
        [
            "⚪ Custom",
            "🟢 Low Risk",
            "🟡 Borderline",
            "🔴 High Risk",
        ],
        index=0,
        label_visibility="collapsed",
    )
    PRESETS = {
        "🟢 Low Risk":   {"income": 12500, "debt_ratio": 0.15, "credit_lines": 8,  "delinquencies": 0, "dependents": 0},
        "🟡 Borderline":  {"income": 4500,  "debt_ratio": 0.48, "credit_lines": 5,  "delinquencies": 0, "dependents": 3},
        "🔴 High Risk":  {"income": 1500,  "debt_ratio": 1.20, "credit_lines": 10, "delinquencies": 5, "dependents": 2},
    }
    defaults = PRESETS.get(profile, {"income": 5000, "debt_ratio": 0.30, "credit_lines": 6, "delinquencies": 0, "dependents": 1})

    st.markdown("<div style='height:0.8rem'></div>", unsafe_allow_html=True)
    st.markdown("---")
    st.markdown('<div class="sidebar-section-title">⚙️ Backend Status</div>', unsafe_allow_html=True)
    st.markdown("""
    <div class="backend-badge">
        <span class="dot"></span>
        Connected: Live Model + BigQuery
    </div>
    """, unsafe_allow_html=True)

# ──────────────────────────────────────────────────────────────
# Input form
# ──────────────────────────────────────────────────────────────
col_form, col_results = st.columns([1, 1.6], gap="large")

with col_form:
    st.markdown("#### Applicant Information")
    with st.form("applicant_form"):
        income = st.number_input(
            "Monthly Income ($)",
            min_value=0,
            max_value=500000,
            value=defaults["income"],
            step=500,
            help="Applicant's gross monthly income in US dollars",
        )

        # Debt ratio: display as percentage (0–500%), convert to decimal internally
        debt_ratio_pct = st.number_input(
            "Debt-to-Income Ratio (%)",
            min_value=0,
            max_value=500,
            value=int(round(defaults["debt_ratio"] * 100)),
            step=1,
            help="Total monthly debt payments ÷ gross monthly income, shown as a percentage",
        )
        # Convert percentage back to decimal for backend
        debt_ratio = debt_ratio_pct / 100.0

        credit_lines = st.number_input(
            "Open Credit Lines",
            min_value=0,
            max_value=50,
            value=defaults["credit_lines"],
            step=1,
            help="Number of currently open credit accounts",
        )
        delinquencies = st.number_input(
            "Delinquencies (90+ days)",
            min_value=0,
            max_value=20,
            value=defaults["delinquencies"],
            step=1,
            help="Count of payments 90 or more days past due",
        )
        dependents = st.number_input(
            "Number of Dependents",
            min_value=0,
            max_value=15,
            value=defaults["dependents"],
            step=1,
            help="Number of financial dependents",
        )
        submitted = st.form_submit_button("⚡  Analyze Applicant")

# ──────────────────────────────────────────────────────────────
# Helper: consistent risk color scale
# ──────────────────────────────────────────────────────────────
def risk_color(score):
    """Green < 0.2, Amber 0.2–0.5, Red >= 0.5."""
    if score < 0.2:
        return "#059669"   # green
    if score < 0.5:
        return "#d97706"   # amber
    return "#dc2626"       # red


def risk_label(score):
    if score < 0.2:
        return "Low Risk"
    if score < 0.5:
        return "Medium Risk"
    return "High Risk"


# ──────────────────────────────────────────────────────────────
# Helper: render agent pipeline tracker
# ──────────────────────────────────────────────────────────────
PIPELINE_AGENTS = [
    ("1", "Ingestion"),
    ("2", "Scoring"),
    ("3", "Cohort"),
    ("4", "Explainer"),
    ("5", "Recommender"),
]


def render_pipeline(active_index=None):
    """Render a horizontal 5-step pipeline tracker.

    active_index: 0-based index of the currently-active agent.
                  None = all idle, 4 = all done.
    """
    steps_html = []
    for i, (num, label) in enumerate(PIPELINE_AGENTS):
        if active_index is not None and i < active_index:
            circle_cls = "pipeline-circle done"
            label_cls = "pipeline-label"
        elif active_index is not None and i == active_index:
            circle_cls = "pipeline-circle active"
            label_cls = "pipeline-label active-label"
        else:
            circle_cls = "pipeline-circle"
            label_cls = "pipeline-label"

        step = f"""
        <div class="pipeline-step">
            <div class="{circle_cls}">{num}</div>
            <div class="{label_cls}">{label}</div>
        </div>"""
        steps_html.append(step)

        # Connector line between steps (not after last)
        if i < len(PIPELINE_AGENTS) - 1:
            line_cls = "pipeline-line done" if (active_index is not None and i < active_index) else "pipeline-line"
            steps_html.append(f'<div class="{line_cls}"></div>')

    return f'<div class="pipeline-tracker">{"".join(steps_html)}</div>'


# ──────────────────────────────────────────────────────────────
# Results
# ──────────────────────────────────────────────────────────────
with col_results:
    if submitted:
        applicant = {
            "income": income,
            "debt_ratio": debt_ratio,
            "credit_lines": credit_lines,
            "delinquencies": delinquencies,
            "dependents": dependents,
        }

        # ── Agent Pipeline Tracker (placeholder: show progress) ──
        pipeline_placeholder = st.empty()
        pipeline_placeholder.markdown(render_pipeline(active_index=0), unsafe_allow_html=True)

        with st.spinner("Running ML model & Gemini analysis..."):
            # Step 1: Ingestion (instant — data is already in dict)
            pipeline_placeholder.markdown(render_pipeline(active_index=1), unsafe_allow_html=True)

            # Step 2: Scoring — measure time
            t0 = time.perf_counter()
            risk_score = score_applicant(applicant)
            scoring_time = time.perf_counter() - t0

            pipeline_placeholder.markdown(render_pipeline(active_index=2), unsafe_allow_html=True)

            # Step 3: Cohort
            cohort_rate = get_cohort_default_rate(applicant)

            pipeline_placeholder.markdown(render_pipeline(active_index=3), unsafe_allow_html=True)

            # Step 4: Explainer
            explanation = explain_risk(applicant, risk_score, cohort_rate)

            pipeline_placeholder.markdown(render_pipeline(active_index=4), unsafe_allow_html=True)

            # Step 5: Recommender
            decision = recommend_decision(explanation)

        # Final: all done
        pipeline_placeholder.markdown(render_pipeline(active_index=5), unsafe_allow_html=True)

        # ── Section header + timing ──
        st.markdown("#### Analysis Results")
        st.markdown(
            f'<div class="timing-badge">⚡ Scored in {scoring_time:.3f}s (GPU-accelerated)</div>',
            unsafe_allow_html=True,
        )
        st.markdown("<div style='height:0.6rem'></div>", unsafe_allow_html=True)

        # ── Score cards ──
        c1, c2 = st.columns(2)
        with c1:
            color = risk_color(risk_score)
            r_label = risk_label(risk_score)
            st.markdown(f"""
            <div class="metric-card">
                <div class="label">Default Risk Score</div>
                <div class="value" style="color:{color}">{risk_score:.0%}</div>
                <div style="font-size:0.7rem; color:{color}; font-weight:600; margin-top:0.2rem;">
                    {r_label}
                </div>
            </div>
            """, unsafe_allow_html=True)
        with c2:
            st.markdown(f"""
            <div class="metric-card">
                <div class="label">Cohort Default Rate</div>
                <div class="value" style="color:#475569">{cohort_rate:.1f}%</div>
                <div style="font-size:0.7rem; color:#64748b; font-weight:500; margin-top:0.2rem;">
                    Historical average
                </div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("<div style='height:0.8rem'></div>", unsafe_allow_html=True)

        # ── Decision badge ──
        rec = decision["recommendation"]
        conf = decision["confidence"]
        badge_class = {
            "Approve": "badge-approve",
            "Manual Review": "badge-review",
            "Decline": "badge-decline",
        }.get(rec, "badge-review")
        conf_class = {"High": "conf-high", "Medium": "conf-medium", "Low": "conf-low"}.get(conf, "conf-medium")

        st.markdown(f"""
        <div style="display:flex; align-items:center; gap:0.8rem; margin-bottom:0.8rem;">
            <span class="decision-badge {badge_class}">{rec}</span>
            <span class="confidence-tag {conf_class}">Confidence: {conf}</span>
        </div>
        """, unsafe_allow_html=True)

        # ── Explanation ──
        st.markdown(f"""
        <div class="explanation-box">
            <strong>AI Risk Explanation</strong><br/><br/>
            {explanation}
        </div>
        """, unsafe_allow_html=True)

    else:
        # ── Empty state ──
        st.markdown(render_pipeline(active_index=None), unsafe_allow_html=True)
        st.markdown("""
        <div style="text-align:center; padding:3rem 2rem; color:#94a3b8;">
            <p style="font-size:2.5rem; margin:0;">🏦</p>
            <p style="font-size:0.95rem; margin:0.5rem 0 0 0; font-weight:400;">
                Enter applicant details and click <strong>Analyze Applicant</strong>
            </p>
        </div>
        """, unsafe_allow_html=True)
