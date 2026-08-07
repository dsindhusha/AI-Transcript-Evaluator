MISSING_PENALTY = 10
INCORRECT_PENALTY = 5
CONFLICTING_PENALTY = 15
EXTRA_PENALTY = 3


class ScoringService:

    def calculate_score(self, report: dict) -> int:

        breakdown = self.get_score_breakdown(report)

        return breakdown["final_score"]

    def get_score_breakdown(self, report: dict) -> dict:

        starting_score = 100

        missing_count = len(report["missing_information"])
        incorrect_count = len(report["incorrect_information"])
        conflicting_count = len(report["conflicting_information"])
        extra_count = len(report["extra_information"])

        missing_deduction = missing_count * MISSING_PENALTY
        incorrect_deduction = incorrect_count * INCORRECT_PENALTY
        conflicting_deduction = conflicting_count * CONFLICTING_PENALTY
        extra_deduction = extra_count * EXTRA_PENALTY

        final_score = (
            starting_score
            - missing_deduction
            - incorrect_deduction
            - conflicting_deduction
            - extra_deduction
        )

        final_score = max(final_score, 0)

        return {

            "starting_score": starting_score,

            "missing": {
                "count": missing_count,
                "penalty": MISSING_PENALTY,
                "deduction": missing_deduction
            },

            "incorrect": {
                "count": incorrect_count,
                "penalty": INCORRECT_PENALTY,
                "deduction": incorrect_deduction
            },

            "conflicting": {
                "count": conflicting_count,
                "penalty": CONFLICTING_PENALTY,
                "deduction": conflicting_deduction
            },

            "extra": {
                "count": extra_count,
                "penalty": EXTRA_PENALTY,
                "deduction": extra_deduction
            },

            "final_score": final_score
        }