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

class AudioDownloadException(Exception):
    pass


class TranscriptionException(Exception):
    pass


class DiarizationException(Exception):
    pass

class VideoDownloadException(Exception):
    pass


class VideoProcessingException(Exception):
    pass

class OCRException(Exception):

    pass