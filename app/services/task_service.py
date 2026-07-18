from uuid import uuid4
from datetime import datetime, UTC

from app.messaging.redis_queue import RedisQueue

from app.repo.task_repository import TaskRepository

from app.models.task_document import (
    TaskDocument,
    TaskInput,
    ServiceResult,
    ServiceStatus,
    ServiceType,
)

from app.workflow.workflow_state import WorkflowStage

from app.config import MASTER_QUEUE


class TaskService:

    def __init__(self):

        self.repository = TaskRepository()

        self.queue = RedisQueue()

    def create_task(
        self,
        youtube_url: str,
    ) -> str:

        task_id = str(uuid4())

        task = TaskDocument(
            _id=task_id,
            status=ServiceStatus.QUEUED,
            workflow_stage=WorkflowStage.TASK_CREATED,
            created_at=datetime.now(UTC),
            input=TaskInput(
                youtube_url=youtube_url,
            ),
        )

        self.repository.create_task(task)

        self.queue.push(
            MASTER_QUEUE,
            {
                "task_id": task_id,
            },
        )

        return task_id

    def get_task(
        self,
        task_id: str,
    ) -> TaskDocument:

        return self.repository.get_task(
            task_id,
        )

    def update_task(
        self,
        task: TaskDocument,
    ):

        self.repository.update_task(
            task,
        )

    def update_service_result(
        self,
        task_id: str,
        service: ServiceType,
        result,
    ):

        task = self.get_task(
            task_id,
        )

        service_result: ServiceResult = getattr(
            task,
            service.value,
        )

        service_result.status = ServiceStatus.COMPLETED
        service_result.completed_at = datetime.now(
            UTC,
        )
        service_result.error = None
        service_result.result = result


        task.status = ServiceStatus.PROCESSING

        self.update_task(task)

    def mark_service_failed(
        self,
        task_id: str,
        service: ServiceType,
        error: str,
    ):

        task = self.get_task(
            task_id,
        )

        service_result: ServiceResult = getattr(
            task,
            service.value,
        )

        service_result.status = ServiceStatus.FAILED
        service_result.completed_at = datetime.now(
            UTC,
        )
        service_result.error = error

        task.status = ServiceStatus.FAILED
        task.completed_at = datetime.now(
            UTC,
        )

        self.update_task(task)

    def mark_service_queued(
        self,
        task_id: str,
        service: ServiceType,
    ):

        task = self.get_task(
            task_id,
        )

        service_result = getattr(
            task,
            service.value,
        )

        service_result.status = ServiceStatus.QUEUED
        service_result.started_at = datetime.now(UTC)

        self.update_task(
            task,
        )

    def update_summary(
        self,
        task_id: str,
        summary,
    ):

        task = self.get_task(
            task_id,
        )

        task.summary.status = ServiceStatus.COMPLETED
        task.summary.completed_at = datetime.now(
            UTC,
        )
        task.summary.result = summary

        task.workflow_stage = WorkflowStage.COMPLETED

        task.status = ServiceStatus.COMPLETED
        task.completed_at = datetime.now(
            UTC,
        )

        self.update_task(task)

    def all_services_completed(
        self,
        task: TaskDocument,
    ) -> bool:

        services = [
            task.video_processing,
            task.ocr,
            task.vision,
            task.whisper,
        ]

        return all(
            service.status == ServiceStatus.COMPLETED
            for service in services
        )

    def mark_workflow_stage(
        self,
        task_id: str,
        stage: WorkflowStage,
    ):

        task = self.get_task(
            task_id,
        )

        task.workflow_stage = stage

        self.update_task(task)