import requests
import streamlit as st


API_URL = "http://127.0.0.1:8000"


st.set_page_config(
    page_title="Autonomous AI Data Analyst",
    page_icon="📊",
    layout="wide",
)


st.title("📊 Autonomous AI Data Analyst")

st.write(
    "Upload a dataset and ask a question in natural language."
)

st.divider()


# =========================================================
# Dataset Upload
# =========================================================

st.subheader("1. Upload Dataset")

uploaded_file = st.file_uploader(
    "Choose a CSV or Excel file",
    type=["csv", "xlsx", "xls"],
)


# =========================================================
# Dataset Profiling
# =========================================================

if uploaded_file is not None:

    st.success(
        f"Dataset selected: {uploaded_file.name}"
    )

    if st.button("Profile Dataset"):

        files = {
            "file": (
                uploaded_file.name,
                uploaded_file.getvalue(),
                uploaded_file.type,
            )
        }

        try:

            response = requests.post(
                f"{API_URL}/profile",
                files=files,
                timeout=120,
            )

            if response.status_code == 200:

                profile_data = response.json()

                st.success(
                    "Dataset profiled successfully."
                )

                profile = profile_data["profile"]

                # -----------------------------------------
                # Dataset Size
                # -----------------------------------------

                col1, col2 = st.columns(2)

                with col1:
                    st.metric(
                        "Rows",
                        profile["rows"],
                    )

                with col2:
                    st.metric(
                        "Columns",
                        profile["columns"],
                    )

                # -----------------------------------------
                # Column Names
                # -----------------------------------------

                st.subheader("Column Names")

                st.write(
                    profile["column_names"]
                )

                # -----------------------------------------
                # Data Types
                # -----------------------------------------

                with st.expander("Data Types"):

                    st.json(
                        profile["data_types"]
                    )

                # -----------------------------------------
                # Missing Values
                # -----------------------------------------

                with st.expander("Missing Values"):

                    st.json(
                        profile["missing_values"]
                    )

                # -----------------------------------------
                # Unique Values
                # -----------------------------------------

                with st.expander("Unique Values"):

                    st.json(
                        profile["unique_values"]
                    )

                # -----------------------------------------
                # Numerical Summary
                # -----------------------------------------

                with st.expander(
                    "Numerical Summary"
                ):

                    st.json(
                        profile["numerical_summary"]
                    )

            else:

                st.error(
                    f"Profiling failed: {response.text}"
                )

        except requests.exceptions.RequestException as error:

            st.error(
                "Could not connect to the FastAPI backend."
            )

            st.code(
                str(error)
            )


# =========================================================
# Natural Language Analysis
# =========================================================

st.divider()

st.subheader("2. Ask a Question")

question = st.text_input(
    "Enter your analysis question",
    placeholder=(
        "Example: Which country generated "
        "the highest revenue?"
    ),
)


if st.button("🔍 Analyze"):

    # -----------------------------------------
    # Validation
    # -----------------------------------------

    if uploaded_file is None:

        st.warning(
            "Please upload a dataset first."
        )

    elif not question.strip():

        st.warning(
            "Please enter a question."
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
                "Analyzing your dataset..."
            ):

                response = requests.post(
                    f"{API_URL}/analyze",
                    files=files,
                    data=data,
                    timeout=120,
                )

            # =================================================
            # Successful Response
            # =================================================

            if response.status_code == 200:

                result = response.json()

                st.success(
                    "Analysis completed successfully."
                )

                # -----------------------------------------
                # Answer
                # -----------------------------------------

                st.subheader("Answer")

                st.info(
                    result["answer"]
                )

                # -----------------------------------------
                # Visualization
                # -----------------------------------------

                if result.get("chart_url"):

                    st.subheader(
                        "Visualization"
                    )

                    chart_url = (
                        f"{API_URL}"
                        f"{result['chart_url']}"
                    )

                    st.image(
                        chart_url,
                        caption=(
                            "Generated visualization"
                        ),
                        use_container_width=True,
                    )

                # -----------------------------------------
                # Confidence + Tools
                # -----------------------------------------

                col1, col2 = st.columns(2)

                with col1:

                    st.metric(
                        "Confidence",
                        f"{result['confidence'] * 100:.0f}%",
                    )

                with col2:

                    st.write(
                        "**Tools Used**"
                    )

                    for tool in result[
                        "tools_used"
                    ]:

                        st.code(tool)

                # -----------------------------------------
                # Dataset Information
                # -----------------------------------------

                st.subheader(
                    "Dataset Information"
                )

                dataset_info = result[
                    "dataset"
                ]

                col1, col2, col3 = st.columns(3)

                with col1:

                    st.metric(
                        "Rows",
                        dataset_info["rows"],
                    )

                with col2:

                    st.metric(
                        "Columns",
                        dataset_info["columns"],
                    )

                with col3:

                    st.write(
                        "**File**"
                    )

                    st.write(
                        dataset_info[
                            "file_name"
                        ]
                    )

                # -----------------------------------------
                # Analysis Plan
                # -----------------------------------------

                with st.expander(
                    "View Analysis Plan"
                ):

                    plan = result["plan"]

                    st.write(
                        "**Objective:**"
                    )

                    st.write(
                        plan["objective"]
                    )

                    st.write(
                        "**Steps:**"
                    )

                    for step in plan["steps"]:

                        st.write(
                            f"- {step}"
                        )

                    st.write(
                        "**Tools:**"
                    )

                    for tool in plan["tools"]:

                        st.code(tool)

            # =================================================
            # Error Response
            # =================================================

            else:

                st.error(
                    f"Analysis failed: {response.text}"
                )

        except requests.exceptions.RequestException as error:

            st.error(
                "Could not connect to the FastAPI backend."
            )

            st.code(
                str(error)
            )


# =========================================================
# Footer
# =========================================================

st.divider()

st.caption(
    "Autonomous AI Data Analyst • FastAPI + Streamlit"
)