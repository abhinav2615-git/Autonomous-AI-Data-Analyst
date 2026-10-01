from typing import Any

import pandas as pd

from src.agent.result_interpreter import interpret_result
from src.agent.result_verifier import ResultVerifier
from src.agent.tool_registry import ToolRegistry
from src.models.agent import (
    AgentResponse,
    AnalysisPlan,
    ExecutionStep,
)


class AgentExecutor:
    """Execute analysis plans using registered tools."""

    def __init__(self, registry: ToolRegistry) -> None:
        self.registry = registry
        self.verifier = ResultVerifier()

    def profile_dataset(
        self,
        df: pd.DataFrame,
    ) -> dict:
        """Profile the uploaded dataset."""
        profiler = self.registry.get("data_profiler")
        return profiler(df)

    def execute_step(
        self,
        tool_name: str,
        df: pd.DataFrame,
    ) -> Any:
        """Execute one analysis step."""
        tool = self.registry.get(tool_name)
        return tool(df)

    def execute_plan(
        self,
        plan: AnalysisPlan,
        df: pd.DataFrame,
    ) -> tuple[dict[str, Any], list[ExecutionStep]]:
        """
        Execute and verify every tool in the analysis plan.

        Each tool is executed independently. Its result is
        verified before being accepted for interpretation.
        """

        results: dict[str, Any] = {}
        execution_steps: list[ExecutionStep] = []

        for step_number, tool_name in enumerate(
            plan.tools,
            start=1,
        ):
            print(
                f"Executing step {step_number}: "
                f"{tool_name}"
            )

            try:
                result = self.execute_step(
                    tool_name,
                    df,
                )

                verification = self.verifier.verify(
                    tool_name,
                    result,
                )

                if not verification["valid"]:
                    error_message = verification["reason"]

                    print(
                        f"Verification failed: "
                        f"{tool_name} -> {error_message}"
                    )

                    results[tool_name] = {
                        "error": error_message,
                    }

                    execution_steps.append(
                        ExecutionStep(
                            step_number=step_number,
                            tool_name=tool_name,
                            success=False,
                            error=error_message,
                        )
                    )

                    continue

                results[tool_name] = result

                print(
                    f"Verification passed: "
                    f"{tool_name}"
                )

                execution_steps.append(
                    ExecutionStep(
                        step_number=step_number,
                        tool_name=tool_name,
                        success=True,
                    )
                )

            except Exception as error:
                error_message = str(error)

                print(
                    f"Step {step_number} failed: "
                    f"{tool_name} -> {error_message}"
                )

                results[tool_name] = {
                    "error": error_message,
                }

                execution_steps.append(
                    ExecutionStep(
                        step_number=step_number,
                        tool_name=tool_name,
                        success=False,
                        error=error_message,
                    )
                )

        return results, execution_steps

    def interpret_results(
        self,
        plan: AnalysisPlan,
        results: dict[str, Any],
    ) -> list[str]:
        """Interpret verified tool results."""

        interpretations: list[str] = []

        for tool_name in plan.tools:

            if tool_name not in results:
                continue

            result = results[tool_name]

            if (
                isinstance(result, dict)
                and "error" in result
            ):
                continue

            interpretation = interpret_result(
                tool_name,
                result,
            )

            if interpretation:
                interpretations.append(
                    interpretation
                )

        return interpretations

    def create_response(
        self,
        plan: AnalysisPlan,
        results: dict[str, Any],
        execution_steps: list[ExecutionStep],
    ) -> AgentResponse:
        """Create the final agent response."""

        if not results:
            return AgentResponse(
                answer="No analysis results were generated.",
                confidence=0.0,
                tools_used=[],
                execution_steps=execution_steps,
                status="failed",
            )

        interpretations = self.interpret_results(
            plan,
            results,
        )

        successful_tools = [
            step.tool_name
            for step in execution_steps
            if step.success
        ]

        failed_tools = [
            step.tool_name
            for step in execution_steps
            if not step.success
        ]

        if not interpretations:
            return AgentResponse(
                answer=(
                    "No verified analysis results "
                    "were available to generate "
                    "an answer."
                ),
                confidence=0.0,
                tools_used=successful_tools,
                execution_steps=execution_steps,
                status="failed",
            )

        answer_parts = interpretations

        if failed_tools:
            answer_parts.append(
                "The following analysis steps "
                "could not be verified or completed: "
                + ", ".join(failed_tools)
                + "."
            )

        return AgentResponse(
            answer="\n\n".join(answer_parts),
            confidence=0.95,
            tools_used=successful_tools,
            execution_steps=execution_steps,
            status="success",
        )