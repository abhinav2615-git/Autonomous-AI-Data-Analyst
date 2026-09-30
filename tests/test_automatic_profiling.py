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

    registry = create_tool_registry()
    executor = AgentExecutor(registry)

    print("\nProfiling dataset before analysis...")

    profile = executor.profile_dataset(df)

    print("\nDATASET SUMMARY")
    print("=========================")
    print(f"Rows: {profile['rows']}")
    print(f"Columns: {profile['columns']}")

    print("\nMissing Values:")

    if profile["missing_values"]:
        for column, count in profile["missing_values"].items():
            print(f"- {column}: {count}")
    else:
        print("- No missing values")

    question = (
        "Which country generated the highest revenue?"
    )

    print("\nUser Question:")
    print(question)

    plan = create_mock_analysis_plan(
        question
    )

    print("\nSelected Tool:")
    for tool in plan.tools:
        print(f"- {tool}")

    print("\nExecuting analysis...")

    results = executor.execute_plan(
        plan,
        df,
    )

    response = executor.create_response(
        plan,
        results,
    )

    print("\nFINAL ANSWER")
    print("=========================")
    print(response.answer)

    print("\nStatus:")
    print(response.status)


if __name__ == "__main__":
    main()