from pathlib import Path
from tempfile import NamedTemporaryFile

from fastapi import FastAPI, File, Form, UploadFile
from fastapi.staticfiles import StaticFiles

from src.agent.chart_router import generate_chart_for_tool
from src.agent.executor import AgentExecutor
from src.agent.planner_factory import create_planner
from src.agent.tools import create_tool_registry
from src.tools.data_loader import load_data


app = FastAPI(
    title="Autonomous AI Data Analyst",
    description="AI-powered data analysis API",
    version="1.0.0",
)


CHART_DIRECTORY = Path("data/outputs/charts")
CHART_DIRECTORY.mkdir(
    parents=True,
    exist_ok=True,
)


app.mount(
    "/charts",
    StaticFiles(directory=CHART_DIRECTORY),
    name="charts",
)


@app.get("/")
def root():
    return {
        "message": (
            "Autonomous AI Data Analyst API "
            "is running."
        )
    }


@app.get("/health")
def health():
    return {
        "status": "healthy"
    }


@app.post("/profile")
async def profile_dataset(
    file: UploadFile = File(...),
):
    suffix = Path(
        file.filename
    ).suffix.lower()

    if suffix not in [
        ".csv",
        ".xlsx",
        ".xls",
    ]:
        return {
            "status": "failed",
            "message": "Unsupported file type.",
        }

    temporary_path = None

    try:
        with NamedTemporaryFile(
            delete=False,
            suffix=suffix,
        ) as temporary_file:

            temporary_file.write(
                await file.read()
            )

            temporary_path = (
                temporary_file.name
            )

        dataframe = load_data(
            temporary_path
        )

        registry = create_tool_registry()

        executor = AgentExecutor(
            registry
        )

        profile = executor.profile_dataset(
            dataframe
        )

        return {
            "status": "success",
            "file_name": file.filename,
            "rows": len(dataframe),
            "columns": len(dataframe.columns),
            "column_names": (
                dataframe.columns.tolist()
            ),
            "profile": profile,
        }

    except Exception as error:

        return {
            "status": "failed",
            "message": str(error),
        }

    finally:

        if temporary_path:
            Path(
                temporary_path
            ).unlink(
                missing_ok=True
            )


@app.post("/analyze")
async def analyze_dataset(
    file: UploadFile = File(...),
    question: str = Form(...),
):
    suffix = Path(
        file.filename
    ).suffix.lower()

    if suffix not in [
        ".csv",
        ".xlsx",
        ".xls",
    ]:
        return {
            "status": "failed",
            "message": "Unsupported file type.",
        }

    if not question.strip():
        return {
            "status": "failed",
            "message": "Question cannot be empty.",
        }

    temporary_path = None

    try:

        with NamedTemporaryFile(
            delete=False,
            suffix=suffix,
        ) as temporary_file:

            temporary_file.write(
                await file.read()
            )

            temporary_path = (
                temporary_file.name
            )

        dataframe = load_data(
            temporary_path
        )

        registry = create_tool_registry()

        # Create the configured planner.
        #
        # USE_LLM_PLANNER=false
        #     -> MockPlanner
        #
        # USE_LLM_PLANNER=true
        #     -> LLMPlanner with fallback.
        planner = create_planner(
            registry
        )

        executor = AgentExecutor(
            registry
        )

        # Create the initial analysis plan.
        initial_plan = planner.create_plan(
            question
        )

        # Execute the plan with controlled
        # re-planning if results are insufficient.
        final_plan, results, execution_steps = (
            executor.execute_with_replanning(
                question=question,
                initial_plan=initial_plan,
                df=dataframe,
            )
        )

        # Create the final agent response.
        agent_response = (
            executor.create_response(
                final_plan,
                results,
                execution_steps,
            )
        )

        # Generate charts for tools that support
        # visualization.
        charts = []

        tools_for_charts = []

        for step in execution_steps:
            if (
                step.success
                and step.tool_name
                not in tools_for_charts
            ):
                tools_for_charts.append(
                    step.tool_name
                )

        for tool_name in tools_for_charts:

            chart_url = (
                generate_chart_for_tool(
                    tool_name,
                    dataframe,
                )
            )

            if chart_url:

                charts.append(
                    {
                        "tool": tool_name,
                        "url": chart_url,
                    }
                )

        return {
            "status": agent_response.status,
            "answer": agent_response.answer,
            "confidence": (
                agent_response.confidence
            ),
            "tools_used": (
                agent_response.tools_used
            ),
            "execution_steps": [
                step.model_dump()
                for step in (
                    agent_response
                    .execution_steps
                )
            ],
            "charts": charts,
            "dataset": {
                "file_name": file.filename,
                "rows": len(dataframe),
                "columns": len(dataframe.columns),
                "column_names": (
                    dataframe.columns.tolist()
                ),
            },
            "plan": {
                "objective": (
                    final_plan.objective
                ),
                "steps": (
                    final_plan.steps
                ),
                "tools": (
                    final_plan.tools
                ),
            },
        }

    except Exception as error:

        return {
            "status": "failed",
            "message": str(error),
        }

    finally:

        if temporary_path:

            Path(
                temporary_path
            ).unlink(
                missing_ok=True
            )


@app.get("/charts/{filename}")
def get_chart(
    filename: str,
):
    chart_path = (
        CHART_DIRECTORY / filename
    )

    if not chart_path.exists():

        return {
            "status": "failed",
            "message": "Chart not found.",
        }

    return {
        "status": "success",
        "filename": filename,
    }