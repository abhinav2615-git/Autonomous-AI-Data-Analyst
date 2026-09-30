from src.agent.llm import ask_llm


def main() -> None:
    question = (
        "Explain in one sentence what a data analyst does."
    )

    response = ask_llm(question)

    print("\nLLM RESPONSE:")
    print(response)


if __name__ == "__main__":
    main()