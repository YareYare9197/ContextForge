import os

from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()


class GeminiClient:
    def __init__(
        self,
        api_key: str | None = None,
        model_name: str | None = None,
    ):
        key = api_key or os.getenv("GEMINI_API_KEY")

        if not key:
            raise RuntimeError("GEMINI_API_KEY is not configured")

        self.model_name = (
            model_name
            or os.getenv("GEMINI_MODEL")
            or "gemini-2.5-flash"
        )

        self.client = genai.Client(api_key=key)

    def generate(
        self,
        system_prompt: str,
        user_prompt: str,
    ) -> str:
        response = self.client.models.generate_content(
            model=self.model_name,
            contents=user_prompt,
            config=types.GenerateContentConfig(
                system_instruction=system_prompt,
            ),
        )

        return response.text or ""
    