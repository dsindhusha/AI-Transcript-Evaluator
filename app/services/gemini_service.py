import os
import time

from dotenv import load_dotenv
from google import genai


load_dotenv()


class GeminiService:

    def __init__(self):

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