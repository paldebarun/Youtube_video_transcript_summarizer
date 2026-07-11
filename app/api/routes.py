from fastapi import APIRouter, HTTPException

from models.request_models import PromptRequest,YoutubeRequest
from services.groq_services import GroqService
from services.transcript_service import TranscriptService
# from services.summarization_service import SummarizationService
from services.task_service import TaskService

from exceptions import (
    GroqException,
    InvalidYouTubeUrlException,
    TranscriptNotFoundException,
    VisionException
)

router = APIRouter()


youtube_service = TranscriptService()
groq_service = GroqService()
# summarization_service = SummarizationService()
task_service = TaskService()
from models.task_document import ServiceStatus

@router.get("/health")
def health():
    return {
        "status": "healthy",
        "service": "YouTube AI Summarizer Backend"
    }


@router.post("/generate")
def generate(request: PromptRequest):

    try:
        response = groq_service.generate(request.prompt)

        return {
            "response": response
        }

    except GroqException as e:
        raise HTTPException(
            status_code=502,
            detail=str(e)
        )



@router.post("/transcript")
def transcript(request: YoutubeRequest):

    try:

        transcript = youtube_service.get_transcript(
            str(request.youtube_url)
        )

        return {
            "transcript": transcript
        }

    except InvalidYouTubeUrlException as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )

    except TranscriptNotFoundException as e:
        raise HTTPException(
            status_code=404,
            detail=str(e)
        )
    
    except VisionException as e:
        raise HTTPException(
            status_code=502,
            detail=str(e),
        )

    except Exception:
        raise HTTPException(
            status_code=500,
            detail="Internal Server Error"
        )

# @router.post("/summarize")
# def summarize(request: YoutubeRequest):

#     try:
#         return summarization_service.summarize(
#         str(request.youtube_url)
# )

#     except InvalidYouTubeUrlException as e:
#         raise HTTPException(
#             status_code=400,
#             detail=str(e)
#         )

#     except TranscriptNotFoundException as e:
#         raise HTTPException(
#             status_code=404,
#             detail=str(e)
#         )
    
#     except VisionException as e:
#         raise HTTPException(
#             status_code=502,
#             detail=str(e),
#         )

#     except GroqException as e:
#         raise HTTPException(
#             status_code=502,
#             detail=str(e)
#         )

#     except Exception:
#         raise HTTPException(
#             status_code=500,
#             detail="Internal Server Error"
#         )

@router.post("/summarize")
def summarize(request: YoutubeRequest):

    task = task_service.create_task(
        str(request.youtube_url)
    )

    return {
        "task_id": task.id,
        "status": "QUEUED",
    }