from fastapi import APIRouter, HTTPException

from app.models.request_models import VideoRequest
from app.services.groq_services import GroqService

from app.services.task_service import TaskService




router = APIRouter()



groq_service = GroqService()

task_service = TaskService()

@router.get("/health")
def health():
    return {
        "status": "healthy",
        "service": "Video summarizer Service"
    }





@router.post("/summarize")
def summarize(request: VideoRequest):

    task_id = task_service.create_task(
    request.source,
    request.value,
)

    return {
        "task_id": task_id,
        "status": "QUEUED",
    }



@router.get("/tasks/{task_id}")
def get_task(
    task_id: str,
):
    try:

        task = task_service.get_task(
            task_id,
        )

        return task

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e),
        )

