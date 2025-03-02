import os
from google import genai
from dotenv import load_dotenv
load_dotenv()


class LLMClient:
    def __init__(self,):
        api_key = os.environ.get('GEMINI_API_KEY')
        self.llm_client = genai.Client(api_key=api_key)

    def run(self, message: str):
        response = self.llm_client.models.generate_content(
            model="gemini-2.0-flash", contents=message
        )
        return response