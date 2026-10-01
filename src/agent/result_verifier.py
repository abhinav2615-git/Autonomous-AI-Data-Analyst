from typing import Any

import pandas as pd


class ResultVerifier:
    """Validate results produced by analysis tools."""

    def verify(
        self,
        tool_name: str,
        result: Any,
    ) -> dict:
        """
        Verify a tool result and return structured metadata.
        """

        if result is None:
            return {
                "tool_name": tool_name,
                "valid": False,
                "reason": "Tool returned no result.",
            }

        if isinstance(result, dict) and "error" in result:
            return {
                "tool_name": tool_name,
                "valid": False,
                "reason": str(result["error"]),
            }

        if isinstance(result, pd.DataFrame):
            return self._verify_dataframe(
                tool_name,
                result,
            )

        if isinstance(result, (list, tuple)):
            return self._verify_collection(
                tool_name,
                result,
            )

        if isinstance(result, dict):
            return self._verify_dictionary(
                tool_name,
                result,
            )

        return {
            "tool_name": tool_name,
            "valid": True,
            "reason": "Result contains usable data.",
        }

    def _verify_dataframe(
        self,
        tool_name: str,
        result: pd.DataFrame,
    ) -> dict:
        """Verify a DataFrame result."""

        if result.empty:
            return {
                "tool_name": tool_name,
                "valid": False,
                "reason": "Tool returned an empty DataFrame.",
            }

        if len(result.columns) == 0:
            return {
                "tool_name": tool_name,
                "valid": False,
                "reason": "Tool returned no columns.",
            }

        if result.isna().all().all():
            return {
                "tool_name": tool_name,
                "valid": False,
                "reason": "Tool result contains only missing values.",
            }

        return {
            "tool_name": tool_name,
            "valid": True,
            "reason": (
                f"Valid DataFrame with "
                f"{len(result)} rows and "
                f"{len(result.columns)} columns."
            ),
        }

    def _verify_collection(
        self,
        tool_name: str,
        result: list | tuple,
    ) -> dict:
        """Verify list or tuple results."""

        if len(result) == 0:
            return {
                "tool_name": tool_name,
                "valid": False,
                "reason": "Tool returned an empty collection.",
            }

        return {
            "tool_name": tool_name,
            "valid": True,
            "reason": (
                f"Valid collection containing "
                f"{len(result)} items."
            ),
        }

    def _verify_dictionary(
        self,
        tool_name: str,
        result: dict,
    ) -> dict:
        """Verify dictionary results."""

        if len(result) == 0:
            return {
                "tool_name": tool_name,
                "valid": False,
                "reason": "Tool returned an empty dictionary.",
            }

        return {
            "tool_name": tool_name,
            "valid": True,
            "reason": (
                f"Valid dictionary containing "
                f"{len(result)} fields."
            ),
        }