import httpx

from config import OCR_SERVICE_URL
from exceptions import OCRException


class OCRService:

    def __init__(self):

        self.endpoint = (
            f"{OCR_SERVICE_URL}/extract-text"
        )

    def extract(
        self,
        scenes: list[dict],
    ) -> dict:

        try:

            response = httpx.post(
                self.endpoint,
                json={
                    "scenes": scenes,
                },
                timeout=600,
            )

            response.raise_for_status()

            return response.json()

        except Exception as e:

            raise OCRException(
                "Failed to extract OCR."
            ) from e