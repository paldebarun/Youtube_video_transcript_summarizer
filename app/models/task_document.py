from datetime import datetime
from enum import Enum
from typing import Any

from pydantic import BaseModel, Field
from workflow.workflow_state import WorkflowStage, ServiceStatus




class ServiceResult(BaseModel):

    status: ServiceStatus = ServiceStatus.PENDING

    started_at: datetime | None = None

    completed_at: datetime | None = None

    error: str | None = None

    result: Any = None


class TaskInput(BaseModel):

    youtube_url: str


class SummaryResult(BaseModel):

    status: ServiceStatus = ServiceStatus.PENDING

    started_at: datetime | None = None

    completed_at: datetime | None = None

    error: str | None = None

    result: Any = None


class TaskDocument(BaseModel):

    id: str = Field(alias="_id")

    status: ServiceStatus = ServiceStatus.PENDING

    workflow_stage: WorkflowStage = WorkflowStage.TASK_CREATED

    created_at: datetime

    completed_at: datetime | None = None

    input: TaskInput

    video_processing: ServiceResult = ServiceResult()

    ocr: ServiceResult = ServiceResult()

    vision: ServiceResult = ServiceResult()

    whisper: ServiceResult = ServiceResult()

    summary: SummaryResult = SummaryResult()

    model_config = {
        "populate_by_name": True
    }


class ServiceType(str, Enum):
    VIDEO_PROCESSING = "video_processing"
    OCR = "ocr"
    VISION = "vision"
    WHISPER = "whisper"
    SUMMARY = "summary"