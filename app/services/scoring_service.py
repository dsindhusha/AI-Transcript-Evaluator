MISSING_PENALTY = 10
INCORRECT_PENALTY = 5
CONFLICTING_PENALTY = 15
EXTRA_PENALTY = 3


class ScoringService:

    def calculate_score(self, report: dict) -> int:

        score = 100

        score -= len(report["missing_information"]) * MISSING_PENALTY

        score -= len(report["incorrect_information"]) * INCORRECT_PENALTY

        score -= len(report["conflicting_information"]) * CONFLICTING_PENALTY

        score -= len(report["extra_information"]) * EXTRA_PENALTY

        return max(score, 0)