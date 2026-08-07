import os
import time

from dotenv import load_dotenv
from google import genai


load_dotenv()


class GeminiService:
    """
    Handles interactions with the Google Gemini API for
    generating transcript evaluation responses.
    """

    def __init__(self):
        """
        Initializes the Gemini client using the API key
        loaded from the environment variables.
        """

        api_key = os.getenv("GEMINI_API_KEY")

        if not api_key:
            raise ValueError("GEMINI_API_KEY not found in .env")

        self.client = genai.Client(
            api_key=api_key
        )

    def generate_response(
        self,
        prompt: str
    ) -> str:
        """
        Sends the evaluation prompt to the Gemini model and
        returns the generated response. The request is retried
        up to three times in case of temporary failures.

        Args:
            prompt: The evaluation prompt sent to the Gemini model.

        Returns:
            The generated response as a string.
        """

        max_attempts = 3

        for attempt in range(max_attempts):

            try:

                response = self.client.models.generate_content(
                    model="gemini-3.5-flash",
                    contents=prompt
                )

                return response.text

            except Exception as e:

                print(f"Attempt {attempt + 1} failed.")

                if attempt == max_attempts - 1:
                    raise e

                print("Retrying in 3 seconds...\n")

                time.sleep(3)