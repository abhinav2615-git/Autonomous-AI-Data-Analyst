import json

from src.agent.llm import ask_llm
from src.agent.planner import BasePlanner
from src.agent.tool_registry import ToolRegistry
from src.models.agent import AnalysisPlan


class LLMPlanner(BasePlanner):
    """Create analysis plans using an LLM."""

    def __init__(
        self,
        registry: ToolRegistry,
        model: str = "gpt-5.6-luna",
    ) -> None:
        self.registry = registry
        self.model = model

    def create_plan(
        self,
        question: str,
    ) -> AnalysisPlan:
        """Create a structured analysis plan using an LLM."""

        if not question.strip():
            raise ValueError(
                "Question cannot be empty."
            )

        prompt = self._build_prompt(
            question
        )

        response = ask_llm(
            prompt,
            model=self.model,
        )

        return self._parse_response(
            response
        )

    def _build_prompt(
        self,
        question: str,
    ) -> str:
        """Build the planning prompt using registered tools."""

        available_tools = (
            self.registry.list_tools()
        )

        tool_list = "\n".join(
            f"- {tool}"
            for tool in available_tools
        )

        return f"""
You are the planning component of an AI Data Analyst.

Your job is to convert the user's natural-language
question into a structured analysis plan.

These are the tools currently registered
in the system:

{tool_list}

Rules:

1. Select only tools from the registered tools above.
2. Use multiple tools when the question requires
   multiple analyses.
3. Do not invent tools.
4. Keep the objective concise.
5. Provide clear analysis steps.
6. Return ONLY valid JSON.
7. The JSON must contain exactly these fields:
   objective
   steps
   tools

Example:

{{
    "objective": "Analyze revenue by country.",
    "steps": [
        "Calculate revenue using Quantity × UnitPrice.",
        "Group revenue by Country.",
        "Sort countries by revenue."
    ],
    "tools": [
        "revenue_by_country"
    ]
}}

User question:

{question}
"""

    def _parse_response(
        self,
        response: str,
    ) -> AnalysisPlan:
        """Parse and validate the LLM response."""

        try:
            data = json.loads(
                response
            )

        except json.JSONDecodeError as error:
            raise ValueError(
                "LLM returned invalid JSON."
            ) from error

        plan = AnalysisPlan.model_validate(
            data
        )

        self._validate_tools(
            plan
        )

        return plan

    def _validate_tools(
        self,
        plan: AnalysisPlan,
    ) -> None:
        """Ensure the LLM selected only registered tools."""

        available_tools = set(
            self.registry.list_tools()
        )

        invalid_tools = [
            tool
            for tool in plan.tools
            if tool not in available_tools
        ]

        if invalid_tools:
            raise ValueError(
                "LLM selected unregistered tools: "
                f"{invalid_tools}"
            )