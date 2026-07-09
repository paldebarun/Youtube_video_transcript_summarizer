import uuid
from datetime import datetime, timezone

from messaging.redis_queue import RedisQueue
from repo.task_repository import TaskRepository

from models.task_document import (
    TaskDocument,
    TaskInput,
    WorkflowStage,
    ServiceStatus,
)

from config import MASTER_QUEUE


class TaskService:

    def __init__(self):

        self.repository = TaskRepository()

        self.queue = RedisQueue()

    def create_task(
        self,
        youtube_url: str,
    ) -> str:

        task_id = str(uuid.uuid4())

        task = TaskDocument(
            _id=task_id,
            status=ServiceStatus.PROCESSING,
            workflow_stage=WorkflowStage.TASK_CREATED,
            created_at=datetime.now(timezone.utc),
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