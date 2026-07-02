from urllib.parse import parse_qs, urlparse

from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api._errors import (
    NoTranscriptFound,
    TranscriptsDisabled,
    VideoUnavailable,
)

from exceptions import (
    AudioDownloadException,
    InvalidYouTubeUrlException,
    TranscriptNotFoundException,
    TranscriptionException,
)
from services.audio_service import AudioService
from services.diarization_service import DiarizationService
from services.transcription_service import TranscriptionService


class TranscriptService:

    def __init__(self):

        self.audio_service = AudioService()
        self.transcription_service = TranscriptionService()
        self.diarization_service = DiarizationService()

    def extract_video_id(self, url: str) -> str:

        parsed = urlparse(url)

        if parsed.hostname == "youtu.be":
            return parsed.path[1:]

        if parsed.hostname in (
            "youtube.com",
            "www.youtube.com",
            "m.youtube.com",
        ):
            video_id = parse_qs(parsed.query).get("v", [None])[0]

            if video_id:
                return video_id

        raise InvalidYouTubeUrlException("Invalid YouTube URL.")

    def get_transcript(self, url: str) -> str:

        audio_path = None

        try:

            video_id = self.extract_video_id(url)

            api = YouTubeTranscriptApi()

            transcript = api.fetch(video_id)

            return " ".join(
                snippet.text
                for snippet in transcript
            )

        except (
            NoTranscriptFound,
            TranscriptsDisabled,
            VideoUnavailable,
        ):

            try:

                audio_path = self.audio_service.download_audio(url)

                transcript = self.transcription_service.transcribe(
                    audio_path
                )

                # Future:
                # speaker_segments = self.diarization_service.diarize(audio_path)
                # transcript = merge_transcript(transcript, speaker_segments)

                return transcript

            except (
                AudioDownloadException,
                TranscriptionException,
            ) as e:

                raise TranscriptNotFoundException(
                    "Unable to generate transcript for this video."
                ) from e

            finally:

                if audio_path:
                    self.audio_service.delete_audio(audio_path)