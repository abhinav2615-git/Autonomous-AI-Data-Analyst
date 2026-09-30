import os

from dotenv import load_dotenv
from openai import OpenAI


load_dotenv()


def get_openai_client() -> OpenAI:
    """Create and return an OpenAI client."""

    api_key = os.getenv("OPENAI_API_KEY")

    if not api_key:
        raise ValueError(
            "OPENAI_API_KEY is not set. "
            "Add it to the .env file."
        )

    return OpenAI(api_key=api_key)


def ask_llm(
    question: str,
    model: str = "gpt-5.6-luna",
) -> str:
    """Send a question to the LLM and return its response."""

    if not question.strip():
        raise ValueError("Question cannot be empty.")

    client = get_openai_client()

    response = client.responses.create(
        model=model,
        input=question,
    )

    return response.output_text