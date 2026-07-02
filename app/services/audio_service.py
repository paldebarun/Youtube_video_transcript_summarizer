from pathlib import Path
import uuid

from yt_dlp import YoutubeDL

from exceptions import AudioDownloadException


class AudioService:

    def __init__(self):
        self.output_dir = Path("downloads")
        self.output_dir.mkdir(exist_ok=True)

    def download_audio(self, youtube_url: str) -> str:

        file_name = str(uuid.uuid4())

        output_template = str(
            self.output_dir / f"{file_name}.%(ext)s"
        )

        options = {
            "format": "bestaudio/best",
            "outtmpl": output_template,
            "quiet": True,
            "noplaylist": True,
            "postprocessors": [
                {
                    "key": "FFmpegExtractAudio",
                    "preferredcodec": "mp3",
                    "preferredquality": "192",
                }
            ],
        }

        try:

            with YoutubeDL(options) as ydl:
                ydl.download([youtube_url])

            return str(
                self.output_dir / f"{file_name}.mp3"
            )

        except Exception as e:
            raise AudioDownloadException(
                "Failed to download YouTube audio."
            ) from e

    def delete_audio(self, file_path: str):

        path = Path(file_path)

        if path.exists():
            path.unlink()