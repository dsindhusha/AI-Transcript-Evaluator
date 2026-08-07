import json

from app.prompts import EVALUATION_PROMPT
from app.services.gemini_service import GeminiService

class EvaluatorService:

    def __init__(self):
        self.gemini = GeminiService()

    def evaluate(
        self,
        ground_truth: str,
        generated: str
    ) -> dict:

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