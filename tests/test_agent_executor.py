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

    print("\nEXECUTION COMPLETE")
    print("-------------------------")

    for tool_name, result in results.items():
        print(f"\nTool: {tool_name}")
        print(result.head(10))


if __name__ == "__main__":
    main()