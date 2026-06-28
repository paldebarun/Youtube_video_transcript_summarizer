class YouTubeException(Exception):
    """Base exception for YouTube related errors."""
    pass


class InvalidYouTubeUrlException(YouTubeException):
    pass


class TranscriptNotFoundException(YouTubeException):
    pass


class GroqException(Exception):
    """Base exception for Groq related errors."""
    pass