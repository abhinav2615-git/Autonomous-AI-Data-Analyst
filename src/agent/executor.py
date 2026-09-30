from typing import Any

import pandas as pd

from src.agent.result_interpreter import interpret_result
from src.agent.tool_registry import ToolRegistry
from src.models.agent import AgentResponse, AnalysisPlan


class AgentExecutor:
    """Execute tools selected by the AI agent."""

    def __init__(self, registry: ToolRegistry) -> None:
        self.registry = registry

    def profile_dataset(
        self,
        df: pd.DataFrame,
    ) -> dict[str, Any]:
        """Profile the dataset before analysis."""

        profiler = self.registry.get(
            "data_profiler"
        )

        profile = profiler(df)

        return profile

    def execute_plan(
        self,
        plan: AnalysisPlan,
        df: pd.DataFrame,
    ) -> dict[str, Any]:
        """Execute all tools listed in the analysis plan."""

        results: dict[str, Any] = {}

        for tool_name in plan.tools:
            tool = self.registry.get(
                tool_name
            )

            result = tool(df)

            results[tool_name] = result

        return results

    def create_response(
        self,
        plan: AnalysisPlan,
        results: dict[str, Any],
    ) -> AgentResponse:
        """Convert tool results into a structured agent response."""

        if not results:
            return AgentResponse(
                answer="No analysis results were generated.",
                confidence=0.0,
                tools_used=plan.tools,
                status="failed",
            )

        first_tool = plan.tools[0]
        result = results[first_tool]

        answer = interpret_result(
            first_tool,
            result,
        )

        return AgentResponse(
            answer=answer,
            confidence=0.95,
            tools_used=plan.tools,
            status="success",
        )