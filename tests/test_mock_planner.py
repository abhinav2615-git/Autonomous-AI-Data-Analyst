from src.agent.mock_llm import create_mock_analysis_plan


def main() -> None:
    questions = [
        "Which country generated the highest revenue?",
        "Which products generated the highest revenue?",
        "Show me monthly revenue.",
        "Which year generated the highest revenue?",
        "Which customers generated the highest revenue?",
    ]

    for question in questions:
        plan = create_mock_analysis_plan(question)

        print("\nQUESTION")
        print("-------------------------")
        print(question)

        print("\nOBJECTIVE")
        print(plan.objective)

        print("\nTOOLS")
        for tool in plan.tools:
            print(f"- {tool}")


if __name__ == "__main__":
    main()