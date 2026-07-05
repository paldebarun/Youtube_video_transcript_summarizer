from pathlib import Path

import httpx

from config import VIDEO_PROCESSING_SERVICE_URL
from exceptions import VideoProcessingException


class VideoProcessingService:

    def __init__(self):

        self.endpoint = (
            f"{VIDEO_PROCESSING_SERVICE_URL}/process"
        )

    def process(
        self,
        video_path: Path,
    ) -> dict:

        try:

            with open(video_path, "rb") as video:

                response = httpx.post(
                    self.endpoint,
                    files={
                        "file": (
                            video_path.name,
                            video,
                            "video/mp4",
                        )
                    },
                    timeout=600,
                )

            response.raise_for_status()

            return response.json()

        except Exception as e:

            raise VideoProcessingException(
                "Failed to process video."
            ) from e