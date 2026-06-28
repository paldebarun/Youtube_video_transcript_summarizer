from urllib.parse import parse_qs, urlparse

from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api._errors import (
    NoTranscriptFound,
    TranscriptsDisabled,
    VideoUnavailable,
)

from app.exceptions import (
    InvalidYouTubeUrlException,
    TranscriptNotFoundException,
)


class YouTubeService:

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

        try:
            video_id = self.extract_video_id(url)

            api = YouTubeTranscriptApi()

            transcript = api.fetch(video_id)

            return " ".join(snippet.text for snippet in transcript)

        except (
            NoTranscriptFound,
            TranscriptsDisabled,
            VideoUnavailable,
        ) as e:
            raise TranscriptNotFoundException(str(e))