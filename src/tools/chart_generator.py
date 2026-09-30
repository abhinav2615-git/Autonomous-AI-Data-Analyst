from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

from src.tools.data_analyzer import (
    revenue_by_country_top,
    top_products_by_revenue,
    revenue_by_month,
)


def save_chart(fig, output_path: str) -> str:
    """Save a chart to the specified output path."""
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    fig.tight_layout()
    fig.savefig(path, dpi=150, bbox_inches="tight")
    plt.close(fig)
    return str(path)


def plot_revenue_by_country(
    df: pd.DataFrame,
    output_path: str,
    n: int = 10,
) -> str:
    """Create a bar chart of revenue by country."""
    data = revenue_by_country_top(df, n)
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.bar(
        data["Country"],
        data["Revenue"],
    )
    ax.set_title("Top Countries by Revenue")
    ax.set_xlabel("Country")
    ax.set_ylabel("Revenue")
    plt.xticks(rotation=45, ha="right")
    return save_chart(fig, output_path)


def plot_top_products(
    df: pd.DataFrame,
    output_path: str,
    n: int = 10,
) -> str:
    """Create a bar chart of top products by revenue."""
    data = top_products_by_revenue(df, n)
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.bar(
        data["StockCode"].astype(str),
        data["Revenue"],
    )
    ax.set_title("Top Products by Revenue")
    ax.set_xlabel("Product")
    ax.set_ylabel("Revenue")
    plt.xticks(rotation=45, ha="right")
    return save_chart(fig, output_path)


def plot_monthly_revenue(
    df: pd.DataFrame,
    output_path: str,
) -> str:
    """Create a line chart of monthly revenue."""
    data = revenue_by_month(df)
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(
        data["Month"],
        data["Revenue"],
        marker="o",
    )
    ax.set_title("Monthly Revenue")
    ax.set_xlabel("Month")
    ax.set_ylabel("Revenue")
    plt.xticks(rotation=45, ha="right")
    return save_chart(fig, output_path)


def plot_revenue_distribution(
    df: pd.DataFrame,
    output_path: str,
) -> str:
    """Create a histogram of transaction revenue."""
    revenue = df["Quantity"] * df["UnitPrice"]
    lower_limit = revenue.quantile(0.01)
    upper_limit = revenue.quantile(0.99)
    filtered_revenue = revenue[
        (revenue >= lower_limit)
        & (revenue <= upper_limit)
    ]

    fig, ax = plt.subplots(figsize=(10, 6))
    ax.hist(
        filtered_revenue,
        bins=50,
    )
    ax.set_title("Transaction Revenue Distribution")
    ax.set_xlabel("Transaction Revenue")
    ax.set_ylabel("Number of Transactions")
    return save_chart(fig, output_path)