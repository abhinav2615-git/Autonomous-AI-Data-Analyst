import os

from dotenv import load_dotenv

from src.agent.llm_planner import LLMPlanner
from src.agent.mock_llm import MockPlanner
from src.agent.planner import BasePlanner
from src.agent.tool_registry import ToolRegistry


load_dotenv()


class FallbackPlanner(BasePlanner):
    """
    Try the primary planner first.

    If the primary planner fails, use the fallback planner.
    """

    def __init__(
        self,
        primary: BasePlanner,
        fallback: BasePlanner,
    ) -> None:
        self.primary = primary
        self.fallback = fallback

    def create_plan(self, question: str):
        try:
            return self.primary.create_plan(question)

        except Exception as error:
            print(
                "Primary planner failed. "
                f"Using fallback planner. Error: {error}"
            )

            return self.fallback.create_plan(
                question
            )


def create_planner(
    registry: ToolRegistry,
) -> BasePlanner:
    """
    Create the configured analysis planner.

    USE_LLM_PLANNER=false
        -> MockPlanner

    USE_LLM_PLANNER=true
        -> LLMPlanner with MockPlanner fallback
    """

    use_llm = (
        os.getenv(
            "USE_LLM_PLANNER",
            "false",
        ).lower()
        == "true"
    )

    mock_planner = MockPlanner()

    if not use_llm:
        return mock_planner

    llm_planner = LLMPlanner(
        registry
    )

    return FallbackPlanner(
        primary=llm_planner,
        fallback=mock_planner,
    )