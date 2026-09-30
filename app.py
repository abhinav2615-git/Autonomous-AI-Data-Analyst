import requests
import streamlit as st


# =========================================================
# CONFIGURATION
# =========================================================

API_URL = "http://127.0.0.1:8000"


st.set_page_config(
    page_title="AIDA | Autonomous AI Data Analyst",
    page_icon="◈",
    layout="wide",
    initial_sidebar_state="collapsed",
)


# =========================================================
# CUSTOM HTML + CSS
# =========================================================

st.html(
    """
    <style>

    /* =====================================================
       GLOBAL
       ===================================================== */

    .stApp {
        background:
            radial-gradient(
                circle at 10% 10%,
                rgba(76, 110, 245, 0.10),
                transparent 28%
            ),
            radial-gradient(
                circle at 90% 20%,
                rgba(139, 92, 246, 0.08),
                transparent 30%
            ),
            #07090f;

        color: #e8edf7;
    }


    .block-container {
        max-width: 1250px;
        padding-top: 2rem;
        padding-bottom: 4rem;
    }


    /* =====================================================
       HIDE STREAMLIT DEFAULT ELEMENTS
       ===================================================== */

    #MainMenu {
        visibility: hidden;
    }

    header {
        visibility: hidden;
    }

    footer {
        visibility: hidden;
    }


    /* =====================================================
       TOP NAVIGATION
       ===================================================== */

    .top-nav {
        display: flex;
        justify-content: space-between;
        align-items: center;

        padding: 14px 20px;

        border: 1px solid rgba(255,255,255,0.07);

        background: rgba(12,15,24,0.72);

        backdrop-filter: blur(20px);

        border-radius: 16px;

        margin-bottom: 55px;
    }


    .brand {
        display: flex;
        align-items: center;
        gap: 12px;
    }


    .brand-icon {
        width: 38px;
        height: 38px;

        display: flex;
        align-items: center;
        justify-content: center;

        border-radius: 11px;

        background:
            linear-gradient(
                135deg,
                #4f7cff,
                #8b5cf6
            );

        color: white;

        font-size: 19px;

        box-shadow:
            0 0 25px rgba(79,124,255,0.25);
    }


    .brand-name {
        font-size: 17px;
        font-weight: 700;
        letter-spacing: -0.3px;
        color: #f5f7fb;
    }


    .brand-subtitle {
        font-size: 11px;
        color: #77819a;
        margin-top: 2px;
    }


    .nav-status {
        display: flex;
        align-items: center;
        gap: 8px;

        font-size: 12px;

        color: #9aa4ba;

        padding: 7px 12px;

        border-radius: 999px;

        border: 1px solid rgba(255,255,255,0.06);

        background: rgba(255,255,255,0.025);
    }


    .status-dot {
        width: 7px;
        height: 7px;

        border-radius: 50%;

        background: #45e6a1;

        box-shadow:
            0 0 10px rgba(69,230,161,0.8);
    }


    /* =====================================================
       HERO
       ===================================================== */

    .hero {
        text-align: center;
        margin-bottom: 50px;
    }


    .hero-badge {
        display: inline-block;

        padding: 7px 14px;

        border-radius: 999px;

        border: 1px solid rgba(103,130,255,0.20);

        background: rgba(79,124,255,0.07);

        color: #8da7ff;

        font-size: 12px;

        font-weight: 600;

        letter-spacing: 0.5px;

        margin-bottom: 18px;
    }


    .hero h1 {
        font-size: clamp(42px, 6vw, 72px);

        line-height: 1.02;

        letter-spacing: -3px;

        margin: 0;

        font-weight: 800;

        background:
            linear-gradient(
                110deg,
                #ffffff 10%,
                #aab9ff 45%,
                #8b5cf6 85%
            );

        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }


    .hero-description {
        max-width: 650px;

        margin: 22px auto 0;

        color: #8d97ad;

        font-size: 16px;

        line-height: 1.7;
    }


    /* =====================================================
       SECTION LABEL
       ===================================================== */

    .section-label {
        color: #707b94;

        font-size: 11px;

        font-weight: 700;

        letter-spacing: 1.5px;

        text-transform: uppercase;

        margin-bottom: 12px;
    }


    /* =====================================================
       GLASS CARD
       ===================================================== */

    .glass-card {
        background:
            linear-gradient(
                145deg,
                rgba(255,255,255,0.045),
                rgba(255,255,255,0.018)
            );

        border: 1px solid rgba(255,255,255,0.075);

        border-radius: 20px;

        padding: 25px;

        box-shadow:
            0 20px 70px rgba(0,0,0,0.22);

        backdrop-filter: blur(20px);
    }


    /* =====================================================
       UPLOAD
       ===================================================== */

    .upload-header {
        display: flex;
        align-items: center;
        gap: 12px;
        margin-bottom: 15px;
    }


    .upload-icon {
        width: 40px;
        height: 40px;

        display: flex;
        align-items: center;
        justify-content: center;

        border-radius: 12px;

        background: rgba(79,124,255,0.10);

        border: 1px solid rgba(79,124,255,0.18);

        color: #8da7ff;

        font-size: 18px;
    }


    .upload-title {
        font-size: 16px;
        font-weight: 700;
        color: #f0f3f9;
    }


    .upload-description {
        color: #77819a;
        font-size: 13px;
        margin-top: 3px;
    }


    /* =====================================================
       FILE UPLOADER
       ===================================================== */

    [data-testid="stFileUploader"] {
        margin-top: 10px;
    }


    [data-testid="stFileUploaderDropzone"] {

        background:
            rgba(255,255,255,0.018);

        border:
            1px dashed
            rgba(120,140,190,0.28);

        border-radius: 16px;

        padding: 10px;

        transition: 0.25s ease;
    }


    [data-testid="stFileUploaderDropzone"]:hover {

        border-color:
            rgba(100,130,255,0.60);

        background:
            rgba(79,124,255,0.035);
    }


    /* =====================================================
       BUTTONS
       ===================================================== */

    .stButton > button {

        width: 100%;

        min-height: 44px;

        border-radius: 12px;

        border: 1px solid rgba(120,140,255,0.30);

        background:
            linear-gradient(
                135deg,
                #4267df,
                #7250d8
            );

        color: white;

        font-weight: 700;

        font-size: 13px;

        box-shadow:
            0 10px 30px rgba(79,90,210,0.20);

        transition:
            transform 0.2s ease,
            box-shadow 0.2s ease;
    }


    .stButton > button:hover {

        transform: translateY(-2px);

        box-shadow:
            0 15px 40px rgba(79,90,210,0.32);
    }


    /* =====================================================
       TEXT INPUT
       ===================================================== */

    .stTextInput input {

        background:
            rgba(255,255,255,0.025) !important;

        border:
            1px solid rgba(255,255,255,0.09) !important;

        border-radius: 14px !important;

        color: #f4f6fb !important;

        min-height: 48px;

        font-size: 14px;

        padding-left: 16px;
    }


    .stTextInput input:focus {

        border-color:
            rgba(100,130,255,0.60) !important;

        box-shadow:
            0 0 0 1px rgba(100,130,255,0.15),
            0 0 30px rgba(79,124,255,0.07);
    }


    /* =====================================================
       METRICS
       ===================================================== */

    [data-testid="stMetric"] {

        background:
            rgba(255,255,255,0.025);

        border:
            1px solid rgba(255,255,255,0.065);

        border-radius: 16px;

        padding: 18px;

        min-height: 105px;
    }


    [data-testid="stMetricLabel"] {

        color: #77819a !important;

        font-size: 11px !important;

        text-transform: uppercase;

        letter-spacing: 1px;
    }


    [data-testid="stMetricValue"] {

        color: #eef2fa !important;

        font-size: 25px !important;

        font-weight: 750;
    }


    /* =====================================================
       RESULT
       ===================================================== */

    .result-card {

        background:
            linear-gradient(
                145deg,
                rgba(79,124,255,0.075),
                rgba(139,92,246,0.035)
            );

        border:
            1px solid
            rgba(100,130,255,0.18);

        border-radius: 20px;

        padding: 26px;

        margin-top: 10px;

        box-shadow:
            0 20px 60px rgba(0,0,0,0.18);
    }


    .result-label {

        font-size: 10px;

        font-weight: 800;

        letter-spacing: 1.5px;

        color: #8199ff;

        text-transform: uppercase;

        margin-bottom: 12px;
    }


    .result-text {

        color: #eef2f8;

        font-size: 18px;

        line-height: 1.65;

        font-weight: 500;
    }


    /* =====================================================
       TOOL BADGES
       ===================================================== */

    .tool-badge {

        display: inline-block;

        padding: 7px 11px;

        margin: 3px;

        border-radius: 8px;

        background:
            rgba(79,124,255,0.07);

        border:
            1px solid rgba(79,124,255,0.14);

        color: #91a7ff;

        font-family: monospace;

        font-size: 11px;
    }


    /* =====================================================
       VISUALIZATION
       ===================================================== */

    .visualization-card {

        background:
            rgba(255,255,255,0.02);

        border:
            1px solid rgba(255,255,255,0.065);

        border-radius: 20px;

        padding: 20px;

        margin-top: 20px;
    }


    /* =====================================================
       EXPANDER
       ===================================================== */

    [data-testid="stExpander"] {

        background:
            rgba(255,255,255,0.018);

        border:
            1px solid rgba(255,255,255,0.065);

        border-radius: 14px;
    }


    /* =====================================================
       FOOTER
       ===================================================== */

    .footer {

        text-align: center;

        margin-top: 70px;

        padding-top: 25px;

        border-top:
            1px solid rgba(255,255,255,0.05);

        color: #555f75;

        font-size: 11px;
    }


    .footer strong {
        color: #79839b;
    }

    </style>
    """
)


# =========================================================
# TOP NAVIGATION
# =========================================================

st.html(
    """
    <div class="top-nav">

        <div class="brand">

            <div class="brand-icon">
                ◈
            </div>

            <div>

                <div class="brand-name">
                    AIDA
                </div>

                <div class="brand-subtitle">
                    Autonomous Intelligence for Data Analysis
                </div>

            </div>

        </div>

        <div class="nav-status">

            <span class="status-dot"></span>

            System Online

        </div>

    </div>
    """
)


# =========================================================
# HERO
# =========================================================

st.html(
    """
    <div class="hero">

        <div class="hero-badge">
            AI-POWERED DATA INTELLIGENCE
        </div>

        <h1>
            Your data.<br>
            <span>Understood.</span>
        </h1>

        <div class="hero-description">

            Upload your dataset, ask questions in natural language,
            and let the AI analyze patterns, generate insights,
            and visualize what matters.

        </div>

    </div>
    """
)


# =========================================================
# DATASET
# =========================================================

st.markdown(
    '<div class="section-label">01 — Dataset</div>',
    unsafe_allow_html=True,
)


st.html(
    """
    <div class="glass-card">

        <div class="upload-header">

            <div class="upload-icon">
                ↑
            </div>

            <div>

                <div class="upload-title">
                    Load your dataset
                </div>

                <div class="upload-description">
                    CSV or Excel files supported
                </div>

            </div>

        </div>

    </div>
    """
)


uploaded_file = st.file_uploader(
    "Upload dataset",
    type=["csv", "xlsx", "xls"],
    label_visibility="collapsed",
)


# =========================================================
# DATASET SELECTED
# =========================================================

if uploaded_file is not None:

    st.html(
        f"""
        <div style="
            margin-top:12px;
            padding:12px 15px;
            border-radius:12px;
            background:rgba(69,230,161,0.045);
            border:1px solid rgba(69,230,161,0.12);
            color:#8de8bd;
            font-size:13px;
        ">
            ✓ Dataset loaded&nbsp;&nbsp;·&nbsp;&nbsp;
            <strong>{uploaded_file.name}</strong>
        </div>
        """
    )


    st.markdown("<br>", unsafe_allow_html=True)


    if st.button(
        "◉  Profile Dataset",
        key="profile_button",
    ):

        files = {
            "file": (
                uploaded_file.name,
                uploaded_file.getvalue(),
                uploaded_file.type,
            )
        }

        try:

            with st.spinner(
                "Profiling dataset..."
            ):

                response = requests.post(
                    f"{API_URL}/profile",
                    files=files,
                    timeout=120,
                )


            if response.status_code == 200:

                profile_data = response.json()

                profile = profile_data["profile"]

                st.success(
                    "Dataset successfully profiled."
                )


                st.markdown(
                    '<div class="section-label">Dataset Overview</div>',
                    unsafe_allow_html=True,
                )


                col1, col2, col3 = st.columns(3)


                with col1:

                    st.metric(
                        "Rows",
                        f"{profile['rows']:,}",
                    )


                with col2:

                    st.metric(
                        "Columns",
                        profile["columns"],
                    )


                with col3:

                    st.metric(
                        "Features",
                        len(profile["column_names"]),
                    )


                with st.expander(
                    "View dataset structure"
                ):

                    st.write(
                        "**Columns**"
                    )

                    st.write(
                        profile["column_names"]
                    )

                    st.write(
                        "**Data Types**"
                    )

                    st.json(
                        profile["data_types"]
                    )

                    st.write(
                        "**Missing Values**"
                    )

                    st.json(
                        profile["missing_values"]
                    )


            else:

                st.error(
                    f"Profiling failed: {response.text}"
                )


        except requests.exceptions.RequestException as error:

            st.error(
                "Unable to connect to the FastAPI backend."
            )

            st.code(
                str(error)
            )


# =========================================================
# QUESTION
# =========================================================

st.markdown(
    "<br>",
    unsafe_allow_html=True,
)


st.markdown(
    '<div class="section-label">02 — Ask your data</div>',
    unsafe_allow_html=True,
)


question = st.text_input(
    "Natural language query",
    placeholder=(
        "e.g. Which country generated the highest revenue?"
    ),
    label_visibility="collapsed",
)


st.html(
    """
    <div style="
        margin-top:8px;
        color:#5f6980;
        font-size:11px;
    ">
        Ask questions about revenue, products, countries,
        customers, trends, and more.
    </div>
    """
)


st.markdown(
    "<br>",
    unsafe_allow_html=True,
)


analyze_button = st.button(
    "✦  Analyze Dataset",
    key="analyze_button",
)


# =========================================================
# ANALYSIS
# =========================================================

if analyze_button:

    if uploaded_file is None:

        st.warning(
            "Please upload a dataset before starting the analysis."
        )

    elif not question.strip():

        st.warning(
            "Please enter a question about your dataset."
        )

    else:

        files = {
            "file": (
                uploaded_file.name,
                uploaded_file.getvalue(),
                uploaded_file.type,
            )
        }

        data = {
            "question": question,
        }


        try:

            with st.spinner(
                "AI agent is analyzing your data..."
            ):

                response = requests.post(
                    f"{API_URL}/analyze",
                    files=files,
                    data=data,
                    timeout=120,
                )


            if response.status_code == 200:

                result = response.json()


                st.markdown(
                    "<br>",
                    unsafe_allow_html=True,
                )


                st.markdown(
                    '<div class="section-label">03 — Intelligence</div>',
                    unsafe_allow_html=True,
                )


                # =================================================
                # AI INSIGHT
                # =================================================

                st.html(
                    f"""
                    <div class="result-card">

                        <div class="result-label">
                            AI Insight
                        </div>

                        <div class="result-text">
                            {result["answer"]}
                        </div>

                    </div>
                    """
                )


                st.markdown(
                    "<br>",
                    unsafe_allow_html=True,
                )


                # =================================================
                # METRICS
                # =================================================

                dataset_info = result["dataset"]


                col1, col2, col3, col4 = st.columns(4)


                with col1:

                    st.metric(
                        "Rows",
                        f"{dataset_info['rows']:,}",
                    )


                with col2:

                    st.metric(
                        "Columns",
                        dataset_info["columns"],
                    )


                with col3:

                    st.metric(
                        "Confidence",
                        f"{result['confidence'] * 100:.0f}%",
                    )


                with col4:

                    st.metric(
                        "Tools",
                        len(result["tools_used"]),
                    )


                # =================================================
                # AGENT ACTIVITY
                # =================================================

                st.markdown(
                    "<br>",
                    unsafe_allow_html=True,
                )


                st.markdown(
                    '<div class="section-label">Agent Activity</div>',
                    unsafe_allow_html=True,
                )


                tool_html = ""


                for tool in result["tools_used"]:

                    tool_html += (
                        f'<span class="tool-badge">'
                        f'✓ {tool}'
                        f'</span>'
                    )


                st.html(
                    f"""
                    <div class="glass-card">

                        <div style="
                            color:#a8b2c8;
                            font-size:12px;
                            margin-bottom:10px;
                        ">
                            Tools executed by the analysis agent
                        </div>

                        {tool_html}

                    </div>
                    """
                )


                # =================================================
                # VISUALIZATION
                # =================================================

                if result.get("chart_url"):

                    st.markdown(
                        "<br>",
                        unsafe_allow_html=True,
                    )


                    st.markdown(
                        '<div class="section-label">Visualization</div>',
                        unsafe_allow_html=True,
                    )


                    chart_url = (
                        f"{API_URL}"
                        f"{result['chart_url']}"
                    )


                    st.html(
                        """
                        <div class="visualization-card">
                        """
                    )


                    st.image(
                        chart_url,
                        use_container_width=True,
                    )


                    st.html(
                        """
                        </div>
                        """
                    )


                # =================================================
                # DATASET INFORMATION
                # =================================================

                st.markdown(
                    "<br>",
                    unsafe_allow_html=True,
                )


                st.markdown(
                    '<div class="section-label">Dataset</div>',
                    unsafe_allow_html=True,
                )


                st.html(
                    f"""
                    <div class="glass-card">

                        <div style="
                            color:#f0f3f9;
                            font-size:14px;
                            font-weight:650;
                            margin-bottom:8px;
                        ">
                            {dataset_info["file_name"]}
                        </div>

                        <div style="
                            color:#737e96;
                            font-size:12px;
                        ">
                            {dataset_info["rows"]:,} rows
                            &nbsp;·&nbsp;
                            {dataset_info["columns"]} columns
                        </div>

                    </div>
                    """
                )


                # =================================================
                # ANALYSIS PLAN
                # =================================================

                st.markdown(
                    "<br>",
                    unsafe_allow_html=True,
                )


                with st.expander(
                    "⌁  View agent reasoning plan"
                ):

                    plan = result["plan"]


                    st.markdown(
                        "**Objective**"
                    )

                    st.write(
                        plan["objective"]
                    )


                    st.markdown(
                        "**Execution steps**"
                    )


                    for index, step in enumerate(
                        plan["steps"],
                        start=1,
                    ):

                        st.write(
                            f"{index}. {step}"
                        )


                    st.markdown(
                        "**Selected tools**"
                    )


                    for tool in plan["tools"]:

                        st.code(
                            tool
                        )


            else:

                st.error(
                    f"Analysis failed: {response.text}"
                )


        except requests.exceptions.RequestException as error:

            st.error(
                "Unable to connect to the FastAPI backend."
            )

            st.code(
                str(error)
            )


# =========================================================
# FOOTER
# =========================================================

st.html(
    """
    <div class="footer">

        <strong>AIDA</strong>
        &nbsp;·&nbsp;
        Autonomous AI Data Analyst

        <br><br>

        FastAPI · Streamlit · Pandas · AI Agent Architecture

    </div>
    """
)