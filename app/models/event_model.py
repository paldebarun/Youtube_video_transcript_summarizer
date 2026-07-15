
from datetime import UTC, datetime
from typing import Any

from pydantic import BaseModel, Field


class WorkflowEvent(BaseModel):

    task_id: str

    event_type: str

    payload: dict[str, Any] | None = None

    error: str | None = None

    timestamp: datetime = Field(
        default_factory=lambda: datetime.now(UTC)
    )