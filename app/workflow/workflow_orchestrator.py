from app.models.event_model import WorkflowEvent
from app.models.job_model import (
    VideoJob,
    OCRJob,
    VisionJob,
    WhisperJob,
)

from app.models.task_document import ServiceType

from app.workflow.workflow_state import WorkflowStage

from app.services.task_service import TaskService
from app.services.youtube_download_service import (
    YouTubeDownloadService,
)

from app.models.job_model import SummaryJob

from app.clients.video_client import VideoClient
from app.clients.ocr_client import OCRClient
from app.clients.vision_client import VisionClient
from app.clients.whisper_client import WhisperClient

from app.messaging.redis_queue import RedisQueue

from app.config import SUMMARY_QUEUE

from app.utils.logger import Logger

logger = Logger.get_logger()


class WorkflowOrchestrator:

    def __init__(self):

        self.task_service = TaskService()

        self.downloader = YouTubeDownloadService()

        self.video_client = VideoClient()
        self.ocr_client = OCRClient()
        self.vision_client = VisionClient()
        self.whisper_client = WhisperClient()

        self.summary_queue = RedisQueue()

    def handle_task_created(
        self,
        task_id: str,
    ):

        task = self.task_service.get_task(
            task_id,
        )

        try:

            logger.info(
                f"Downloading video for task: {task_id}"
            )

            video_path = self.downloader.download(
                task.input.youtube_url,
            )

            self.task_service.mark_service_queued(
                task.id,
                ServiceType.VIDEO_PROCESSING,
            )

            self.task_service.mark_workflow_stage(
                task.id,
                WorkflowStage.VIDEO_PROCESSING,
            )

            job = VideoJob(
                task_id=task.id,
                video_path=str(video_path),
            )

            self.video_client.submit(job)

            logger.info(
                f"Video job submitted: {task.id}"
            )

        except Exception as e:

            logger.error(
                f"Failed to create workflow for {task_id}: {e}"
            )

            self.task_service.mark_service_failed(
                task.id,
                ServiceType.VIDEO_PROCESSING,
                str(e),
            )

            self.task_service.mark_workflow_stage(
                task.id,
                WorkflowStage.FAILED,
            )

            raise

    def handle_event(
            self,
            event: WorkflowEvent,
        ):

            handlers = {

                "video.completed": self.handle_video_completed,
                "video.failed": self.handle_video_failed,

                "ocr.completed": self.handle_ocr_completed,
                "ocr.failed": self.handle_ocr_failed,

                "vision.completed": self.handle_vision_completed,
                "vision.failed": self.handle_vision_failed,

                "whisper.completed": self.handle_whisper_completed,
                "whisper.failed": self.handle_whisper_failed,
            }

            handler = handlers.get(event.event_type)

            if handler is None:

                logger.warning(
                    f"Unknown workflow event: {event.event_type}"
                )

                return

            if event.event_type.endswith(".completed") and event.payload is None:

                raise ValueError(
                    f"Completed event '{event.event_type}' is missing payload."
                )

            if event.event_type.endswith(".failed") and event.error is None:

                raise ValueError(
                    f"Failed event '{event.event_type}' is missing error."
                )

            handler(event)


    def handle_video_completed(
        self,
        event: WorkflowEvent,
    ):

        try:

            self.task_service.update_service_result(
                event.task_id,
                ServiceType.VIDEO_PROCESSING,
                event.payload,
            )

            self.task_service.mark_workflow_stage(
                event.task_id,
                WorkflowStage.PARALLEL_PROCESSING,
            )

            payload = event.payload

            logger.info(
                f"Submitting OCR, Vision and Whisper jobs for {event.task_id}"
            )

            self.task_service.mark_service_queued(
                event.task_id,
                ServiceType.OCR,
            )

            self.ocr_client.submit(
                OCRJob(
                    task_id=event.task_id,
                    frames=payload["scenes"],
                )
            )

            self.task_service.mark_service_queued(
                event.task_id,
                ServiceType.VISION,
            )

            self.vision_client.submit(
                VisionJob(
                    task_id=event.task_id,
                    frames=payload["scenes"],
                )
            )

            self.task_service.mark_service_queued(
                event.task_id,
                ServiceType.WHISPER,
            )

            self.whisper_client.submit(
                WhisperJob(
                    task_id=event.task_id,
                    audio_path=payload["audio_path"],
                )
            )

        except Exception as e:

            logger.error(
                f"Failed to submit downstream jobs for {event.task_id}: {e}"
            )

            self.task_service.mark_workflow_stage(
                event.task_id,
                WorkflowStage.FAILED,
            )

            raise


    def _handle_parallel_completion(
        self,
        task_id: str,
        service: ServiceType,
        payload,
    ):

        self.task_service.update_service_result(
            task_id,
            service,
            payload,
        )

        task = self.task_service.get_task(
            task_id,
        )

        if self.task_service.all_services_completed(
            task,
        ):

            logger.info(
                f"Submitting Summary job for {task_id}"
            )

            self.task_service.mark_service_queued(
                task_id,
                ServiceType.SUMMARY,
            )

            self.task_service.mark_workflow_stage(
                task_id,
                WorkflowStage.SUMMARY_PROCESSING,
            )

            job = SummaryJob(
                task_id=task_id,
            )

            self.summary_queue.push(
                SUMMARY_QUEUE,
                job.model_dump(),
            )



    def handle_ocr_completed(
        self,
        event: WorkflowEvent,
    ):

        self._handle_parallel_completion(
            event.task_id,
            ServiceType.OCR,
            event.payload,
        )


    def handle_vision_completed(
        self,
        event: WorkflowEvent,
    ):

        self._handle_parallel_completion(
            event.task_id,
            ServiceType.VISION,
            event.payload,
        )

    
    def handle_whisper_completed(
        self,
        event: WorkflowEvent,
    ):

        self._handle_parallel_completion(
            event.task_id,
            ServiceType.WHISPER,
            event.payload,
        )

    def _handle_failure(
        self,
        event: WorkflowEvent,
        service: ServiceType,
    ):

        logger.error(
            f"{event.event_type} | Task: {event.task_id} | Error: {event.error}"
        )

        self.task_service.mark_service_failed(
            event.task_id,
            service,
            event.error or "Unknown error",
        )

        self.task_service.mark_workflow_stage(
            event.task_id,
            WorkflowStage.FAILED,
        )

    def handle_video_failed(self, event):
        self._handle_failure(
            event,
            ServiceType.VIDEO_PROCESSING,
        )

    def handle_ocr_failed(self, event):
        self._handle_failure(
            event,
            ServiceType.OCR,
        )

    def handle_vision_failed(self, event):
        self._handle_failure(
            event,
            ServiceType.VISION,
        )

    def handle_whisper_failed(self, event):
        self._handle_failure(
            event,
            ServiceType.WHISPER,
        )