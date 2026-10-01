import html

import requests
import streamlit as st


API_URL = "http://127.0.0.1:8000"


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="AIDA — Autonomous AI Data Analyst",
    page_icon="📊",
    layout="wide",
)


# ============================================================
# CSS
# ============================================================

st.html(
    """
    <style>
    .stApp {
        background:
            radial-gradient(
                circle at 8% 0%,
                rgba(99, 102, 241, 0.12),
                transparent 32%
            ),
            radial-gradient(
                circle at 92% 8%,
                rgba(6, 182, 212, 0.10),
                transparent 32%
            ),
            #080b12;
        color: #f8fafc;
    }

    .block-container {
        max-width: 1080px;
        padding-top: 1.5rem;
        padding-bottom: 4rem;
    }

    /* Header */

    .header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 3rem;
    }

    .brand {
        display: flex;
        align-items: center;
        gap: 12px;
    }

    .brand-icon {
        width: 44px;
        height: 44px;
        border-radius: 13px;
        display: flex;
        align-items: center;
        justify-content: center;
        background: linear-gradient(135deg, #6366f1, #06b6d4);
        color: white;
        font-size: 22px;
        font-weight: 800;
    }

    .brand-name {
        color: #f8fafc;
        font-size: 1.2rem;
        font-weight: 750;
    }

    .brand-subtitle {
        color: #94a3b8;
        font-size: 0.75rem;
        margin-top: 2px;
    }

    .status {
        display: flex;
        align-items: center;
        gap: 7px;
        padding: 7px 12px;
        border-radius: 999px;
        border: 1px solid rgba(34, 197, 94, 0.25);
        background: rgba(34, 197, 94, 0.08);
        color: #86efac;
        font-size: 0.75rem;
        font-weight: 650;
    }

    .status-dot {
        width: 7px;
        height: 7px;
        border-radius: 50%;
        background: #22c55e;
    }

    /* Hero */

    .hero {
        margin-bottom: 3.2rem;
    }

    .hero-title {
        color: #f8fafc;
        font-size: 3rem;
        line-height: 1.08;
        letter-spacing: -0.045em;
        font-weight: 800;
        margin-bottom: 0.8rem;
    }

    .hero-title span {
        background: linear-gradient(90deg, #818cf8, #22d3ee);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }

    .hero-description {
        max-width: 760px;
        color: #94a3b8;
        font-size: 0.98rem;
        line-height: 1.7;
    }

    /* Sections */

    .section-label {
        color: #64748b;
        font-size: 0.72rem;
        font-weight: 750;
        letter-spacing: 0.12em;
        text-transform: uppercase;
        margin: 1.7rem 0 0.8rem;
    }

    .card {
        background: rgba(15, 23, 42, 0.72);
        border: 1px solid rgba(148, 163, 184, 0.10);
        border-radius: 17px;
        padding: 1.25rem;
        box-shadow: 0 16px 45px rgba(0, 0, 0, 0.16);
    }

    .card-title {
        color: #f8fafc;
        font-size: 1rem;
        font-weight: 700;
        margin-bottom: 0.35rem;
    }

    .card-description {
        color: #94a3b8;
        font-size: 0.8rem;
        line-height: 1.5;
    }

    /* File */

    .file-status {
        margin-top: 0.8rem;
        padding: 0.7rem 0.85rem;
        border-radius: 10px;
        background: rgba(34, 197, 94, 0.07);
        border: 1px solid rgba(34, 197, 94, 0.15);
        color: #bbf7d0;
        font-size: 0.8rem;
    }

    /* Insight */

    .insight {
        background:
            linear-gradient(
                135deg,
                rgba(99, 102, 241, 0.13),
                rgba(6, 182, 212, 0.07)
            );
        border: 1px solid rgba(129, 140, 248, 0.18);
        border-radius: 16px;
        padding: 1.25rem;
        margin-top: 1rem;
    }

    .insight-label {
        color: #a5b4fc;
        font-size: 0.7rem;
        font-weight: 750;
        letter-spacing: 0.1em;
        text-transform: uppercase;
        margin-bottom: 0.55rem;
    }

    .insight-text {
        color: #e2e8f0;
        font-size: 0.95rem;
        line-height: 1.7;
        white-space: pre-wrap;
    }

    /* Metrics */

    .metric {
        background: rgba(15, 23, 42, 0.72);
        border: 1px solid rgba(148, 163, 184, 0.10);
        border-radius: 14px;
        padding: 1rem;
    }

    .metric-label {
        color: #64748b;
        font-size: 0.72rem;
        margin-bottom: 0.3rem;
    }

    .metric-value {
        color: #f8fafc;
        font-size: 1.35rem;
        font-weight: 750;
    }

    /* Activity */

    .activity {
        background: rgba(15, 23, 42, 0.72);
        border: 1px solid rgba(148, 163, 184, 0.10);
        border-radius: 16px;
        padding: 1rem;
    }

    .activity-row {
        display: flex;
        align-items: center;
        gap: 10px;
        padding: 9px 10px;
        border-radius: 9px;
        background: rgba(30, 41, 59, 0.45);
        margin-bottom: 6px;
    }

    .activity-row:last-child {
        margin-bottom: 0;
    }

    .success {
        color: #4ade80;
        font-weight: 750;
    }

    .failed {
        color: #f87171;
        font-weight: 750;
    }

    .activity-tool {
        color: #e2e8f0;
        font-size: 0.8rem;
        font-weight: 600;
    }

    .activity-status {
        margin-left: auto;
        color: #64748b;
        font-size: 0.7rem;
    }

    /* Badges */

    .badge {
        display: inline-block;
        padding: 5px 9px;
        margin: 3px;
        border-radius: 999px;
        background: rgba(99, 102, 241, 0.10);
        border: 1px solid rgba(129, 140, 248, 0.18);
        color: #c7d2fe;
        font-size: 0.72rem;
        font-weight: 600;
    }

    /* Dataset */

    .data-row {
        display: flex;
        justify-content: space-between;
        padding: 8px 0;
        border-bottom: 1px solid rgba(148, 163, 184, 0.07);
        font-size: 0.8rem;
    }

    .data-row:last-child {
        border-bottom: none;
    }

    .data-key {
        color: #64748b;
    }

    .data-value {
        color: #cbd5e1;
    }

    /* Plan */

    .plan-step {
        background: rgba(30, 41, 59, 0.45);
        color: #cbd5e1;
        border-radius: 9px;
        padding: 8px 10px;
        margin-bottom: 6px;
        font-size: 0.79rem;
    }
    </style>
    """
)


# ============================================================
# HELPERS
# ============================================================

def section(title):
    st.html(
        f'<div class="section-label">{html.escape(title)}</div>'
    )


def api_upload(endpoint, file, question=None):
    files = {
        "file": (
            file.name,
            file.getvalue(),
            file.type,
        )
    }

    data = {"question": question} if question else None

    return requests.post(
        f"{API_URL}/{endpoint}",
        files=files,
        data=data,
        timeout=180,
    )


# ============================================================
# SESSION STATE
# ============================================================

if "analysis_result" not in st.session_state:
    st.session_state.analysis_result = None

if "profile_result" not in st.session_state:
    st.session_state.profile_result = None

if "file_name" not in st.session_state:
    st.session_state.file_name = None


# ============================================================
# HEADER
# ============================================================

st.html(
    """
    <div class="header">
        <div class="brand">
            <div class="brand-icon">✦</div>
            <div>
                <div class="brand-name">AIDA</div>
                <div class="brand-subtitle">
                    Autonomous AI Data Analyst
                </div>
            </div>
        </div>

        <div class="status">
            <span class="status-dot"></span>
            System Online
        </div>
    </div>
    """
)


# ============================================================
# HERO
# ============================================================

st.html(
    """
    <div class="hero">
        <div class="hero-title">
            Turn your data into
            <span>intelligent insights.</span>
        </div>

        <div class="hero-description">
            Upload a dataset, ask a natural-language question,
            and let the AI analyst select analysis tools,
            execute them, generate visualizations,
            and explain the results.
        </div>
    </div>
    """
)


# ============================================================
# DATASET
# ============================================================

section("Dataset")

st.html(
    """
    <div class="card">
        <div class="card-title">
            Upload your dataset
        </div>

        <div class="card-description">
            Supported formats: CSV, XLSX, XLS
        </div>
    </div>
    """
)

uploaded_file = st.file_uploader(
    "Upload dataset",
    type=["csv", "xlsx", "xls"],
    label_visibility="collapsed",
)

if uploaded_file:

    if st.session_state.file_name != uploaded_file.name:
        st.session_state.file_name = uploaded_file.name
        st.session_state.analysis_result = None
        st.session_state.profile_result = None

    file_name = html.escape(uploaded_file.name)

    st.html(
        f"""
        <div class="file-status">
            ✓ Dataset ready:
            <strong>{file_name}</strong>
        </div>
        """
    )


    # ========================================================
    # INSPECT
    # ========================================================

    if st.button("Inspect Dataset"):

        with st.spinner("Inspecting dataset..."):

            try:
                response = api_upload(
                    "profile",
                    uploaded_file,
                )

                result = response.json()

                if result.get("status") == "success":
                    st.session_state.profile_result = result
                    st.success("Dataset inspection completed.")
                else:
                    st.error(
                        result.get(
                            "message",
                            "Dataset inspection failed.",
                        )
                    )

            except requests.RequestException as error:
                st.error(
                    f"Could not connect to FastAPI: {error}"
                )


    # ========================================================
    # QUESTION
    # ========================================================

    section("Ask your data analyst")

    question = st.text_area(
        "Question",
        placeholder="Ask something about your dataset...",
        height=100,
        label_visibility="collapsed",
    )

    suggestion_cols = st.columns(3)

    suggestions = [
        "Which country generated the highest revenue?",
        "Show monthly revenue.",
        "Which products generated the highest revenue?",
    ]

    for i, suggestion in enumerate(suggestions):

        with suggestion_cols[i]:

            if st.button(
                suggestion,
                use_container_width=True,
                key=f"suggestion_{i}",
            ):
                question = suggestion


    # ========================================================
    # ANALYZE
    # ========================================================

    if st.button(
        "✦ Analyze Dataset",
        type="primary",
        use_container_width=True,
    ):

        if not question.strip():

            st.warning("Please enter a question first.")

        else:

            with st.spinner(
                "AI analyst is analyzing your dataset..."
            ):

                try:
                    response = api_upload(
                        "analyze",
                        uploaded_file,
                        question,
                    )

                    result = response.json()

                    if result.get("status") == "success":

                        st.session_state.analysis_result = result

                    else:

                        st.error(
                            result.get(
                                "message",
                                "Analysis failed.",
                            )
                        )

                except requests.RequestException as error:

                    st.error(
                        f"Could not connect to FastAPI: {error}"
                    )


# ============================================================
# RESULTS
# ============================================================

result = st.session_state.analysis_result

if result:

    # ========================================================
    # PIPELINE
    # ========================================================

    section("Agent Pipeline")

    st.html(
        """
        <div class="card">
            <div style="
                display:flex;
                justify-content:space-between;
                align-items:center;
                gap:12px;
                flex-wrap:wrap;
            ">
                <div>
                    <strong>Understand</strong>
                    <div class="card-description">
                        Interpret question
                    </div>
                </div>

                <div>→</div>

                <div>
                    <strong>Select Tool</strong>
                    <div class="card-description">
                        Create analysis plan
                    </div>
                </div>

                <div>→</div>

                <div>
                    <strong>Analyze</strong>
                    <div class="card-description">
                        Execute tools
                    </div>
                </div>

                <div>→</div>

                <div>
                    <strong>Insight</strong>
                    <div class="card-description">
                        Interpret results
                    </div>
                </div>
            </div>
        </div>
        """
    )


    # ========================================================
    # INSIGHT
    # ========================================================

    answer = html.escape(
        str(result.get("answer", ""))
    )

    st.html(
        f"""
        <div class="insight">
            <div class="insight-label">
                AI Insight
            </div>

            <div class="insight-text">
                {answer}
            </div>
        </div>
        """
    )


    # ========================================================
    # METRICS
    # ========================================================

    dataset = result.get("dataset", {})

    rows = dataset.get("rows", 0)
    columns = dataset.get("columns", 0)
    confidence = result.get("confidence", 0)
    tools = result.get("tools_used", [])

    metrics = st.columns(4)

    values = [
        ("Rows", f"{rows:,}"),
        ("Columns", f"{columns:,}"),
        ("Confidence", f"{confidence:.0%}"),
        ("Tools", str(len(tools))),
    ]

    for column, (label, value) in zip(metrics, values):

        with column:

            st.html(
                f"""
                <div class="metric">
                    <div class="metric-label">
                        {label}
                    </div>

                    <div class="metric-value">
                        {value}
                    </div>
                </div>
                """
            )


    # ========================================================
    # AGENT ACTIVITY
    # ========================================================

    section("Agent Activity")

    execution_steps = result.get(
        "execution_steps",
        [],
    )

    activity = ""

    for step in execution_steps:

        number = html.escape(
            str(step.get("step_number", ""))
        )

        tool = html.escape(
            str(step.get("tool_name", ""))
        )

        success = step.get(
            "success",
            False,
        )

        icon = "✓" if success else "✕"
        status = "Completed" if success else "Failed"
        css = "success" if success else "failed"

        activity += f"""
            <div class="activity-row">
                <span class="{css}">
                    {icon}
                </span>

                <span class="activity-tool">
                    Step {number} — {tool}
                </span>

                <span class="activity-status">
                    {status}
                </span>
            </div>
        """

    st.html(
        f"""
        <div class="activity">
            {activity}
        </div>
        """
    )


    # ========================================================
    # VISUALIZATIONS
    # ========================================================

    charts = result.get("charts", [])

    if charts:

        section("Visualizations")

        for chart in charts:

            chart_url = chart.get("url")

            if not chart_url:
                continue

            chart_name = html.escape(
                str(
                    chart.get(
                        "tool",
                        "Analysis",
                    )
                )
            )

            st.html(
                f"""
                <div style="
                    color:#94a3b8;
                    font-size:0.75rem;
                    margin:0.7rem 0 0.35rem;
                ">
                    {chart_name}
                </div>
                """
            )

            st.image(
                f"{API_URL}{chart_url}",
                use_container_width=True,
            )


    # ========================================================
    # DATASET INFORMATION
    # ========================================================

    section("Dataset Information")

    file_name = html.escape(
        str(
            dataset.get(
                "file_name",
                "Unknown",
            )
        )
    )

    column_names = dataset.get(
        "column_names",
        [],
    )

    badges = "".join(
        f'<span class="badge">'
        f'{html.escape(str(column))}'
        f'</span>'
        for column in column_names
    )

    st.html(
        f"""
        <div class="card">

            <div class="data-row">
                <span class="data-key">
                    File
                </span>

                <span class="data-value">
                    {file_name}
                </span>
            </div>

            <div class="data-row">
                <span class="data-key">
                    Rows
                </span>

                <span class="data-value">
                    {rows:,}
                </span>
            </div>

            <div class="data-row">
                <span class="data-key">
                    Columns
                </span>

                <span class="data-value">
                    {columns:,}
                </span>
            </div>

            <div style="
                margin-top:12px;
                color:#64748b;
                font-size:0.72rem;
            ">
                Column Names
            </div>

            <div style="margin-top:6px;">
                {badges}
            </div>

        </div>
        """
    )


    # ========================================================
    # ANALYSIS PLAN
    # ========================================================

    section("Analysis Execution Plan")

    plan = result.get("plan", {})

    objective = html.escape(
        str(
            plan.get(
                "objective",
                "",
            )
        )
    )

    plan_steps = plan.get(
        "steps",
        [],
    )

    steps_html = "".join(
        f"""
        <div class="plan-step">
            <strong>{i}.</strong>
            {html.escape(str(step))}
        </div>
        """
        for i, step in enumerate(
            plan_steps,
            start=1,
        )
    )

    st.html(
        f"""
        <div class="card">

            <div style="
                color:#a5b4fc;
                font-size:0.7rem;
                font-weight:750;
                letter-spacing:0.08em;
                margin-bottom:8px;
            ">
                OBJECTIVE
            </div>

            <div style="
                color:#e2e8f0;
                font-size:0.88rem;
                margin-bottom:14px;
            ">
                {objective}
            </div>

            {steps_html}

        </div>
        """
    )