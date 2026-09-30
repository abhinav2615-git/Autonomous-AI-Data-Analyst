from pydantic import BaseModel, Field
from typing import Any


class DatasetInfo(BaseModel):
    """Basic information about a dataset."""
    file_name: str
    rows: int
    columns: int
    column_names: list[str]


class AnalysisRequest(BaseModel):
    """Represent a user's data analysis request."""
    question: str = Field(min_length=1)
    dataset_name: str | None = None


class AnalysisResult(BaseModel):
    """Represent the result of a data analysis operation."""
    operation: str
    success: bool
    result: Any
    explanation: str | None = None


class ChartResult(BaseModel):
    """Represent a generated chart."""
    chart_type: str
    file_path: str
    title: str