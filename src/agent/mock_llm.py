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
            objective="Analyze revenue by country.",
            steps=[
                "Calculate revenue using Quantity × UnitPrice.",
                "Group revenue by Country.",
                "Sort countries by revenue in descending order.",
                "Return the countries ranked by revenue.",
            ],
            tools=["revenue_by_country"],
        )

    if "product" in question_lower and "revenue" in question_lower:
        return AnalysisPlan(
            objective="Analyze revenue by product.",
            steps=[
                "Calculate revenue using Quantity × UnitPrice.",
                "Group revenue by product.",
                "Sort products by revenue in descending order.",
                "Return the products ranked by revenue.",
            ],
            tools=["revenue_by_product"],
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
            tools=["revenue_by_month"],
        )

    if "year" in question_lower and "revenue" in question_lower:
        return AnalysisPlan(
            objective="Analyze revenue by year.",
            steps=[
                "Calculate revenue using Quantity × UnitPrice.",
                "Extract the year from InvoiceDate.",
                "Group revenue by year.",
                "Compare yearly revenue.",
            ],
            tools=["revenue_by_year"],
        )

    if "customer" in question_lower and "revenue" in question_lower:
        return AnalysisPlan(
            objective="Analyze revenue by customer.",
            steps=[
                "Calculate revenue using Quantity × UnitPrice.",
                "Group revenue by CustomerID.",
                "Sort customers by revenue in descending order.",
                "Return the customers ranked by revenue.",
            ],
            tools=["top_customers_by_revenue"],
        )

    return AnalysisPlan(
        objective=question,
        steps=[
            "Inspect the dataset.",
            "Identify the relevant columns.",
            "Perform the required analysis.",
            "Return the results.",
        ],
        tools=["data_profiler"],
    )