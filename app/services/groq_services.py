from groq import Groq

from app.config import (
    GROQ_API_KEY,
    GROQ_MODEL,
)
from app.exceptions import GroqException
from app.utils.logger import Logger

logger = Logger.get_logger()


class GroqService:

    def __init__(self):

        self.client = Groq(
            api_key=GROQ_API_KEY,
        )

        self.model = GROQ_MODEL

    def generate(
        self,
        prompt: str,
    ) -> str:

        try:

            logger.info(
                "Generating summary using Groq."
            )

            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "user",
                        "content": prompt,
                    }
                ],
                temperature=0.5,
                max_tokens=2048,
            )

            return response.choices[0].message.content

        except Exception as e:

            logger.error(
                f"Groq request failed: {e}"
            )

            raise GroqException(
                "Failed to generate response."
            ) from e