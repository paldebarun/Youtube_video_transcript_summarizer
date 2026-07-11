from datetime import UTC, datetime

from pydantic import BaseModel, Field


class WorkflowEvent(BaseModel):

    task_id: str

    event_type: str

    payload: dict

    timestamp: datetime = Field(
        default_factory=lambda: datetime.now(UTC)
    )