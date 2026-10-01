from pathlib import Path
from tempfile import NamedTemporaryFile

from fastapi import FastAPI, File, Form, HTTPException, UploadFile
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from src.agent.chart_router import generate_chart_for_tool
from src.agent.executor import AgentExecutor
from src.agent.mock_llm import create_mock_analysis_plan
from src.agent.tools import create_tool_registry
from src.tools.data_loader import load_data


app = FastAPI(
    title="Autonomous AI Data Analyst",
    description="Backend API for the AI-powered data analysis agent.",
    version="1.0.0",
)


CHART_DIRECTORY = Path("data/outputs/charts")

CHART_DIRECTORY.mkdir(
    parents=True,
    exist_ok=True,
)


app.mount(
    "/charts",
    StaticFiles(directory=str(CHART_DIRECTORY)),
    name="charts",
)


@app.get("/")
def root() -> dict[str, str]:
    """Return basic API information."""

    return {
        "message": "Autonomous AI Data Analyst API is running.",
        "status": "success",
    }


@app.get("/health")
def health_check() -> dict[str, str]:
    """Check whether the backend is running."""

    return {
        "status": "healthy",
    }


@app.post("/profile")
async def profile_dataset(
    file: UploadFile = File(...),
) -> dict:
    """Upload a CSV/XLSX dataset and return its profile."""

    if not file.filename:
        raise HTTPException(
            status_code=400,
            detail="A dataset file is required.",
        )

    supported_extensions = {
        ".csv",
        ".xlsx",
        ".xls",
    }

    file_extension = Path(
        file.filename
    ).suffix.lower()

    if file_extension not in supported_extensions:
        raise HTTPException(
            status_code=400,
            detail=(
                "Unsupported file type. "
                "Use CSV, XLSX, or XLS."
            ),
        )

    try:
        file_bytes = await file.read()

        with NamedTemporaryFile(
            suffix=file_extension,
            delete=False,
        ) as temporary_file:
            temporary_file.write(file_bytes)
            temporary_file_path = temporary_file.name

        dataset = load_data(
            temporary_file_path
        )

        registry = create_tool_registry()

        executor = AgentExecutor(
            registry
        )

        profile = executor.profile_dataset(
            dataset
        )

        return {
            "status": "success",
            "file_name": file.filename,
            "profile": profile,
        }

    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail=f"Profiling failed: {error}",
        ) from error

    finally:
        if "temporary_file_path" in locals():
            Path(
                temporary_file_path
            ).unlink(
                missing_ok=True
            )


@app.post("/analyze")
async def analyze_dataset(
    file: UploadFile = File(...),
    question: str = Form(...),
) -> dict:
    """Analyze an uploaded dataset using the AI agent."""

    if not question.strip():
        raise HTTPException(
            status_code=400,
            detail="Question cannot be empty.",
        )

    if not file.filename:
        raise HTTPException(
            status_code=400,
            detail="A dataset file is required.",
        )

    supported_extensions = {
        ".csv",
        ".xlsx",
        ".xls",
    }

    file_extension = Path(
        file.filename
    ).suffix.lower()

    if file_extension not in supported_extensions:
        raise HTTPException(
            status_code=400,
            detail=(
                "Unsupported file type. "
                "Use CSV, XLSX, or XLS."
            ),
        )

    try:
        file_bytes = await file.read()

        with NamedTemporaryFile(
            suffix=file_extension,
            delete=False,
        ) as temporary_file:
            temporary_file.write(file_bytes)
            temporary_file_path = temporary_file.name

        dataset = load_data(
            temporary_file_path
        )

        # --------------------------------------------------
        # CREATE TOOL REGISTRY
        # --------------------------------------------------

        registry = create_tool_registry()

        # --------------------------------------------------
        # CREATE ANALYSIS PLAN
        # --------------------------------------------------

        planner = create_mock_analysis_plan(
            question
        )

        # --------------------------------------------------
        # EXECUTE ANALYSIS
        # --------------------------------------------------

        executor = AgentExecutor(
            registry
        )

        results = executor.execute_plan(
            planner,
            dataset,
        )

        response = executor.create_response(
            planner,
            results,
        )

        # --------------------------------------------------
        # AUTOMATIC CHART GENERATION
        # --------------------------------------------------

        chart_url = None

        if planner.tools:

            selected_tool = planner.tools[0]

            chart_url = generate_chart_for_tool(
                selected_tool,
                dataset,
            )

        # --------------------------------------------------
        # RETURN RESPONSE
        # --------------------------------------------------

        return {
            "status": response.status,
            "answer": response.answer,
            "confidence": response.confidence,
            "tools_used": response.tools_used,
            "chart_url": chart_url,
            "dataset": {
                "file_name": file.filename,
                "rows": len(dataset),
                "columns": len(dataset.columns),
                "column_names": dataset.columns.tolist(),
            },
            "plan": {
                "objective": planner.objective,
                "steps": planner.steps,
                "tools": planner.tools,
            },
        }

    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail=f"Analysis failed: {error}",
        ) from error

    finally:
        if "temporary_file_path" in locals():
            Path(
                temporary_file_path
            ).unlink(
                missing_ok=True
            )


@app.get("/charts/{filename}")
def get_chart(
    filename: str,
) -> FileResponse:
    """Return a generated chart image."""

    chart_path = (
        CHART_DIRECTORY / filename
    )

    if not chart_path.exists():
        raise HTTPException(
            status_code=404,
            detail="Chart not found.",
        )

    return FileResponse(
        chart_path,
        media_type="image/png",
    )