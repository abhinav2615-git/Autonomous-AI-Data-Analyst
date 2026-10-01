from typing import Any

import pandas as pd


def _detect_datetime_columns(
    df: pd.DataFrame,
) -> list[str]:
    """Detect columns that contain date/time values."""

    datetime_columns = []

    for column in df.columns:

        if pd.api.types.is_datetime64_any_dtype(
            df[column]
        ):
            datetime_columns.append(column)
            continue

        if df[column].dtype == "object":

            sample = df[column].dropna()

            if sample.empty:
                continue

            converted = pd.to_datetime(
                sample,
                errors="coerce",
            )

            valid_ratio = (
                converted.notna().mean()
            )

            if valid_ratio >= 0.8:
                datetime_columns.append(
                    column
                )

    return datetime_columns


def _detect_column_roles(
    df: pd.DataFrame,
    datetime_columns: list[str],
) -> dict[str, str]:
    """Detect likely semantic roles for columns."""

    roles: dict[str, str] = {}

    datetime_set = set(
        datetime_columns
    )

    for column in df.columns:

        column_lower = (
            str(column).lower()
        )

        # ----------------------------------------------
        # Date / time
        # ----------------------------------------------

        if column in datetime_set:

            roles[column] = "datetime"
            continue

        # ----------------------------------------------
        # Quantity
        # ----------------------------------------------

        if any(
            keyword in column_lower
            for keyword in [
                "quantity",
                "qty",
                "units",
                "unit_sold",
                "items",
                "count",
            ]
        ):

            roles[column] = "quantity"
            continue

        # ----------------------------------------------
        # Price / monetary value
        # ----------------------------------------------

        if any(
            keyword in column_lower
            for keyword in [
                "price",
                "cost",
                "amount",
                "revenue",
                "sales",
                "value",
                "profit",
            ]
        ):

            roles[column] = "numeric_measure"
            continue

        # ----------------------------------------------
        # Country
        # ----------------------------------------------

        if any(
            keyword in column_lower
            for keyword in [
                "country",
                "nation",
            ]
        ):

            roles[column] = "country"
            continue

        # ----------------------------------------------
        # Customer
        # ----------------------------------------------

        if any(
            keyword in column_lower
            for keyword in [
                "customer",
                "client",
                "buyer",
            ]
        ):

            roles[column] = "customer"
            continue

        # ----------------------------------------------
        # Product
        # ----------------------------------------------

        if any(
            keyword in column_lower
            for keyword in [
                "product",
                "item",
                "sku",
                "stockcode",
            ]
        ):

            roles[column] = "product"
            continue

        # ----------------------------------------------
        # Identifier
        # ----------------------------------------------

        if any(
            keyword in column_lower
            for keyword in [
                "id",
                "code",
                "number",
                "no",
            ]
        ):

            roles[column] = "identifier"
            continue

        # ----------------------------------------------
        # Generic numeric column
        # ----------------------------------------------

        if pd.api.types.is_numeric_dtype(
            df[column]
        ):

            roles[column] = "numeric"

        # ----------------------------------------------
        # Generic categorical column
        # ----------------------------------------------

        elif (
            df[column].dtype == "object"
            or str(
                df[column].dtype
            ) == "category"
        ):

            roles[column] = "categorical"

        else:

            roles[column] = "unknown"

    return roles


def analyze_schema(
    df: pd.DataFrame,
) -> dict[str, Any]:
    """
    Analyze the structural and semantic schema
    of a dataset.
    """

    columns = df.columns.tolist()

    data_types = {
        column: str(dtype)
        for column, dtype in df.dtypes.items()
    }

    numerical_columns = (
        df.select_dtypes(
            include="number"
        )
        .columns
        .tolist()
    )

    categorical_columns = (
        df.select_dtypes(
            include=[
                "object",
                "category",
            ]
        )
        .columns
        .tolist()
    )

    datetime_columns = (
        _detect_datetime_columns(df)
    )

    missing_values = {
        column: int(value)
        for column, value in (
            df.isna().sum().items()
        )
        if value > 0
    }

    unique_values = {
        column: int(
            df[column].nunique(
                dropna=True
            )
        )
        for column in columns
    }

    column_roles = _detect_column_roles(
        df=df,
        datetime_columns=datetime_columns,
    )

    return {
        "rows": len(df),
        "columns": len(columns),
        "column_names": columns,
        "data_types": data_types,
        "numerical_columns": numerical_columns,
        "categorical_columns": categorical_columns,
        "datetime_columns": datetime_columns,
        "column_roles": column_roles,
        "missing_values": missing_values,
        "unique_values": unique_values,
    }