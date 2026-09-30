from typing import Any

import pandas as pd

from src.agent.tool_registry import ToolRegistry
from src.models.agent import AgentResponse, AnalysisPlan


class AgentExecutor:
    """Execute tools selected by an analysis plan."""

    def __init__(self, registry: ToolRegistry) -> None:
        self.registry = registry

    def execute_plan(
        self,
        plan: AnalysisPlan,
        df: pd.DataFrame,
    ) -> dict[str, Any]:
        """Execute all tools listed in the analysis plan."""

        results: dict[str, Any] = {}

        for tool_name in plan.tools:
            tool = self.registry.get(tool_name)

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

        if isinstance(result, pd.DataFrame):
            if result.empty:
                answer = "The analysis returned no results."
                confidence = 0.5
            else:
                first_row = result.iloc[0]

                if "Country" in result.columns:
                    answer = (
                        f"The country with the highest revenue "
                        f"is {first_row['Country']}."
                    )
                    confidence = 0.95

                else:
                    answer = (
                        f"The analysis completed successfully "
                        f"using the {first_tool} tool."
                    )
                    confidence = 0.85

        else:
            answer = (
                f"The analysis completed successfully "
                f"using the {first_tool} tool."
            )
            confidence = 0.85

        return AgentResponse(
            answer=answer,
            confidence=confidence,
            tools_used=plan.tools,
            status="success",
        )