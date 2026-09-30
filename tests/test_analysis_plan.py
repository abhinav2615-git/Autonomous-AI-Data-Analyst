from src.agent.mock_llm import create_mock_analysis_plan


def main() -> None:
    question = "Which country generated the highest revenue?"

    plan = create_mock_analysis_plan(question)

    print("\nANALYSIS PLAN")
    print("-------------------------")

    print("Objective:")
    print(plan.objective)

    print("\nSteps:")

    for step in plan.steps:
        print(f"- {step}")

    print("\nTools:")
    
    for tool in plan.tools:
        print(f"- {tool}")


if __name__ == "__main__":
    main()