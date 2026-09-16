from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import logging

from backend.api.routes import router
from backend.core.config import CORS_ORIGINS
from backend.core.model_inference import get_detector

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="VoiceShield API",
    description="Real-time AI Voice Clone Detection (Hindi & English)",
    version="1.0.0"
)

# Set up CORS for Hackathon Deployment (Allow All)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup_event():
    logger.info("Starting up VoiceShield API...")
    # Initialize the ML model detector
    detector = get_detector()
    logger.info(f"Detector initialized in {detector.mode} mode.")

# Include routers
app.include_router(router, prefix="/api")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("backend.main:app", host="0.0.0.0", port=8000, reload=True)
