import os
from dotenv import load_dotenv
from google import  genai


class Generator:
    def __init__(self):
        load_dotenv()
        self.key = os.getenv('GEMINI_API_KEY')
        if not self.key:
            raise ValueError('GEMINI_API_KEY not found in environment variables')
        self.client = genai.Client(api_key=self.key)
    def generate(self,
                 prompt,
                 model='gemini-3.5-flash-lite'):
        result = self.client.interactions.create(
            model=model,
            input=prompt
        )
        response = result.output_text
        return response