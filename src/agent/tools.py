from src.tools.data_analyzer import (
    revenue_by_country,
    revenue_by_product,
    top_products_by_revenue,
    top_customers_by_revenue,
    revenue_by_month,
    revenue_by_year,
)

from src.agent.tool_registry import ToolRegistry


def create_tool_registry() -> ToolRegistry:
    """Create and configure the agent tool registry."""

    registry = ToolRegistry()

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

    registry.register(
        "revenue_by_month",
        revenue_by_month,
    )

    registry.register(
        "revenue_by_year",
        revenue_by_year,
    )

    return registry