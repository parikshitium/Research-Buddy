import os
from dotenv import load_dotenv
from google import  genai


class Generator():
    def __init__(self):
        load_dotenv()
        self.key = os.getenv('GEMINI_API_KEY')
        if not self.key:
            raise ValueError('Key does not exist')
        self.client = genai.Client(api_key=self.key)
    def generate(self,
                 prompt,
                 model='gemini-3.5-flash-lite'):
        feed = self.client.interactions.create(
            model=model,
            input=prompt
        )
        response = feed.output_text
        return response