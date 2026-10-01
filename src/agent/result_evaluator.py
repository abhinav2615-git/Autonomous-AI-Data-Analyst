from typing import Any

import pandas as pd


class ResultEvaluator:
    """Evaluate whether analysis results are sufficient."""

    def evaluate(
        self,
        results: dict[str, Any],
    ) -> dict[str, Any]:
        """
        Evaluate the current analysis results.

        Returns structured information describing
        whether usable results are available.
        """

        if not results:
            return {
                "sufficient": False,
                "reason": "No analysis results were produced.",
            }

        valid_results = 0
        invalid_results = 0

        for result in results.values():

            if (
                isinstance(result, dict)
                and "error" in result
            ):
                invalid_results += 1
                continue

            if isinstance(result, pd.DataFrame):
                if result.empty:
                    invalid_results += 1
                else:
                    valid_results += 1
                continue

            if result is None:
                invalid_results += 1
                continue

            valid_results += 1

        if valid_results == 0:
            return {
                "sufficient": False,
                "reason": (
                    "No valid analysis results "
                    "are available."
                ),
            }

        return {
            "sufficient": True,
            "reason": (
                f"{valid_results} valid analysis result(s) "
                f"are available."
            ),
            "valid_results": valid_results,
            "invalid_results": invalid_results,
        }