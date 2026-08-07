import json

from pathlib import Path


class ReportService:

    def save_report(
        self,
        report: dict,
        output_path: Path
    ):

        output_path.write_text(
            json.dumps(report, indent=4),
            encoding="utf-8"
        )