import json
import re

from models.request_models import SummaryResponse
from prompts import summarization_prompt
from services.groq_services import GroqService
from services.transcript_service import TranscriptService
from exceptions import GroqException


class SummarizationService:

    def __init__(self):
        self.transcript_service = TranscriptService()
        self.groq_service = GroqService()

    def summarize(self, youtube_url: str) -> SummaryResponse:

        transcript = self.transcript_service.get_transcript(youtube_url)

        prompt = summarization_prompt(transcript)

        response = self.groq_service.generate(prompt)

        print("Raw LLM Response:\n", response)

        try:

            match = re.search(r"\{.*\}", response, re.DOTALL)

            if not match:
                raise ValueError("No JSON object found in LLM response.")

            summary = json.loads(match.group())

            return SummaryResponse(**summary)

        except Exception as e:

            print("Failed to parse response:", e)

            raise GroqException(
                "Failed to parse summary response."
            ) from e