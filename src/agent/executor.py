from typing import Any

import pandas as pd

from src.agent.replanner import Replanner
from src.agent.result_evaluator import ResultEvaluator
from src.agent.result_interpreter import interpret_result
from src.agent.result_verifier import ResultVerifier
from src.agent.tool_registry import ToolRegistry
from src.agent.tool_requirements import (
    validate_tool_requirements,
)
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
        step_number: int,
    ) -> tuple[Any, ExecutionStep]:
        """
        Validate and execute one analysis tool.

        Schema requirements are checked before
        the actual tool is executed.
        """

        print(
            f"Executing step {step_number}: "
            f"{tool_name}"
        )

        # --------------------------------------------------
        # 1. Validate that the tool exists.
        # --------------------------------------------------

        try:
            tool = self.registry.get(
                tool_name
            )

        except KeyError as error:

            print(
                f"Step {step_number} failed: "
                f"{tool_name} -> {error}"
            )

            execution_step = ExecutionStep(
                step_number=step_number,
                tool_name=tool_name,
                success=False,
                error=str(error),
            )

            return None, execution_step

        # --------------------------------------------------
        # 2. Validate dataset schema BEFORE execution.
        # --------------------------------------------------

        try:

            requirement_check = (
                validate_tool_requirements(
                    tool_name=tool_name,
                    available_columns=(
                        df.columns.tolist()
                    ),
                )
            )

        except KeyError:

            # If a tool has no explicit requirement
            # definition yet, allow execution.
            requirement_check = {
                "valid": True,
                "tool_name": tool_name,
                "required_columns": [],
                "missing_columns": [],
                "reason": (
                    "No explicit schema requirements "
                    "are defined for this tool."
                ),
            }

        if not requirement_check["valid"]:

            error_message = (
                "Schema validation failed. "
                f"Missing columns: "
                f"{requirement_check['missing_columns']}"
            )

            print(
                f"Step {step_number} failed: "
                f"{tool_name} -> "
                f"{error_message}"
            )

            execution_step = ExecutionStep(
                step_number=step_number,
                tool_name=tool_name,
                success=False,
                error=error_message,
            )

            return None, execution_step

        # --------------------------------------------------
        # 3. Execute the tool.
        # --------------------------------------------------

        try:

            result = tool(df)

        except Exception as error:

            print(
                f"Step {step_number} failed: "
                f"{tool_name} -> {error}"
            )

            execution_step = ExecutionStep(
                step_number=step_number,
                tool_name=tool_name,
                success=False,
                error=str(error),
            )

            return None, execution_step

        # --------------------------------------------------
        # 4. Verify the tool result.
        # --------------------------------------------------

        verification = self.verifier.verify(
            tool_name,
            result,
        )

        if not verification["valid"]:

            print(
                f"Verification failed: "
                f"{tool_name} -> "
                f"{verification['reason']}"
            )

            execution_step = ExecutionStep(
                step_number=step_number,
                tool_name=tool_name,
                success=False,
                error=verification["reason"],
            )

            return result, execution_step

        print(
            f"Verification passed: "
            f"{tool_name}"
        )

        execution_step = ExecutionStep(
            step_number=step_number,
            tool_name=tool_name,
            success=True,
            error=None,
        )

        return result, execution_step

    def execute_plan(
        self,
        plan: AnalysisPlan,
        df: pd.DataFrame,
        starting_step: int = 1,
    ) -> tuple[
        dict[str, Any],
        list[ExecutionStep],
    ]:
        """Execute every tool in an analysis plan."""

        results: dict[str, Any] = {}

        execution_steps: list[
            ExecutionStep
        ] = []

        for index, tool_name in enumerate(
            plan.tools,
            start=starting_step,
        ):

            result, execution_step = (
                self.execute_step(
                    tool_name=tool_name,
                    df=df,
                    step_number=index,
                )
            )

            results[tool_name] = result

            execution_steps.append(
                execution_step
            )

        return (
            results,
            execution_steps,
        )

    def evaluate_results(
        self,
        results: dict[str, Any],
    ) -> dict[str, Any]:
        """Evaluate whether analysis results are sufficient."""

        return self.evaluator.evaluate(
            results
        )

    def interpret_results(
        self,
        results: dict[str, Any],
    ) -> list[str]:
        """Convert successful results into human-readable insights."""

        interpretations = []

        for tool_name, result in results.items():

            if result is None:
                continue

            if (
                isinstance(result, dict)
                and "error" in result
            ):
                continue

            try:

                interpretation = interpret_result(
                    tool_name,
                    result,
                )

                interpretations.append(
                    interpretation
                )

            except Exception as error:

                interpretations.append(
                    (
                        f"{tool_name} completed, "
                        f"but its result could not "
                        f"be interpreted: {error}"
                    )
                )

        return interpretations

    def calculate_confidence(
        self,
        execution_steps: list[ExecutionStep],
    ) -> float:
        """
        Calculate confidence from execution success.

        Successful execution steps contribute
        positively to confidence.
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
            successful_steps
            / total_steps,
            2,
        )

    def create_response(
        self,
        plan: AnalysisPlan,
        results: dict[str, Any],
        execution_steps: list[ExecutionStep],
    ) -> AgentResponse:
        """Create the final agent response."""

        interpretations = (
            self.interpret_results(
                results
            )
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

        confidence = (
            self.calculate_confidence(
                execution_steps
            )
        )

        if interpretations:

            answer = "\n\n".join(
                interpretations
            )

        elif failed_tools:

            answer = (
                "The requested analysis "
                "could not be completed."
            )

        else:

            answer = (
                "No usable analysis results "
                "were produced."
            )

        if failed_tools:

            failed_summary = (
                "\n\nThe following analysis steps "
                "could not be verified or completed: "
                + ", ".join(
                    failed_tools
                )
                + "."
            )

            answer += failed_summary

        if not successful_tools:

            status = "failed"

        elif failed_tools:

            status = "success"

        else:

            status = "success"

        return AgentResponse(
            answer=answer,
            confidence=confidence,
            tools_used=successful_tools,
            execution_steps=execution_steps,
            status=status,
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
        Execute a plan and re-plan when results
        are insufficient.

        Re-planning is limited to MAX_REPLANS.
        """

        current_plan = initial_plan

        all_results: dict[
            str,
            Any,
        ] = {}

        all_execution_steps: list[
            ExecutionStep
        ] = []

        replan_count = 0

        while True:

            starting_step = (
                len(all_execution_steps)
                + 1
            )

            results, execution_steps = (
                self.execute_plan(
                    plan=current_plan,
                    df=df,
                    starting_step=starting_step,
                )
            )

            all_results.update(
                results
            )

            all_execution_steps.extend(
                execution_steps
            )

            evaluation = (
                self.evaluate_results(
                    all_results
                )
            )

            if evaluation["sufficient"]:

                return (
                    current_plan,
                    all_results,
                    all_execution_steps,
                )

            if (
                replan_count
                >= MAX_REPLANS
            ):

                print(
                    "Maximum re-plan limit reached."
                )

                return (
                    current_plan,
                    all_results,
                    all_execution_steps,
                )

            print(
                "Results were insufficient. "
                "Attempting re-plan."
            )

            previous_tools = [
                step.tool_name
                for step in all_execution_steps
            ]

            request = ReplanRequest(
                reason=evaluation[
                    "reason"
                ],
                previous_tools=(
                    previous_tools
                ),
            )

            try:

                new_plan = (
                    self.replanner.create_replan(
                        question=question,
                        request=request,
                    )
                )

            except Exception as error:

                print(
                    "Re-planning failed: "
                    f"{error}"
                )

                return (
                    current_plan,
                    all_results,
                    all_execution_steps,
                )

            new_tools = [
                tool
                for tool in new_plan.tools
                if tool
                not in previous_tools
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
                objective=new_plan.objective,
                steps=new_plan.steps,
                tools=new_tools,
            )

            replan_count += 1

            print(
                f"Re-plan {replan_count} "
                "created."
            )