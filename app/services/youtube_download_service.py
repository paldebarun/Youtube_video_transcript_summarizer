from pathlib import Path
import uuid

from yt_dlp import YoutubeDL

from config import DOWNLOAD_DIR
from exceptions import VideoDownloadException


class YouTubeDownloadService:

    def __init__(self):

        self.download_dir = DOWNLOAD_DIR
        self.download_dir.mkdir(
            parents=True,
            exist_ok=True,
        )

    def download(
        self,
        youtube_url: str,
    ) -> Path:

        file_name = str(uuid.uuid4())

        output_template = str(
            self.download_dir / f"{file_name}.%(ext)s"
        )

        options = {
            "format": "bestvideo+bestaudio/best",
            "merge_output_format": "mp4",
            "outtmpl": output_template,
            "quiet": True,
            "noplaylist": True,
        }

        try:

            with YoutubeDL(options) as ydl:
                ydl.download([youtube_url])

            return self.download_dir / f"{file_name}.mp4"

        except Exception as e:

            raise VideoDownloadException(
                "Failed to download YouTube video."
            ) from e

    def delete_video(
        self,
        video_path: Path,
    ):

        if video_path.exists():
            video_path.unlink()