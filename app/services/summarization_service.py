import json

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
         
        print(response)
        try:

            summary = json.loads(response)
            return SummaryResponse(**summary)

        except Exception as e:
            print(e)
            raise GroqException(
                "Failed to parse summary response."
            ) from e