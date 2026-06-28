from fastapi import APIRouter, HTTPException

from app.models.request_models import PromptRequest,YoutubeRequest
from app.services.groq_services import GroqService
from app.services.youtube_service import YouTubeService
from app.services.summarization_service import SummarizationService


from app.exceptions import (
    GroqException,
    InvalidYouTubeUrlException,
    TranscriptNotFoundException,
)

router = APIRouter()


youtube_service = YouTubeService()
groq_service = GroqService()
summarization_service = SummarizationService()

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

    except Exception:
        raise HTTPException(
            status_code=500,
            detail="Internal Server Error"
        )

@router.post("/summarize")
def summarize(request: YoutubeRequest):

    try:
        response = summarization_service.summarize(
            str(request.youtube_url)
        )

        return {
            "response": response
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

    except GroqException as e:
        raise HTTPException(
            status_code=502,
            detail=str(e)
        )

    except Exception:
        raise HTTPException(
            status_code=500,
            detail="Internal Server Error"
        )