from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.controllers import health_controller, transcription_controller
from app.middleware.logging_middleware import LoggingMiddleware
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('app.log'),
        logging.StreamHandler()
    ]
)

app = FastAPI(
    title="Whisper Transcription API",
    description="OpenAI Whisper kullanarak ses-metin dönüştürme API'si",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(LoggingMiddleware)

app.include_router(
    health_controller.router,
    prefix="/api/v1",
    tags=["Health"]
)

app.include_router(
    transcription_controller.router,
    prefix="/api/v1",
    tags=["Transcription"]
)

@app.get("/")
async def root():
    return {
        "message": "Whisper Transcription API",
        "version": "1.0.0",
        "status": "running"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
