from pathlib import Path

from models.internal_models import VideoUnderstandingResult

from services.youtube_download_service import (
    YouTubeDownloadService,
)
from services.video_processing_service import (
    VideoProcessingService,
)
from services.transcription_service import (
    TranscriptionService,
)
from services.transcript_service import (
    TranscriptService,
)
from services.ocr_service import (
    OCRService,
)
from services.vision_service import (
    VisionService,
)

from exceptions import (
    TranscriptNotFoundException,
    VideoDownloadException,
    VideoProcessingException,
    TranscriptionException,
    OCRException,
    VisionException
)


class VideoPipelineService:

    def __init__(self):

        self.youtube_download_service = (
            YouTubeDownloadService()
        )

        self.video_processing_service = (
            VideoProcessingService()
        )

        self.transcript_service = (
            TranscriptService()
        )

        self.transcription_service = (
            TranscriptionService()
        )

        self.ocr_service = (
            OCRService()
        )
        self.vision_service = (
           VisionService()
        )

    def process(
        self,
        youtube_url: str,
    ) -> VideoUnderstandingResult:

        video_path: Path | None = None

        try:

            video_path = (
                self.youtube_download_service.download(
                    youtube_url
                )
            )

            processing_response = (
                self.video_processing_service.process(
                    video_path
                )
            )

            try:

                transcript = (
                    self.transcript_service.get_transcript(
                        youtube_url
                    )
                )

            except TranscriptNotFoundException:

                transcript = (
                    self.transcription_service.transcribe(
                        processing_response["audio_path"]
                    )
                )

            scenes = processing_response["scenes"]

            ocr = self.ocr_service.extract(scenes)

            vision = self.vision_service.analyze(scenes)


            return VideoUnderstandingResult(
                transcript=transcript,
                metadata=processing_response["metadata"],
                scenes=scenes,
                ocr=ocr,
                vision=vision,
            )

        except (
            VideoDownloadException,
            VideoProcessingException,
            TranscriptionException,
            OCRException,
            VisionException
        ):
            raise

        finally:

            if (
                video_path
                and video_path.exists()
            ):
                video_path.unlink()