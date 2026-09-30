from src.config import DATASET_PATH


def main() -> None:
    print("DATASET CONFIGURATION")
    print("=========================")

    print(f"Dataset path:")
    print(DATASET_PATH)

    print("\nDataset exists:")

    if DATASET_PATH.exists():
        print("Yes")
    else:
        print("No")


if __name__ == "__main__":
    main()