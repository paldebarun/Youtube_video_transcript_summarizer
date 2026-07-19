import json
import re

from app.exceptions import GroqException

from app.models.internal_models import (
    VideoUnderstandingResult,
)

from app.models.request_models import (
    SummaryResult,
)

from app.prompts import summarization_prompt

from app.services.groq_services import GroqService

from app.utils.logger import Logger

logger = Logger.get_logger()


class SummarizationService:

    def __init__(self):

        self.groq_service = GroqService()

    def summarize(
        self,
        video: VideoUnderstandingResult,
    ) -> SummaryResult:

        prompt = summarization_prompt(
            transcript=video.transcript,
            metadata=video.metadata,
            ocr=video.ocr,
            vision=video.vision,
        )

        response = self.groq_service.generate(
            prompt,
        )

        try:

            match = re.search(
                r"\{.*\}",
                response,
                re.DOTALL,
            )

            if match is None:

                raise ValueError(
                    "No JSON object found."
                )

            summary = json.loads(
                match.group(),
            )

            logger.info(
                "Summary generated successfully."
            )

            return SummaryResult(
                **summary,
            )

        except Exception as e:

            logger.error(
                f"Failed parsing summary: {e}"
            )

            raise GroqException(
                "Failed to parse summary."
            ) from e