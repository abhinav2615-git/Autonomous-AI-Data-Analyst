from pydantic import ValidationError

from src.models.agent import AnalysisPlan


def main() -> None:
    try:
        plan = AnalysisPlan(
            objective="Find highest revenue",
            steps=[
                "Calculate revenue",
                "Group by country",
            ],
            tools=[
                "revenue_by_country",
            ],
        )

        print("VALID PLAN:")
        print(plan)

    except ValidationError as error:
        print("VALIDATION ERROR:")
        print(error)


if __name__ == "__main__":
    main()