from app.services.youtube_service import YouTubeService
from app.services.groq_services import GroqService
from app.prompts import summarization_prompt

class SummarizationService:

    def __init__(self):
        self.youtube_service = YouTubeService()
        self.groq_service = GroqService()

    def summarize(self, youtube_url: str):

        transcript = self.youtube_service.get_transcript(youtube_url)

        prompt = summarization_prompt(transcript)

        return self.groq_service.generate(prompt)
     