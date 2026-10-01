from src.agent.mock_llm import MockPlanner
from src.agent.planner import BasePlanner
from src.agent.planner_factory import FallbackPlanner


class FailingPlanner(BasePlanner):
    """Planner that intentionally fails for testing."""

    def create_plan(self, question: str):
        raise RuntimeError(
            "Simulated LLM failure."
        )


def main():
    fallback = MockPlanner()

    planner = FallbackPlanner(
        primary=FailingPlanner(),
        fallback=fallback,
    )

    plan = planner.create_plan(
        "Which country generated the highest revenue?"
    )

    print("Planner fallback test passed.")
    print("Objective:", plan.objective)
    print("Tools:", plan.tools)


if __name__ == "__main__":
    main()