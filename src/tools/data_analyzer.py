import pandas as pd

def calculate_revenue(df: pd.DataFrame) -> pd.Series:
    """Calculate revenue for each transaction.
    Revenue = Quantity * UnitPrice"""
    revenue = df["Quantity"] * df["UnitPrice"]
    return revenue


def calculate_total_revenue(df: pd.DataFrame) -> float:
    """Calculate total revenue across all transactions."""
    revenue = calculate_revenue(df)
    total_revenue = revenue.sum()
    return float(total_revenue)


def calculate_total_units(df: pd.DataFrame) -> int:
    """Calculate the total number of units sold."""
    total_units = df["Quantity"].sum()
    return int(total_units)


def calculate_average_transaction_value(df: pd.DataFrame) -> float:
    """Calculate the average transaction value."""
    revenue = calculate_revenue(df)
    average_value = revenue.mean()
    return float(average_value)


def count_unique_products(df: pd.DataFrame) -> int:
    """Count the number of unique products."""
    unique_products = df["StockCode"].nunique()
    return int(unique_products)


def count_unique_customers(df: pd.DataFrame) -> int:
    """Count the number of unique customers."""
    unique_customers = df["CustomerID"].nunique()
    return int(unique_customers)


def count_unique_countries(df: pd.DataFrame) -> int:
    """Count the number of unique countries."""
    unique_countries = df["Country"].nunique()
    return int(unique_countries)


def revenue_by_country(df: pd.DataFrame) -> pd.DataFrame:
    """Calculate total revenue for each country."""
    data = df.copy()
    data["Revenue"] = calculate_revenue(data)
    result = (
        data.groupby("Country")["Revenue"]
        .sum()
        .sort_values(ascending=False)
        .reset_index()
    )
    return result


def units_by_product(df: pd.DataFrame) -> pd.DataFrame:
    """Calculate total units sold for each product."""
    result = (
        df.groupby("StockCode")["Quantity"]
        .sum()
        .sort_values(ascending=False)
        .reset_index()
    )
    return result


def revenue_by_product(df: pd.DataFrame) -> pd.DataFrame:
    """Calculate total revenue for each product."""
    data = df.copy()
    data["Revenue"] = calculate_revenue(data)
    result = (
        data.groupby("StockCode")["Revenue"]
        .sum()
        .sort_values(ascending=False)
        .reset_index()
    )
    return result


def revenue_by_customer(df: pd.DataFrame) -> pd.DataFrame:
    """Calculate total revenue for each customer."""
    data = df.copy()
    data["Revenue"] = calculate_revenue(data)
    result = (
        data.groupby("CustomerID")["Revenue"]
        .sum()
        .sort_values(ascending=False)
        .reset_index()
    )
    return result


def revenue_by_country_top(df: pd.DataFrame, n: int = 10) -> pd.DataFrame:
    """Return the top N countries by revenue."""
    result = revenue_by_country(df)
    return result.head(n)


def top_products_by_units(df: pd.DataFrame, n: int = 10) -> pd.DataFrame:
    """Return the top N products by units sold."""
    result = units_by_product(df)
    return result.head(n)


def top_products_by_revenue(df: pd.DataFrame, n: int = 10) -> pd.DataFrame:
    """Return the top N products by revenue."""
    result = revenue_by_product(df)
    return result.head(n)


def top_customers_by_revenue(df: pd.DataFrame, n: int = 10) -> pd.DataFrame:
    """Return the top N customers by revenue."""
    result = revenue_by_customer(df)
    return result.head(n)


def revenue_by_month(df: pd.DataFrame) -> pd.DataFrame:
    """Calculate total revenue for each month."""
    data = df.copy()
    data["InvoiceDate"] = pd.to_datetime(data["InvoiceDate"])
    data["Revenue"] = calculate_revenue(data)
    data["Month"] = data["InvoiceDate"].dt.to_period("M")
    result = (
        data.groupby("Month")["Revenue"]
        .sum()
        .reset_index()
    )
    result["Month"] = result["Month"].astype(str)
    return result


def revenue_by_year(df: pd.DataFrame) -> pd.DataFrame:
    """Calculate total revenue for each year."""
    data = df.copy()
    data["InvoiceDate"] = pd.to_datetime(data["InvoiceDate"])
    data["Revenue"] = calculate_revenue(data)
    data["Year"] = data["InvoiceDate"].dt.year
    result = (
        data.groupby("Year")["Revenue"]
        .sum()
        .reset_index()
    )
    return result


def cancelled_transactions(df: pd.DataFrame) -> pd.DataFrame:
    """Return transactions whose invoice numbers start with C."""
    data = df.copy()
    data["InvoiceNo"] = data["InvoiceNo"].astype(str)
    result = data[
        data["InvoiceNo"].str.startswith("C")
    ]
    return result


def count_cancelled_transactions(df: pd.DataFrame) -> int:
    """Count cancelled transactions."""
    cancellations = cancelled_transactions(df)
    return len(cancellations)


def analysis_summary(df: pd.DataFrame) -> dict:
    """Generate a high-level summary of the dataset."""
    summary = {
        "total_rows": len(df),
        "total_columns": len(df.columns),
        "total_revenue": calculate_total_revenue(df),
        "total_units": calculate_total_units(df),
        "average_transaction_value": calculate_average_transaction_value(df),
        "unique_products": count_unique_products(df),
        "unique_customers": count_unique_customers(df),
        "unique_countries": count_unique_countries(df),
        "cancelled_transactions": count_cancelled_transactions(df),
    }
    return summary