from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI

from app.api.routes import router

from app.config import PORT

from app.utils.logger import Logger
from app.utils.supervisor_manager import SupervisorManager


logger = Logger.get_logger()

supervisor = SupervisorManager()


@asynccontextmanager
async def lifespan(app: FastAPI):

    try:

        logger.info(
            "Starting Video summarizer..."
        )

        supervisor.generate_config()

        supervisor.start()

        logger.info(
            "Supervisor started successfully."
        )

        yield

    finally:

        logger.info(
            "Stopping Video summarizer..."
        )

        supervisor.stop()

        logger.info(
            "Supervisor stopped successfully."
        )


app = FastAPI(
    title="Video summarizer Service",
    version="1.0.0",
    lifespan=lifespan,
)

app.include_router(router)


if __name__ == "__main__":

    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=PORT,
        reload=True,
    )