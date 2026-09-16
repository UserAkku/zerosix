import os

# Server
HOST = "0.0.0.0"
PORT = 8000
CORS_ORIGINS = ["http://localhost:3000"]

# Audio Settings
SAMPLE_RATE = 16000
CHUNK_DURATION = 4.0  # seconds

# Model & Device
DEVICE = "mps"  # Apple Silicon (M1/M2/M3) acceleration
MODEL_DIR = os.path.join(os.path.dirname(__file__), "../models")

# Risk Scoring
RISK_THRESHOLDS = {
    "low": 30,
    "medium": 50,
    "high": 70,
    "critical": 80
}

# Language-specific weights (model, prosody, hindi_features)
LANGUAGE_WEIGHTS = {
    "hindi": {"model": 0.40, "prosody": 0.35, "hindi_features": 0.25},
    "english": {"model": 0.50, "prosody": 0.30, "hindi_features": 0.20},
    "hinglish": {"model": 0.30, "prosody": 0.35, "hindi_features": 0.35}
}

EMA_LAMBDA = 0.3  # Temporal smoothing

# Prosody Normal Ranges (for fallback and prosody scoring)
PROSODY_THRESHOLDS = {
    "jitter_normal": (0.008, 0.015),
    "shimmer_normal": (0.02, 0.05),
    "hnr_normal": (15, 35)
}
