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

    first_row = result.iloc[0]

    if tool_name == "revenue_by_country":
        country = first_row["Country"]
        revenue = first_row["Revenue"]

        return (
            f"{country} generated the highest revenue, "
            f"with total revenue of {revenue:,.2f}."
        )

    if tool_name == "revenue_by_product":
        product = first_row["StockCode"]
        revenue = first_row["Revenue"]

        return (
            f"Product {product} generated the highest revenue, "
            f"with total revenue of {revenue:,.2f}."
        )

    if tool_name == "top_products_by_revenue":
        product = first_row["StockCode"]
        revenue = first_row["Revenue"]

        return (
            f"Product {product} is the top product by revenue, "
            f"generating {revenue:,.2f}."
        )

    if tool_name == "top_customers_by_revenue":
        customer = first_row["CustomerID"]
        revenue = first_row["Revenue"]

        return (
            f"Customer {customer} generated the highest revenue, "
            f"with total revenue of {revenue:,.2f}."
        )

    if tool_name == "revenue_by_month":
        month = first_row["Month"]
        revenue = first_row["Revenue"]

        return (
            f"The first reported month, {month}, "
            f"generated revenue of {revenue:,.2f}."
        )

    if tool_name == "revenue_by_year":
        year = first_row["Year"]
        revenue = first_row["Revenue"]

        return (
            f"The year {year} generated revenue of "
            f"{revenue:,.2f}."
        )

    return (
        f"The {tool_name} analysis completed successfully."
    )