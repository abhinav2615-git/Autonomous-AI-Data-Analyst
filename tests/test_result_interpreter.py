from src.agent.executor import AgentExecutor
from src.agent.mock_llm import create_mock_analysis_plan
from src.agent.tools import create_tool_registry
from src.tools.data_loader import load_data


def main() -> None:
    print("Loading dataset...")

    df = load_data(
        "data/datasets/Online Retail.xlsx"
    )

    registry = create_tool_registry()
    executor = AgentExecutor(registry)

    questions = [
        "Which country generated the highest revenue?",
        "Which products generated the highest revenue?",
        "Which customers generated the highest revenue?",
        "Which year generated the highest revenue?",
    ]

    for question in questions:
        print("\n" + "=" * 60)
        print(f"QUESTION: {question}")
        print("=" * 60)

        plan = create_mock_analysis_plan(question)

        results = executor.execute_plan(
            plan,
            df,
        )

        response = executor.create_response(
            plan,
            results,
        )

        print("\nFINAL ANSWER:")
        print(response.answer)

        print("\nSTATUS:")
        print(response.status)


if __name__ == "__main__":
    main()