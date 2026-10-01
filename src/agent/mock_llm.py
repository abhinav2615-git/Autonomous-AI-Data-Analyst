from src.agent.planner import BasePlanner
from src.models.agent import AnalysisPlan


class MockPlanner(BasePlanner):
    """Rule-based planner used for development."""

    def create_plan(
        self,
        question: str,
    ) -> AnalysisPlan:
        """Create an analysis plan without an LLM."""

        if not question.strip():
            raise ValueError(
                "Question cannot be empty."
            )

        question_lower = question.lower()

        # -----------------------------------------------------
        # MULTI-TOOL: COUNTRY + MONTHLY REVENUE
        # -----------------------------------------------------

        if (
            "country" in question_lower
            and "revenue" in question_lower
            and (
                "month" in question_lower
                or "monthly" in question_lower
            )
        ):
            return AnalysisPlan(
                objective=(
                    "Analyze revenue by country "
                    "and examine the monthly revenue trend."
                ),
                steps=[
                    "Calculate revenue using Quantity × UnitPrice.",
                    "Group revenue by Country.",
                    "Identify the highest-revenue countries.",
                    "Group revenue by month.",
                    "Analyze the monthly revenue trend.",
                ],
                tools=[
                    "revenue_by_country",
                    "revenue_by_month",
                ],
            )

        # -----------------------------------------------------
        # MULTI-TOOL: PRODUCT + COUNTRY
        # -----------------------------------------------------

        if (
            "product" in question_lower
            and "country" in question_lower
            and "revenue" in question_lower
        ):
            return AnalysisPlan(
                objective=(
                    "Analyze revenue by product "
                    "and country."
                ),
                steps=[
                    "Calculate revenue using Quantity × UnitPrice.",
                    "Group revenue by product.",
                    "Identify the highest-revenue products.",
                    "Group revenue by country.",
                    "Identify the highest-revenue countries.",
                ],
                tools=[
                    "revenue_by_product",
                    "revenue_by_country",
                ],
            )

        # -----------------------------------------------------
        # MULTI-TOOL: CUSTOMER + COUNTRY
        # -----------------------------------------------------

        if (
            "customer" in question_lower
            and "country" in question_lower
            and "revenue" in question_lower
        ):
            return AnalysisPlan(
                objective=(
                    "Analyze revenue by customer "
                    "and country."
                ),
                steps=[
                    "Calculate revenue using Quantity × UnitPrice.",
                    "Group revenue by customer.",
                    "Identify the highest-revenue customers.",
                    "Group revenue by country.",
                    "Identify the highest-revenue countries.",
                ],
                tools=[
                    "revenue_by_customer",
                    "revenue_by_country",
                ],
            )

        # -----------------------------------------------------
        # COUNTRY + REVENUE
        # -----------------------------------------------------

        if (
            "country" in question_lower
            and "revenue" in question_lower
        ):
            return AnalysisPlan(
                objective="Analyze revenue by country.",
                steps=[
                    "Calculate revenue using Quantity × UnitPrice.",
                    "Group revenue by Country.",
                    "Sort countries by revenue.",
                    "Return the country-level revenue results.",
                ],
                tools=[
                    "revenue_by_country"
                ],
            )

        # -----------------------------------------------------
        # TOP PRODUCTS + REVENUE
        # -----------------------------------------------------

        if (
            (
                "top" in question_lower
                or "highest" in question_lower
            )
            and "product" in question_lower
            and "revenue" in question_lower
        ):
            return AnalysisPlan(
                objective=(
                    "Find the products "
                    "with the highest revenue."
                ),
                steps=[
                    "Calculate revenue using Quantity × UnitPrice.",
                    "Group revenue by product.",
                    "Sort products by revenue in descending order.",
                    "Return the top products by revenue.",
                ],
                tools=[
                    "top_products_by_revenue"
                ],
            )

        # -----------------------------------------------------
        # PRODUCT + REVENUE
        # -----------------------------------------------------

        if (
            "product" in question_lower
            and "revenue" in question_lower
        ):
            return AnalysisPlan(
                objective="Analyze revenue by product.",
                steps=[
                    "Calculate revenue using Quantity × UnitPrice.",
                    "Group revenue by product.",
                    "Sort products by revenue.",
                    "Return the product-level revenue results.",
                ],
                tools=[
                    "revenue_by_product"
                ],
            )

        # -----------------------------------------------------
        # PRODUCT + UNITS
        # -----------------------------------------------------

        if (
            "product" in question_lower
            and (
                "unit" in question_lower
                or "quantity" in question_lower
                or "sold" in question_lower
            )
        ):
            return AnalysisPlan(
                objective="Analyze units sold by product.",
                steps=[
                    "Group the dataset by product.",
                    "Calculate total units sold for each product.",
                    "Sort products by units sold.",
                    "Return the product-level unit results.",
                ],
                tools=[
                    "units_by_product"
                ],
            )

        # -----------------------------------------------------
        # TOP CUSTOMERS + REVENUE
        # -----------------------------------------------------

        if (
            (
                "top" in question_lower
                or "highest" in question_lower
            )
            and "customer" in question_lower
            and "revenue" in question_lower
        ):
            return AnalysisPlan(
                objective=(
                    "Find the customers "
                    "with the highest revenue."
                ),
                steps=[
                    "Calculate revenue using Quantity × UnitPrice.",
                    "Group revenue by CustomerID.",
                    "Sort customers by revenue in descending order.",
                    "Return the top customers by revenue.",
                ],
                tools=[
                    "top_customers_by_revenue"
                ],
            )

        # -----------------------------------------------------
        # CUSTOMER + REVENUE
        # -----------------------------------------------------

        if (
            "customer" in question_lower
            and "revenue" in question_lower
        ):
            return AnalysisPlan(
                objective="Analyze revenue by customer.",
                steps=[
                    "Calculate revenue using Quantity × UnitPrice.",
                    "Group revenue by CustomerID.",
                    "Sort customers by revenue.",
                    "Return the customer-level revenue results.",
                ],
                tools=[
                    "revenue_by_customer"
                ],
            )

        # -----------------------------------------------------
        # MONTH + REVENUE
        # -----------------------------------------------------

        if (
            (
                "month" in question_lower
                or "monthly" in question_lower
            )
            and "revenue" in question_lower
        ):
            return AnalysisPlan(
                objective=(
                    "Analyze revenue over time by month."
                ),
                steps=[
                    "Calculate revenue using Quantity × UnitPrice.",
                    "Extract the month from InvoiceDate.",
                    "Group revenue by month.",
                    "Compare monthly revenue.",
                ],
                tools=[
                    "revenue_by_month"
                ],
            )

        # -----------------------------------------------------
        # YEAR + REVENUE
        # -----------------------------------------------------

        if (
            (
                "year" in question_lower
                or "yearly" in question_lower
                or "annual" in question_lower
            )
            and "revenue" in question_lower
        ):
            return AnalysisPlan(
                objective=(
                    "Analyze revenue over time by year."
                ),
                steps=[
                    "Calculate revenue using Quantity × UnitPrice.",
                    "Extract the year from InvoiceDate.",
                    "Group revenue by year.",
                    "Compare yearly revenue.",
                ],
                tools=[
                    "revenue_by_year"
                ],
            )

        # -----------------------------------------------------
        # CANCELLATIONS
        # -----------------------------------------------------

        if (
            "cancel" in question_lower
            or "cancellation" in question_lower
            or "cancelled" in question_lower
        ):
            return AnalysisPlan(
                objective="Analyze cancelled transactions.",
                steps=[
                    "Identify invoices beginning with C.",
                    "Filter cancelled transactions.",
                    "Return the cancelled transaction records.",
                ],
                tools=[
                    "cancelled_transactions"
                ],
            )

        # -----------------------------------------------------
        # FALLBACK
        # -----------------------------------------------------

        return AnalysisPlan(
            objective=question,
            steps=[
                "Inspect the dataset.",
                "Identify the relevant columns.",
                "Perform the required analysis.",
                "Return the results.",
            ],
            tools=[
                "data_profiler"
            ],
        )


def create_mock_analysis_plan(
    question: str,
) -> AnalysisPlan:
    """Backward-compatible helper for existing code."""

    planner = MockPlanner()

    return planner.create_plan(
        question
    )