from groq import Groq

from config import GROQ_API_KEY
from exceptions import GroqException


class GroqService:

    def __init__(self):
        self.client = Groq(api_key=GROQ_API_KEY)
        self.model = "llama-3.3-70b-versatile"

    def generate(self, prompt: str) -> str:

        try:

            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.5,
                max_tokens=1024
            )

            return response.choices[0].message.content

        except Exception as e:
            raise GroqException("Failed to generate response.") from e