from pathlib import Path
from urllib import response

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
            audio_file = Path(audio_path)

            print("Exists:", audio_file.exists())
            print("Audio path:", audio_file)

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
            print(response.status_code)
            print(response.text)
            response.raise_for_status()

            return response.json()["text"]

        except Exception as e:
            import traceback

            traceback.print_exc()

            print("Audio path:", audio_path)
            print("Whisper endpoint:", self.endpoint)
            print("Actual exception:", repr(e))

            raise TranscriptionException(
                "Failed to transcribe audio."
            ) from e