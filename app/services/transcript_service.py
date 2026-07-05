from urllib.parse import parse_qs, urlparse
from pathlib import Path

from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api._errors import (
    NoTranscriptFound,
    TranscriptsDisabled,
    VideoUnavailable,
)

from exceptions import (
    InvalidYouTubeUrlException,
    TranscriptNotFoundException,
    TranscriptionException,
    VideoDownloadException,
    VideoProcessingException,
)

from services.youtube_download_service import (
    YouTubeDownloadService,
)
from services.video_processing_service import (
    VideoProcessingService,
)
from services.transcription_service import (
    TranscriptionService,
)
from services.diarization_service import (
    DiarizationService,
)


class TranscriptService:

    def __init__(self):

        self.youtube_download_service = (
            YouTubeDownloadService()
        )

        self.video_processing_service = (
            VideoProcessingService()
        )

        self.transcription_service = (
            TranscriptionService()
        )

        self.diarization_service = (
            DiarizationService()
        )

    def extract_video_id(
        self,
        url: str,
    ) -> str:

        parsed = urlparse(url)

        if parsed.hostname == "youtu.be":
            return parsed.path[1:]

        if parsed.hostname in (
            "youtube.com",
            "www.youtube.com",
            "m.youtube.com",
        ):

            video_id = parse_qs(
                parsed.query
            ).get(
                "v",
                [None],
            )[0]

            if video_id:
                return video_id

        raise InvalidYouTubeUrlException(
            "Invalid YouTube URL."
        )

    def get_transcript(
        self,
        url: str,
    ) -> str:

        video_path: Path | None = None

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

                video_path = (
                    self.youtube_download_service.download(
                        url
                    )
                )
                print(f"Downloaded video to: {video_path}")
                processing_response = (
                    self.video_processing_service.process(
                        video_path
                    )
                )
                print(f"Video processing response: {processing_response}")
                audio_path = processing_response[
                    "audio_path"
                ]
                print(f"Extracted audio path: {audio_path}")
                transcript = (
                    self.transcription_service.transcribe(
                        audio_path
                    )
                )
                print(f"Generated transcript: {transcript}")
                # Future:
                # speaker_segments = (
                #     self.diarization_service.diarize(
                #         audio_path
                #     )
                # )

                return transcript

            except (
                VideoDownloadException,
                VideoProcessingException,
                TranscriptionException,
            ) as e:
                print(f"this is the error : {e}")
                raise TranscriptNotFoundException(
                    "Unable to generate transcript for this video."
                ) from e

            finally:

                if (
                    video_path
                    and video_path.exists()
                ):
                    video_path.unlink()