from dataclasses import dataclass


@dataclass(frozen=True)
class ToolIntent:
    """Describe the type of question a tool can answer."""

    keywords: tuple[str, ...]


TOOL_INTENTS = {
    "revenue_by_country": ToolIntent(
        keywords=(
            "country",
            "countries",
        ),
    ),
    "revenue_by_product": ToolIntent(
        keywords=(
            "product",
            "products",
        ),
    ),
    "revenue_by_customer": ToolIntent(
        keywords=(
            "customer",
            "customers",
        ),
    ),
    "top_products_by_revenue": ToolIntent(
        keywords=(
            "product",
            "products",
            "top",
            "highest",
        ),
    ),
    "top_customers_by_revenue": ToolIntent(
        keywords=(
            "customer",
            "customers",
            "top",
            "highest",
        ),
    ),
    "units_by_product": ToolIntent(
        keywords=(
            "product",
            "products",
            "units",
            "quantity",
            "sold",
        ),
    ),
    "revenue_by_month": ToolIntent(
        keywords=(
            "month",
            "monthly",
        ),
    ),
    "revenue_by_year": ToolIntent(
        keywords=(
            "year",
            "yearly",
            "annual",
        ),
    ),
    "cancelled_transactions": ToolIntent(
        keywords=(
            "cancel",
            "cancelled",
            "cancellation",
        ),
    ),
    "data_profiler": ToolIntent(
        keywords=(
            "profile",
            "overview",
            "summary",
            "dataset",
            "data",
        ),
    ),
}


def check_tool_question_compatibility(
    tool_name: str,
    question: str,
) -> dict:
    """
    Check whether a tool is relevant to the
    user's question.
    """

    if tool_name not in TOOL_INTENTS:
        raise KeyError(
            f"No intent definition found for tool: {tool_name}"
        )

    if not question.strip():
        return {
            "compatible": False,
            "tool_name": tool_name,
            "matched_keywords": [],
            "reason": "Question is empty.",
        }

    question_lower = question.lower()

    intent = TOOL_INTENTS[tool_name]

    matched_keywords = [
        keyword
        for keyword in intent.keywords
        if keyword in question_lower
    ]

    if matched_keywords:
        return {
            "compatible": True,
            "tool_name": tool_name,
            "matched_keywords": matched_keywords,
            "reason": (
                "Tool intent matches the user's question."
            ),
        }

    return {
        "compatible": False,
        "tool_name": tool_name,
        "matched_keywords": [],
        "reason": (
            "Tool intent does not match "
            "the user's question."
        ),
    }


def validate_tool_for_question(
    tool_name: str,
    question: str,
) -> None:
    """
    Validate that a tool is compatible with the question.

    Raises ValueError when the tool does not match
    the user's question.
    """

    result = check_tool_question_compatibility(
        tool_name=tool_name,
        question=question,
    )

    if not result["compatible"]:
        raise ValueError(
            f"Tool '{tool_name}' is not compatible "
            f"with the question. "
            f"{result['reason']}"
        )