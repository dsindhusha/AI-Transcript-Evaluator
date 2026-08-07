import json
from pathlib import Path

from app.services.scoring_service import ScoringService


def main():
    """
    Recalculates and updates the evaluation scores
    for all report files in the dataset.
    """

    reports_folder = Path("dataset/reports")

    scoring_service = ScoringService()

    report_files = sorted(
        reports_folder.glob("*.json")
    )

    print(f"Found {len(report_files)} reports.\n")

    for report_file in report_files:

        print(f"Processing {report_file.name}...")

        with open(report_file, "r", encoding="utf-8") as file:

            report = json.load(file)

        score = scoring_service.calculate_score(
            report
        )

        report["score"] = score

        with open(report_file, "w", encoding="utf-8") as file:

            json.dump(
                report,
                file,
                indent=4
            )

        print(f"Score = {score}/100\n")

    print("All reports updated successfully.")


if __name__ == "__main__":
    main()