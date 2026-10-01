from src.agent.mock_llm import MockPlanner
from src.models.agent import AnalysisPlan, ReplanRequest


class Replanner:
    """Create a new analysis plan when existing results are insufficient."""

    def __init__(self) -> None:
        self.planner = MockPlanner()

    def create_replan(
        self,
        question: str,
        request: ReplanRequest,
    ) -> AnalysisPlan:
        """
        Create a revised analysis plan.

        The current implementation uses deterministic
        rules. A future version can use an LLM.
        """

        if not question.strip():
            raise ValueError(
                "Question cannot be empty."
            )

        if not request.reason.strip():
            raise ValueError(
                "Re-plan reason cannot be empty."
            )

        initial_plan = self.planner.create_plan(
            question
        )

        previous_tools = set(
            request.previous_tools
        )

        new_tools = [
            tool
            for tool in initial_plan.tools
            if tool not in previous_tools
        ]

        if new_tools:
            return AnalysisPlan(
                objective=initial_plan.objective,
                steps=initial_plan.steps,
                tools=new_tools,
            )

        alternative_tool = self._find_alternative_tool(
            question=question,
            previous_tools=previous_tools,
        )

        if alternative_tool is None:
            return AnalysisPlan(
                objective=initial_plan.objective,
                steps=initial_plan.steps,
                tools=[],
            )

        return AnalysisPlan(
            objective=initial_plan.objective,
            steps=[
                (
                    f"Use {alternative_tool} "
                    "to obtain additional analysis results."
                )
            ],
            tools=[alternative_tool],
        )

    def _find_alternative_tool(
        self,
        question: str,
        previous_tools: set[str],
    ) -> str | None:
        """Find a relevant alternative analysis tool."""

        question_lower = question.lower()

        alternatives = []

        if (
            "country" in question_lower
            and "revenue" in question_lower
        ):
            alternatives = [
                "revenue_by_country",
                "revenue_by_month",
                "revenue_by_year",
            ]

        elif (
            "product" in question_lower
            and "revenue" in question_lower
        ):
            alternatives = [
                "revenue_by_product",
                "top_products_by_revenue",
                "units_by_product",
            ]

        elif (
            "customer" in question_lower
            and "revenue" in question_lower
        ):
            alternatives = [
                "revenue_by_customer",
                "top_customers_by_revenue",
            ]

        elif (
            "month" in question_lower
            or "monthly" in question_lower
        ):
            alternatives = [
                "revenue_by_month",
                "revenue_by_year",
            ]

        elif (
            "year" in question_lower
            or "yearly" in question_lower
            or "annual" in question_lower
        ):
            alternatives = [
                "revenue_by_year",
                "revenue_by_month",
            ]

        for tool in alternatives:
            if tool not in previous_tools:
                return tool

        return None