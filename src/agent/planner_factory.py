import os

from src.agent.mock_llm import MockPlanner
from src.agent.llm_planner import LLMPlanner
from src.agent.planner import BasePlanner
from src.agent.tool_registry import ToolRegistry


def create_planner(registry: ToolRegistry) -> BasePlanner:
    """
    Create the appropriate planner based on environment configuration.

    By default, the system uses MockPlanner so the application
    works without an external LLM API.

    Set USE_LLM_PLANNER=true to use LLMPlanner.
    """

    use_llm = os.getenv("USE_LLM_PLANNER", "false").lower() == "true"

    if use_llm:
        return LLMPlanner(registry)

    return MockPlanner()