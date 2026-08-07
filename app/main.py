from pathlib import Path

from app.services.evaluator_service import EvaluatorService
from app.services.report_service import ReportService
from app.services.scoring_service import ScoringService


def main():
    """
    Evaluates all transcript pairs in the dataset, calculates
    their scores, and saves the evaluation reports.
    """

    evaluator = EvaluatorService()
    report_service = ReportService()
    scoring_service = ScoringService()

    ground_truth_folder = Path("dataset/ground_truth")
    generated_folder = Path("dataset/generated")
    reports_folder = Path("dataset/reports")

    ground_truth_files = sorted(
        ground_truth_folder.glob("*.txt")
    )

    print(f"Found {len(ground_truth_files)} transcript pairs.\n")

    for ground_truth_file in ground_truth_files:

        generated_file = (
            generated_folder /
            ground_truth_file.name
        )

        report_file = (
            reports_folder /
            f"{ground_truth_file.stem}.json"
        )

        print(f"Evaluating {ground_truth_file.stem}...")

        try:

            ground_truth = ground_truth_file.read_text(
                encoding="utf-8"
            )

            generated = generated_file.read_text(
                encoding="utf-8"
            )

            report = evaluator.evaluate(
                ground_truth,
                generated
            )

            score = scoring_service.calculate_score(
                report
            )

            report["score"] = score

            report_service.save_report(
                report,
                report_file
            )

            print(f"Saved {report_file.name}")
            print(f"Score : {score}/100\n")

        except Exception as e:

            print(f"Skipping {ground_truth_file.stem}")
            print(f"Reason: {e}\n")

    print("Evaluation completed successfully.")


if __name__ == "__main__":
    main()