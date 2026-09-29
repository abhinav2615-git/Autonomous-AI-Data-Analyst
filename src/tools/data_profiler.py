import pandas as pd


def profile_data(df: pd.DataFrame) -> dict:
    """Generate a basic profile of a Pandas DataFrame."""

    profile = {
        "rows": len(df),
        "columns": len(df.columns),
        "column_names": df.columns.tolist(),
        "data_types": {
            column: str(dtype)
            for column, dtype in df.dtypes.items()
        },
        "missing_values": {
            column: int(value)
            for column, value in df.isna().sum().items()
            if value > 0
        },
        "unique_values": {
            column: int(df[column].nunique())
            for column in df.columns
        },
    }

    numerical_columns = df.select_dtypes(
        include="number"
    ).columns.tolist()

    if numerical_columns:
        profile["numerical_summary"] = (
            df[numerical_columns]
            .describe()
            .round(2)
            .to_dict()
        )
    else:
        profile["numerical_summary"] = {}

    return profile
