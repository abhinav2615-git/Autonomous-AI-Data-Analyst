from pathlib import Path
from uuid import uuid4

import pandas as pd

from src.tools.chart_generator import (
    plot_revenue_by_country,
    plot_top_products,
    plot_top_customers_by_revenue,
    plot_units_by_product,
    plot_monthly_revenue,
    plot_yearly_revenue,
    plot_revenue_distribution,
)


CHART_DIRECTORY = Path(
    "data/outputs/charts"
)


CHART_DIRECTORY.mkdir(
    parents=True,
    exist_ok=True,
)


CHART_FUNCTIONS = {
    "revenue_by_country": plot_revenue_by_country,
    "revenue_by_product": plot_top_products,
    "top_products_by_revenue": plot_top_products,
    "top_customers_by_revenue": plot_top_customers_by_revenue,
    "revenue_by_customer": plot_top_customers_by_revenue,
    "units_by_product": plot_units_by_product,
    "revenue_by_month": plot_monthly_revenue,
    "revenue_by_year": plot_yearly_revenue,
    "revenue_distribution": plot_revenue_distribution,
}


def generate_chart_for_tool(
    tool_name: str,
    df: pd.DataFrame,
) -> str | None:
    """
    Generate a chart for a selected analysis tool.

    Returns:
        Relative chart URL if visualization is supported.
        Otherwise returns None.
    """

    chart_function = CHART_FUNCTIONS.get(
        tool_name
    )

    if chart_function is None:
        return None

    chart_filename = (
        f"{uuid4().hex}.png"
    )

    chart_path = (
        CHART_DIRECTORY
        / chart_filename
    )

    chart_function(
        df,
        str(chart_path),
    )

    return (
        f"/charts/{chart_filename}"
    )