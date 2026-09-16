from pydantic import BaseModel
from typing import Optional, List, Dict

class DetectionDetails(BaseModel):
    model_score: float
    model_mode: str
    jitter: float
    jitter_status: str
    shimmer: float
    shimmer_status: str
    hnr: float
    hnr_status: str
    speaking_rate: float
    f0_mean: float
    f0_std: float
    spectral_rolloff: float
    spectral_centroid: float
    spectral_bandwidth: float
    zcr: float
    spectral_flatness: float
    retroflex_score: Optional[float] = None
    retroflex_anomaly: Optional[bool] = None
    code_switch_score: Optional[float] = None
    code_switch_anomaly: Optional[bool] = None

class AnalysisResponse(BaseModel):
    risk_score: int
    risk_level: str
    language_detected: str
    language_confidence: float
    confidence: float
    recommendation: str
    processing_time_ms: int
    details: DetectionDetails
    spectrogram_image: str
    waveform_data: List[float]

class HealthResponse(BaseModel):
    status: str
    model_loaded: bool
    model_mode: str
    device: str
    version: str
