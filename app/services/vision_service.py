import httpx

from config import VISION_SERVICE_URL
from exceptions import VisionException


class VisionService:

    def __init__(self):

        self.endpoint = (
            f"{VISION_SERVICE_URL}/analyze"
        )

    def analyze(
        self,
        frames: list[dict],
    ) -> dict:

        try:

            response = httpx.post(
                self.endpoint,
                json={
                    "frames": frames,
                },
                timeout=600,
            )

            response.raise_for_status()

            return response.json()

        except Exception as e:

            raise VisionException(
                "Failed to analyze video frames."
            ) from e