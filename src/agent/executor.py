from typing import Any

import pandas as pd

from src.agent.replanner import Replanner
from src.agent.result_evaluator import ResultEvaluator
from src.agent.result_interpreter import interpret_result
from src.agent.result_verifier import ResultVerifier
from src.agent.tool_registry import ToolRegistry
from src.models.agent import (
    AgentResponse,
    AnalysisPlan,
    ExecutionStep,
    ReplanRequest,
)


MAX_REPLANS = 1


class AgentExecutor:
    """Execute analysis plans using registered tools."""

    def __init__(
        self,
        registry: ToolRegistry,
    ) -> None:
        self.registry = registry
        self.verifier = ResultVerifier()
        self.evaluator = ResultEvaluator()
        self.replanner = Replanner()

    def profile_dataset(
        self,
        df: pd.DataFrame,
    ) -> dict:
        """Profile the uploaded dataset."""

        profiler = self.registry.get(
            "data_profiler"
        )

        return profiler(df)

    def execute_step(
        self,
        tool_name: str,
        df: pd.DataFrame,
    ) -> Any:
        """Execute one analysis step."""

        tool = self.registry.get(
            tool_name
        )

        return tool(df)

    def execute_plan(
        self,
        plan: AnalysisPlan,
        df: pd.DataFrame,
        starting_step: int = 1,
    ) -> tuple[
        dict[str, Any],
        list[ExecutionStep],
    ]:
        """
        Execute and verify every tool in an analysis plan.
        """

        results: dict[str, Any] = {}

        execution_steps: list[
            ExecutionStep
        ] = []

        for step_number, tool_name in enumerate(
            plan.tools,
            start=starting_step,
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
                    error_message = (
                        verification["reason"]
                    )

                    print(
                        "Verification failed: "
                        f"{tool_name} -> "
                        f"{error_message}"
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
                    "Verification passed: "
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
                    f"{tool_name} -> "
                    f"{error_message}"
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

        return (
            results,
            execution_steps,
        )

    def evaluate_results(
        self,
        results: dict[str, Any],
    ) -> dict[str, Any]:
        """Evaluate whether results are sufficient."""

        return self.evaluator.evaluate(
            results
        )

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

    def calculate_confidence(
        self,
        execution_steps: list[ExecutionStep],
    ) -> float:
        """
        Calculate execution confidence based on
        successful tool verification.

        This is execution confidence, not statistical
        confidence or model certainty.
        """

        if not execution_steps:
            return 0.0

        successful_steps = sum(
            1
            for step in execution_steps
            if step.success
        )

        total_steps = len(
            execution_steps
        )

        return round(
            successful_steps / total_steps,
            2,
        )

    def create_response(
        self,
        plan: AnalysisPlan,
        results: dict[str, Any],
        execution_steps: list[ExecutionStep],
    ) -> AgentResponse:
        """Create the final agent response."""

        confidence = self.calculate_confidence(
            execution_steps
        )

        evaluation = self.evaluate_results(
            results
        )

        if not evaluation["sufficient"]:
            return AgentResponse(
                answer=(
                    "The analysis did not produce "
                    "sufficient verified results. "
                    f"{evaluation['reason']}"
                ),
                confidence=confidence,
                tools_used=[
                    step.tool_name
                    for step in execution_steps
                    if step.success
                ],
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
                confidence=confidence,
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
            answer="\n\n".join(
                answer_parts
            ),
            confidence=confidence,
            tools_used=successful_tools,
            execution_steps=execution_steps,
            status="success",
        )

    def execute_with_replanning(
        self,
        question: str,
        initial_plan: AnalysisPlan,
        df: pd.DataFrame,
    ) -> tuple[
        AnalysisPlan,
        dict[str, Any],
        list[ExecutionStep],
    ]:
        """
        Execute an initial plan and allow one controlled
        re-planning attempt if the results are insufficient.
        """

        current_plan = initial_plan

        all_results: dict[str, Any] = {}

        all_execution_steps: list[
            ExecutionStep
        ] = []

        replan_count = 0

        while True:
            starting_step = (
                len(all_execution_steps) + 1
            )

            results, execution_steps = (
                self.execute_plan(
                    current_plan,
                    df,
                    starting_step=starting_step,
                )
            )

            all_results.update(
                results
            )

            all_execution_steps.extend(
                execution_steps
            )

            evaluation = self.evaluate_results(
                all_results
            )

            if evaluation["sufficient"]:
                return (
                    current_plan,
                    all_results,
                    all_execution_steps,
                )

            if replan_count >= MAX_REPLANS:
                return (
                    current_plan,
                    all_results,
                    all_execution_steps,
                )

            previous_tools = [
                step.tool_name
                for step in all_execution_steps
            ]

            replan_request = ReplanRequest(
                reason=evaluation["reason"],
                previous_tools=previous_tools,
            )

            print(
                "Results were insufficient. "
                "Attempting re-plan."
            )

            current_plan = (
                self.replanner.create_replan(
                    question,
                    replan_request,
                )
            )

            replan_count += 1

            new_tools = [
                tool
                for tool in current_plan.tools
                if tool not in previous_tools
            ]

            if not new_tools:
                print(
                    "Re-planner did not select "
                    "any new tools."
                )

                return (
                    current_plan,
                    all_results,
                    all_execution_steps,
                )

            current_plan = AnalysisPlan(
                objective=current_plan.objective,
                steps=current_plan.steps,
                tools=new_tools,
            )