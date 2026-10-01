from dataclasses import dataclass


@dataclass(frozen=True)
class ToolRequirement:
    """Describe the dataset columns required by a tool."""

    required_columns: tuple[str, ...]


TOOL_REQUIREMENTS = {
    "data_profiler": ToolRequirement(
        required_columns=(),
    ),
    "schema_analyzer": ToolRequirement(
        required_columns=(),
    ),
    "revenue_by_country": ToolRequirement(
        required_columns=(
            "Country",
            "Quantity",
            "UnitPrice",
        ),
    ),
    "revenue_by_product": ToolRequirement(
        required_columns=(
            "StockCode",
            "Quantity",
            "UnitPrice",
        ),
    ),
    "revenue_by_customer": ToolRequirement(
        required_columns=(
            "CustomerID",
            "Quantity",
            "UnitPrice",
        ),
    ),
    "top_products_by_revenue": ToolRequirement(
        required_columns=(
            "StockCode",
            "Quantity",
            "UnitPrice",
        ),
    ),
    "top_customers_by_revenue": ToolRequirement(
        required_columns=(
            "CustomerID",
            "Quantity",
            "UnitPrice",
        ),
    ),
    "units_by_product": ToolRequirement(
        required_columns=(
            "StockCode",
            "Quantity",
        ),
    ),
    "revenue_by_month": ToolRequirement(
        required_columns=(
            "InvoiceDate",
            "Quantity",
            "UnitPrice",
        ),
    ),
    "revenue_by_year": ToolRequirement(
        required_columns=(
            "InvoiceDate",
            "Quantity",
            "UnitPrice",
        ),
    ),
    "cancelled_transactions": ToolRequirement(
        required_columns=(
            "InvoiceNo",
        ),
    ),
}


def get_tool_requirements(
    tool_name: str,
) -> ToolRequirement:
    """Return the requirements for a registered tool."""

    if tool_name not in TOOL_REQUIREMENTS:
        raise KeyError(
            f"No requirements defined for tool: {tool_name}"
        )

    return TOOL_REQUIREMENTS[tool_name]


def validate_tool_requirements(
    tool_name: str,
    available_columns: list[str],
) -> dict:
    """
    Check whether a tool can operate on the dataset.
    """

    requirements = get_tool_requirements(
        tool_name
    )

    available = set(
        available_columns
    )

    missing_columns = [
        column
        for column in requirements.required_columns
        if column not in available
    ]

    if missing_columns:
        return {
            "valid": False,
            "tool_name": tool_name,
            "required_columns": list(
                requirements.required_columns
            ),
            "missing_columns": missing_columns,
            "reason": (
                "Required dataset columns are missing: "
                f"{missing_columns}"
            ),
        }

    return {
        "valid": True,
        "tool_name": tool_name,
        "required_columns": list(
            requirements.required_columns
        ),
        "missing_columns": [],
        "reason": (
            "All required dataset columns "
            "are available."
        ),
    }