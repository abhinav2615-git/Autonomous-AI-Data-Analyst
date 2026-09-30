from pathlib import Path

from src.tools.data_loader import load_data
from src.tools.data_cleaner import clean_online_retail_data
from src.tools.feature_engineering import engineer_features


INPUT_FILE = "data/datasets/Online Retail.xlsx"
OUTPUT_FILE = "data/datasets/processed_retail.csv"


def main() -> None:
    print("Loading dataset...")

    df = load_data(INPUT_FILE)

    print(f"Original rows: {len(df)}")
    print(f"Original columns: {len(df.columns)}")

    print("\nCleaning dataset...")

    cleaned_df = clean_online_retail_data(
        df,
        remove_cancellations=False,
    )

    print(f"Rows after cleaning: {len(cleaned_df)}")

    print("\nEngineering features...")

    processed_df = engineer_features(cleaned_df)

    output_path = Path(OUTPUT_FILE)
    output_path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    processed_df.to_csv(
        output_path,
        index=False,
    )

    print("\nFeature engineering complete.")
    print(f"Processed rows: {len(processed_df)}")
    print(f"Processed columns: {len(processed_df.columns)}")
    print(f"Saved to: {OUTPUT_FILE}")

    print("\nNew columns:")

    original_columns = set(df.columns)

    new_columns = [
        column
        for column in processed_df.columns
        if column not in original_columns
    ]

    for column in new_columns:
        print(f"- {column}")


if __name__ == "__main__":
    main()