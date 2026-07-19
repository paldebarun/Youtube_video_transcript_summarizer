from enum import Enum

from pydantic import BaseModel


class TaskStatus(str, Enum):

    PENDING = "PENDING"

    PROCESSING = "PROCESSING"

    COMPLETED = "COMPLETED"

    FAILED = "FAILED"


class SubmitTaskResponse(BaseModel):

    task_id: str

    status: TaskStatus


class TaskStatusResponse(BaseModel):

    task_id: str

    status: TaskStatus

    message: str | None = None