import json
import re

from services.video_pipeline_service import VideoPipelineService
from exceptions import GroqException
from models.request_models import SummaryResponse
from prompts import summarization_prompt

from services.groq_services import GroqService
# from services.ocr_service import OCRService
# from services.transcript_service import TranscriptService


class SummarizationService:

    def __init__(self):
        # self.transcript_service = TranscriptService()
        # self.ocr_service = OCRService()
        self.groq_service = GroqService()
        self.video_pipeline_service = VideoPipelineService()

    def summarize(self, youtube_url: str) -> SummaryResponse:

        # transcript = self.transcript_service.get_transcript(youtube_url)
        
        video = self.video_pipeline_service.process(
    youtube_url
)
        


        prompt = summarization_prompt(transcript=video.transcript,
    ocr=video.ocr,
    metadata=video.metadata,
    vision=video.vision,
)

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