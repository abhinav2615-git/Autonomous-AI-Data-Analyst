import pandas as pd


def add_revenue(df: pd.DataFrame) -> pd.DataFrame:
    """Add Revenue column using Quantity × UnitPrice."""

    data = df.copy()

    data["Revenue"] = (
        data["Quantity"] * data["UnitPrice"]
    )

    return data


def add_date_features(df: pd.DataFrame) -> pd.DataFrame:
    """Add useful date and time based features."""

    data = df.copy()

    data["InvoiceDate"] = pd.to_datetime(
        data["InvoiceDate"],
        errors="coerce",
    )

    data["Year"] = data["InvoiceDate"].dt.year
    data["Month"] = data["InvoiceDate"].dt.month
    data["Quarter"] = data["InvoiceDate"].dt.quarter
    data["DayOfWeek"] = data["InvoiceDate"].dt.day_name()
    data["Hour"] = data["InvoiceDate"].dt.hour

    data["InvoiceYearMonth"] = (
        data["InvoiceDate"].dt.to_period("M").astype(str)
    )

    return data


def add_cancellation_features(df: pd.DataFrame) -> pd.DataFrame:
    """Add cancellation and transaction-type features."""

    data = df.copy()

    data["InvoiceNo"] = data["InvoiceNo"].astype(str)

    data["IsCancelled"] = (
        data["InvoiceNo"].str.startswith("C")
    )

    data["TransactionType"] = data["IsCancelled"].map(
        {
            True: "Cancellation",
            False: "Sale",
        }
    )

    return data


def add_price_band(df: pd.DataFrame) -> pd.DataFrame:
    """Create categories for unit prices."""

    data = df.copy()

    data["UnitPriceBand"] = pd.cut(
        data["UnitPrice"],
        bins=[
            -float("inf"),
            1,
            5,
            10,
            50,
            float("inf"),
        ],
        labels=[
            "Very Low",
            "Low",
            "Medium",
            "High",
            "Very High",
        ],
    )

    return data


def add_quantity_band(df: pd.DataFrame) -> pd.DataFrame:
    """Create categories for transaction quantities."""

    data = df.copy()

    data["QuantityBand"] = pd.cut(
        data["Quantity"],
        bins=[
            -float("inf"),
            1,
            5,
            10,
            50,
            float("inf"),
        ],
        labels=[
            "Very Low",
            "Low",
            "Medium",
            "High",
            "Very High",
        ],
    )

    return data


def engineer_features(df: pd.DataFrame) -> pd.DataFrame:
    """Apply all feature-engineering operations."""

    required_columns = [
        "InvoiceNo",
        "Quantity",
        "InvoiceDate",
        "UnitPrice",
    ]

    missing_columns = [
        column
        for column in required_columns
        if column not in df.columns
    ]

    if missing_columns:
        raise ValueError(
            f"Missing required columns: {missing_columns}"
        )

    data = df.copy()

    data = add_revenue(data)
    data = add_date_features(data)
    data = add_cancellation_features(data)
    data = add_price_band(data)
    data = add_quantity_band(data)

    return data