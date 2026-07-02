from pathlib import Path

import httpx



from exceptions import TranscriptionException


class TranscriptionService:

    def __init__(self):

        self.endpoint = "http://localhost:2000/transcribe"

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