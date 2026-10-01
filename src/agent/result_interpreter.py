import pandas as pd


def interpret_result(
    tool_name: str,
    result: object,
) -> str:
    """Convert a tool result into a human-readable insight."""

    if not isinstance(result, pd.DataFrame):
        return (
            f"The {tool_name} analysis completed successfully."
        )

    if result.empty:
        return "The analysis returned no results."

    if tool_name == "revenue_by_country":
        return _interpret_revenue_by_country(result)

    if tool_name == "revenue_by_product":
        return _interpret_revenue_by_product(result)

    if tool_name == "top_products_by_revenue":
        return _interpret_top_products(result)

    if tool_name == "top_customers_by_revenue":
        return _interpret_top_customers(result)

    if tool_name == "revenue_by_month":
        return _interpret_revenue_by_month(result)

    if tool_name == "revenue_by_year":
        return _interpret_revenue_by_year(result)

    return (
        f"The {tool_name} analysis completed successfully."
    )


def _interpret_revenue_by_country(
    result: pd.DataFrame,
) -> str:
    """Interpret revenue grouped by country."""

    first_row = result.iloc[0]

    country = first_row["Country"]
    revenue = first_row["Revenue"]

    return (
        f"{country} generated the highest revenue, "
        f"with total revenue of {revenue:,.2f}."
    )


def _interpret_revenue_by_product(
    result: pd.DataFrame,
) -> str:
    """Interpret revenue grouped by product."""

    first_row = result.iloc[0]

    product = first_row["StockCode"]
    revenue = first_row["Revenue"]

    return (
        f"Product {product} generated the highest revenue, "
        f"with total revenue of {revenue:,.2f}."
    )


def _interpret_top_products(
    result: pd.DataFrame,
) -> str:
    """Interpret top products by revenue."""

    first_row = result.iloc[0]

    product = first_row["StockCode"]
    revenue = first_row["Revenue"]

    return (
        f"Product {product} is the top product by revenue, "
        f"generating {revenue:,.2f}."
    )


def _interpret_top_customers(
    result: pd.DataFrame,
) -> str:
    """Interpret top customers by revenue."""

    first_row = result.iloc[0]

    customer = first_row["CustomerID"]
    revenue = first_row["Revenue"]

    return (
        f"Customer {customer} generated the highest revenue, "
        f"with total revenue of {revenue:,.2f}."
    )


def _interpret_revenue_by_month(
    result: pd.DataFrame,
) -> str:
    """Interpret monthly revenue results."""

    if "Month" not in result.columns:
        return (
            "Monthly revenue analysis completed, "
            "but the expected Month column was not found."
        )

    if "Revenue" not in result.columns:
        return (
            "Monthly revenue analysis completed, "
            "but the expected Revenue column was not found."
        )

    total_revenue = result["Revenue"].sum()

    highest_row = result.loc[
        result["Revenue"].idxmax()
    ]

    lowest_row = result.loc[
        result["Revenue"].idxmin()
    ]

    highest_month = highest_row["Month"]
    highest_revenue = highest_row["Revenue"]

    lowest_month = lowest_row["Month"]
    lowest_revenue = lowest_row["Revenue"]

    return (
        f"Monthly revenue was analyzed across "
        f"{len(result)} months. "
        f"Total reported revenue was "
        f"{total_revenue:,.2f}. "
        f"The highest-revenue month was "
        f"{highest_month}, generating "
        f"{highest_revenue:,.2f}. "
        f"The lowest-revenue month was "
        f"{lowest_month}, generating "
        f"{lowest_revenue:,.2f}."
    )


def _interpret_revenue_by_year(
    result: pd.DataFrame,
) -> str:
    """Interpret yearly revenue results."""

    if "Year" not in result.columns:
        return (
            "Yearly revenue analysis completed, "
            "but the expected Year column was not found."
        )

    if "Revenue" not in result.columns:
        return (
            "Yearly revenue analysis completed, "
            "but the expected Revenue column was not found."
        )

    total_revenue = result["Revenue"].sum()

    highest_row = result.loc[
        result["Revenue"].idxmax()
    ]

    lowest_row = result.loc[
        result["Revenue"].idxmin()
    ]

    highest_year = highest_row["Year"]
    highest_revenue = highest_row["Revenue"]

    lowest_year = lowest_row["Year"]
    lowest_revenue = lowest_row["Revenue"]

    return (
        f"Yearly revenue was analyzed across "
        f"{len(result)} years. "
        f"Total reported revenue was "
        f"{total_revenue:,.2f}. "
        f"The highest-revenue year was "
        f"{highest_year}, generating "
        f"{highest_revenue:,.2f}. "
        f"The lowest-revenue year was "
        f"{lowest_year}, generating "
        f"{lowest_revenue:,.2f}."
    )