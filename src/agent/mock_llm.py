from src.models.agent import AnalysisPlan


def create_mock_analysis_plan(
    question: str,
) -> AnalysisPlan:
    """Create a mock analysis plan for development."""

    if not question.strip():
        raise ValueError("Question cannot be empty.")

    question_lower = question.lower()

    if "country" in question_lower and "revenue" in question_lower:
        return AnalysisPlan(
            objective="Find the country with the highest revenue.",
            steps=[
                "Calculate revenue using Quantity × UnitPrice.",
                "Group revenue by Country.",
                "Sort countries by revenue in descending order.",
                "Return the country with the highest revenue.",
            ],
            tools=[
                "revenue_by_country",
            ],
        )

    if "product" in question_lower and "revenue" in question_lower:
        return AnalysisPlan(
            objective="Find the products with the highest revenue.",
            steps=[
                "Calculate revenue using Quantity × UnitPrice.",
                "Group revenue by product.",
                "Sort products by revenue in descending order.",
                "Return the top products by revenue.",
            ],
            tools=[
                "top_products_by_revenue",
            ],
        )

    if "monthly" in question_lower and "revenue" in question_lower:
        return AnalysisPlan(
            objective="Analyze revenue across months.",
            steps=[
                "Calculate revenue using Quantity × UnitPrice.",
                "Extract the month from InvoiceDate.",
                "Group revenue by month.",
                "Compare monthly revenue.",
            ],
            tools=[
                "revenue_by_month",
            ],
        )

    return AnalysisPlan(
        objective=question,
        steps=[
            "Inspect the dataset.",
            "Identify the relevant columns.",
            "Perform the required analysis.",
            "Return the results.",
        ],
        tools=[
            "data_profiler",
        ],
    )