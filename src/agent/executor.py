from typing import Any

import pandas as pd

from src.agent.tool_registry import ToolRegistry
from src.models.agent import AnalysisPlan


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