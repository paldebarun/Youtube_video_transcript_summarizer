from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI

from api.routes import router

from config import PORT

from utils.logger import Logger
from utils.supervisor_manager import SupervisorManager


logger = Logger.get_logger()

supervisor = SupervisorManager()


@asynccontextmanager
async def lifespan(app: FastAPI):

    try:

        logger.info(
            "Starting YouTube AI Summarizer..."
        )

        supervisor.generate_config()

        supervisor.start()

        logger.info(
            "Supervisor started successfully."
        )

        yield

    finally:

        logger.info(
            "Stopping YouTube AI Summarizer..."
        )

        supervisor.stop()

        logger.info(
            "Supervisor stopped successfully."
        )


app = FastAPI(
    title="YouTube AI Summarizer",
    version="1.0.0",
    lifespan=lifespan,
)

app.include_router(router)


if __name__ == "__main__":

    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=PORT,
        reload=True,
    )