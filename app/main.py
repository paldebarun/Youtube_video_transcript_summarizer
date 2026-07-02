from fastapi import FastAPI
import uvicorn

from api.routes import router

app = FastAPI(
    title="YouTube AI Summarizer",
    version="1.0.0"
)

app.include_router(router)


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
    )