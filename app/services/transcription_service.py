from pathlib import Path

import httpx



from exceptions import TranscriptionException
from config import WHISPER_SERVICE_URL

class TranscriptionService:

    def __init__(self):

        self.endpoint = f"{WHISPER_SERVICE_URL}/transcribe"

    def transcribe(
        self,
        audio_path: str,
    ) -> str:

        try:

            with open(audio_path, "rb") as audio:

                response = httpx.post(
                    self.endpoint,
                    files={
                        "file": (
                            Path(audio_path).name,
                            audio,
                            "audio/mpeg",
                        )
                    },
                    timeout=300,
                )

            response.raise_for_status()

            return response.json()["text"]

        except Exception as e:

            raise TranscriptionException(
                "Failed to transcribe audio."
            ) from e