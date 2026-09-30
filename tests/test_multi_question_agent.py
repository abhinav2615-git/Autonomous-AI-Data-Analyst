from src.agent.executor import AgentExecutor
from src.agent.mock_llm import create_mock_analysis_plan
from src.agent.tools import create_tool_registry
from src.tools.data_loader import load_data


def main() -> None:
    print("Loading dataset...")

    df = load_data(
        "data/datasets/Online Retail.xlsx"
    )

    print(f"Dataset loaded: {len(df)} rows")

    questions = [
        "Which country generated the highest revenue?",
        "Which products generated the highest revenue?",
        "Show me monthly revenue.",
        "Which year generated the highest revenue?",
        "Which customers generated the highest revenue?",
    ]

    registry = create_tool_registry()
    executor = AgentExecutor(registry)

    for question in questions:
        print("\n" + "=" * 60)
        print(f"QUESTION: {question}")
        print("=" * 60)

        plan = create_mock_analysis_plan(question)

        print(f"\nObjective: {plan.objective}")

        print("\nSelected tool:")
        for tool in plan.tools:
            print(f"- {tool}")

        print("\nExecuting...")

        results = executor.execute_plan(
            plan,
            df,
        )

        response = executor.create_response(
            plan,
            results,
        )

        print("\nAgent Response:")
        print(f"- Answer: {response.answer}")
        print(f"- Confidence: {response.confidence}")
        print(f"- Tools Used: {response.tools_used}")
        print(f"- Status: {response.status}")


if __name__ == "__main__":
    main()