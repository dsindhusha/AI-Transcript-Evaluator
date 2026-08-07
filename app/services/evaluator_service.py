import json

from app.prompts import EVALUATION_PROMPT
from app.services.gemini_service import GeminiService


class EvaluatorService:
    """
    Compares a generated transcript with the ground truth transcript
    using Gemini AI and returns a structured evaluation report.
    """

    def __init__(self):
        """
        Initializes the Gemini service.
        """
        self.gemini = GeminiService()

    def evaluate(
        self,
        ground_truth: str,
        generated: str
    ) -> dict:
        """
        Evaluates the generated transcript against the ground truth.

        Args:
            ground_truth: Reference transcript.
            generated: Transcript generated from the audio.

        Returns:
            A structured evaluation report as a dictionary.
        """

        prompt = (
            EVALUATION_PROMPT
            + "\n\n"
            + "Ground Truth Transcript:\n"
            + ground_truth
            + "\n\n"
            + "Generated Transcript:\n"
            + generated
        )

        response = self.gemini.generate_response(prompt)

        return json.loads(response)