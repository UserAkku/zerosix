import time
from fastapi import APIRouter, UploadFile, File, HTTPException
from .schemas import AnalysisResponse, HealthResponse, DetectionDetails
from ..core import preprocessor, feature_extractor, model_inference, risk_scorer

router = APIRouter()

@router.get("/health", response_model=HealthResponse)
def health_check():
    detector = model_inference.get_detector()
    return HealthResponse(
        status="healthy",
        model_loaded=True,
        model_mode=detector.mode,
        device="mps",  # Defaulting as per plan
        version="1.0.0"
    )

@router.post("/analyze", response_model=AnalysisResponse)
async def analyze_audio(file: UploadFile = File(...)):
    if not file.filename.endswith(('.wav', '.mp3', '.ogg', '.m4a', '.webm')):
        raise HTTPException(status_code=400, detail="Unsupported file format.")
        
    start_time = time.time()
    
    try:
        # Read file
        audio_bytes = await file.read()
        
        # 1. Preprocess
        clean_audio, sr = preprocessor.preprocess_file(audio_bytes)
        
        # 2. Extract Features
        features = feature_extractor.extract_all(clean_audio, sr)
        
        # 3. Model Inference
        detector = model_inference.get_detector()
        model_score = detector.predict(clean_audio, features)
        
        # 4. Mock Language Detection (MVP)
        # Ideally, we would detect language here. We'll default to hindi.
        language = "hindi"
        if "english" in file.filename.lower():
            language = "english"
        elif "hinglish" in file.filename.lower():
            language = "hinglish"
            
        # 5. Risk Scoring
        risk_result = risk_scorer.calculate_risk(model_score, features, language)
        
        # Format details
        details = DetectionDetails(**risk_result.pop("details"))
        
        processing_time_ms = int((time.time() - start_time) * 1000)
        
        return AnalysisResponse(
            **risk_result,
            processing_time_ms=processing_time_ms,
            details=details,
            spectrogram_image=features["spectrogram_image"],
            waveform_data=features["waveform_data"]
        )
        
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")
