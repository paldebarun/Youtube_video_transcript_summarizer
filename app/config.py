from dotenv import load_dotenv
import os

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
WHISPER_SERVICE_URL = os.getenv(
    "WHISPER_SERVICE_URL",
    "http://localhost:2000",
)