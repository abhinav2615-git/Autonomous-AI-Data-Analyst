import pandas as pd


def remove_duplicate_rows(df: pd.DataFrame) -> pd.DataFrame:
    """Remove duplicate rows from the dataset."""
    cleaned_data = df.drop_duplicates()
    return cleaned_data


def handle_missing_values(
    df: pd.DataFrame,
    numerical_strategy: str = "median",
) -> pd.DataFrame:
    """Handle missing values in numerical and categorical columns."""
    cleaned_data = df.copy()

    numerical_columns = cleaned_data.select_dtypes(
        include="number"
    ).columns

    categorical_columns = cleaned_data.select_dtypes(
        include=["object", "category"]
    ).columns

    if numerical_strategy == "median":
        for column in numerical_columns:
            cleaned_data[column] = cleaned_data[column].fillna(
                cleaned_data[column].median()
            )

    elif numerical_strategy == "mean":
        for column in numerical_columns:
            cleaned_data[column] = cleaned_data[column].fillna(
                cleaned_data[column].mean()
            )

    else:
        raise ValueError(
            "Unsupported numerical strategy. "
            "Use 'median' or 'mean'."
        )

    for column in categorical_columns:
        cleaned_data[column] = cleaned_data[column].fillna(
            "Unknown"
        )

    return cleaned_data


def convert_invoice_date(df: pd.DataFrame) -> pd.DataFrame:
    """Convert InvoiceDate to a datetime column."""
    cleaned_data = df.copy()

    if "InvoiceDate" in cleaned_data.columns:
        cleaned_data["InvoiceDate"] = pd.to_datetime(
            cleaned_data["InvoiceDate"],
            errors="coerce",
        )

    return cleaned_data


def remove_invalid_quantities(df: pd.DataFrame) -> pd.DataFrame:
    """Remove rows where Quantity is zero or missing."""
    cleaned_data = df.copy()

    if "Quantity" in cleaned_data.columns:
        cleaned_data = cleaned_data[
            cleaned_data["Quantity"].notna()
        ]
        cleaned_data = cleaned_data[
            cleaned_data["Quantity"] != 0
        ]

    return cleaned_data


def remove_invalid_prices(df: pd.DataFrame) -> pd.DataFrame:
    """Remove rows where UnitPrice is zero or negative."""
    cleaned_data = df.copy()

    if "UnitPrice" in cleaned_data.columns:
        cleaned_data = cleaned_data[
            cleaned_data["UnitPrice"].notna()
        ]
        cleaned_data = cleaned_data[
            cleaned_data["UnitPrice"] > 0
        ]

    return cleaned_data


def clean_online_retail_data(
    df: pd.DataFrame,
    remove_cancellations: bool = False,
) -> pd.DataFrame:
    """Clean the Online Retail dataset."""
    cleaned_data = df.copy()

    cleaned_data = remove_duplicate_rows(cleaned_data)
    cleaned_data = convert_invoice_date(cleaned_data)
    cleaned_data = remove_invalid_quantities(cleaned_data)
    cleaned_data = remove_invalid_prices(cleaned_data)
    cleaned_data = handle_missing_values(cleaned_data)

    if remove_cancellations and "InvoiceNo" in cleaned_data.columns:
        cleaned_data["InvoiceNo"] = (
            cleaned_data["InvoiceNo"].astype(str)
        )
        cleaned_data = cleaned_data[
            ~cleaned_data["InvoiceNo"].str.startswith("C")
        ]

    return cleaned_data


def cleaning_summary(
    original_df: pd.DataFrame,
    cleaned_df: pd.DataFrame,
) -> dict:
    """Generate a summary of changes made during cleaning."""
    original_rows = len(original_df)
    cleaned_rows = len(cleaned_df)

    summary = {
        "original_rows": original_rows,
        "cleaned_rows": cleaned_rows,
        "rows_removed": original_rows - cleaned_rows,
        "original_columns": len(original_df.columns),
        "cleaned_columns": len(cleaned_df.columns),
        "missing_values_after_cleaning": int(
            cleaned_df.isna().sum().sum()
        ),
        "duplicate_rows_after_cleaning": int(
            cleaned_df.duplicated().sum()
        ),
    }

    return summary