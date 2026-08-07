import json

from pathlib import Path


class ReportService:
    """
    Handles saving evaluation reports as formatted JSON files.
    """

    def save_report(
        self,
        report: dict,
        output_path: Path
    ):
        """
        Saves the evaluation report to the specified output path.

        Args:
            report: Evaluation report to be saved.
            output_path: Destination path for the JSON report.
        """

        output_path.write_text(
            json.dumps(report, indent=4),
            encoding="utf-8"
        )