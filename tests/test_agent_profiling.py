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

    question = "Tell me about this dataset."

    print("\nUser Question:")
    print(question)

    print("\nCreating analysis plan...")

    plan = create_mock_analysis_plan(question)

    print("\nSelected Tool:")
    for tool in plan.tools:
        print(f"- {tool}")

    registry = create_tool_registry()
    executor = AgentExecutor(registry)

    print("\nExecuting profiler...")

    results = executor.execute_plan(
        plan,
        df,
    )

    profile = results["data_profiler"]

    print("\nDATASET PROFILE")
    print("=========================")

    print(f"Rows: {profile['rows']}")
    print(f"Columns: {profile['columns']}")

    print("\nColumn Names:")
    for column in profile["column_names"]:
        print(f"- {column}")

    print("\nData Types:")
    for column, dtype in profile["data_types"].items():
        print(f"- {column}: {dtype}")

    print("\nMissing Values:")
    if profile["missing_values"]:
        for column, count in profile["missing_values"].items():
            print(f"- {column}: {count}")
    else:
        print("- No missing values")

    print("\nUnique Values:")
    for column, count in profile["unique_values"].items():
        print(f"- {column}: {count}")

    print("\nNumerical Summary:")
    print(profile["numerical_summary"])


if __name__ == "__main__":
    main()