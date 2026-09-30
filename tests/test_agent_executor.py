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

    question = "Which country generated the highest revenue?"

    print("\nUser Question:")
    print(question)

    print("\nCreating analysis plan...")

    plan = create_mock_analysis_plan(question)

    print("\nSelected Tools:")
    for tool in plan.tools:
        print(f"- {tool}")

    registry = create_tool_registry()

    executor = AgentExecutor(registry)

    print("\nExecuting plan...")

    results = executor.execute_plan(
        plan,
        df,
    )

    print("\nCreating structured response...")

    response = executor.create_response(
        plan,
        results,
    )

    print("\nAGENT RESPONSE")
    print("-------------------------")
    print(f"Answer: {response.answer}")
    print(f"Confidence: {response.confidence}")
    print(f"Tools Used: {response.tools_used}")
    print(f"Status: {response.status}")


if __name__ == "__main__":
    main()