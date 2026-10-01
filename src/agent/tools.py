from src.tools.data_analyzer import (
    revenue_by_country,
    revenue_by_product,
    top_products_by_revenue,
    top_customers_by_revenue,
    units_by_product,
    revenue_by_month,
    revenue_by_year,
    cancelled_transactions,
)

from src.tools.data_profiler import profile_data

from src.agent.tool_registry import ToolRegistry


def create_tool_registry() -> ToolRegistry:
    """Create and configure the agent tool registry."""

    registry = ToolRegistry()

    # Dataset profiling
    registry.register(
        "data_profiler",
        profile_data,
    )

    # Revenue analysis
    registry.register(
        "revenue_by_country",
        revenue_by_country,
    )

    registry.register(
        "revenue_by_product",
        revenue_by_product,
    )

    registry.register(
        "top_products_by_revenue",
        top_products_by_revenue,
    )

    registry.register(
        "top_customers_by_revenue",
        top_customers_by_revenue,
    )

    # Quantity analysis
    registry.register(
        "units_by_product",
        units_by_product,
    )

    # Time-based analysis
    registry.register(
        "revenue_by_month",
        revenue_by_month,
    )

    registry.register(
        "revenue_by_year",
        revenue_by_year,
    )

    # Cancellation analysis
    registry.register(
        "cancelled_transactions",
        cancelled_transactions,
    )

    return registry