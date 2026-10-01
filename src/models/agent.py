from typing import Any, Literal

from pydantic import BaseModel, Field


class ToolCall(BaseModel):
    tool_name: str
    arguments: dict[str, Any] = Field(default_factory=dict)


class AnalysisPlan(BaseModel):
    objective: str
    steps: list[str]
    tools: list[str]


class ExecutionStep(BaseModel):
    step_number: int
    tool_name: str
    success: bool
    error: str | None = None


class AgentResponse(BaseModel):
    answer: str
    confidence: float = Field(ge=0.0, le=1.0)
    tools_used: list[str] = Field(default_factory=list)
    execution_steps: list[ExecutionStep] = Field(default_factory=list)
    status: Literal["success", "failed", "needs_input"]