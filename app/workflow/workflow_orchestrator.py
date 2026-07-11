from models.job_model import VideoJob

from services.youtube_download_service import (
    YouTubeDownloadService,
)

from services.video_processing_service import (
    VideoProcessingService,
)

from repo.task_repository import TaskRepository

from .workflow_state import WorkflowStage


class WorkflowOrchestrator:

    def __init__(self):

        self.repository = TaskRepository()

        self.downloader = (
            YouTubeDownloadService()
        )

        self.video_service = (
            VideoProcessingService()
        )

    def handle_task_created(
        self,
        task_id: str,
    ):

        task = self.repository.get_task(task_id)

        video_path = self.downloader.download(
            task.input.youtube_url
        )

        job = VideoJob(
            task_id=task.id,
            video_path=str(video_path),
        )

        self.video_service.submit(job)
        self.repository.update_stage(
            task.id,
            WorkflowStage.VIDEO_PROCESSING,
        )


    def handle_event(
        self,
        event,
    ):

        if event.event_type == "video.completed":

            self.handle_video_completed(event)

        elif event.event_type == "video.failed":

            self.handle_video_failed(event)

    def handle_video_completed(
        self,
        event,
    ):

        self.repository.update_video_result(
            event.task_id,
            event.payload,
        )

        # TODO
        # submit OCR
        # submit Vision
        # submit Whisper

    def handle_video_failed(
        self,
        event,
    ):

        self.repository.mark_failed(
            event.task_id,
            event.error,
        )