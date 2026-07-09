from datetime import datetime

from pydantic import BaseModel


class EventModel(BaseModel):

    task_id: str

    event_type: str

    service: str

    status: str

    payload: dict

    timestamp: datetime