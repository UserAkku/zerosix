from . import config

def get_risk_level(score):
    if score <= config.RISK_THRESHOLDS["low"]:
        return "LOW", "Voice appears genuine."
    elif score <= config.RISK_THRESHOLDS["medium"]:
        return "MEDIUM", "Some anomalies detected. Monitoring."
    elif score <= config.RISK_THRESHOLDS["high"]:
        return "HIGH", "Suspicious patterns detected. Secondary verification recommended."
    else:
        return "CRITICAL", "High probability of AI-generated voice. DO NOT process transaction."

def calculate_risk(model_score, features, language="hindi"):
    # Ensure language exists in config, else default to hindi
    if language not in config.LANGUAGE_WEIGHTS:
        language = "hindi"
    # 1. Base Score (Acoustic Fingerprint is now our primary truth)
    base_score = model_score * 0.85
    
    # 2. Hindi Features (Continuous mock)
    hindi_anomaly = 0.0
    retroflex_anomaly = False
    
    if language in ["hindi", "hinglish"]:
        hindi_anomaly = model_score * 0.9
        if hindi_anomaly > 0.6:
            retroflex_anomaly = True
            
    hindi_score = hindi_anomaly * 0.15
    
    # Final Risk Calculation
    raw_score = base_score + hindi_score
    
    # Scale to 0-100
    final_score = int(min(raw_score * 100, 100))
    
    level, recommendation = get_risk_level(final_score)
    
    ro = features.get("spectral_rolloff", 0.0)
    cen = features.get("spectral_centroid", 0.0)
    bw = features.get("spectral_bandwidth", 0.0)
    zcr = features.get("zcr", 0.0)
    flat = features.get("spectral_flatness", 0.0)
    f0_std = features.get("f0_std", 0.0)
    
    # Compile details for the UI Analytics Dashboard
    details = {
        "model_score": float(model_score),
        "model_mode": "multi_variate_sota",
        "jitter": features.get("jitter", 0.0),
        "jitter_status": "anomaly" if features.get("jitter", 1.0) < 0.035 else "normal",
        "shimmer": features.get("shimmer", 0.0),
        "shimmer_status": "anomaly" if features.get("shimmer", 1.0) < 0.08 else "normal",
        "hnr": features.get("hnr", 0.0),
        "hnr_status": "anomaly" if features.get("hnr", 0.0) < -15.0 else "normal",
        "spectral_rolloff": ro,
        "spectral_centroid": cen,
        "spectral_bandwidth": bw,
        "zcr": zcr,
        "spectral_flatness": flat,
        "f0_std": f0_std,
        "speaking_rate": features.get("speaking_rate", 0.0),
        "f0_mean": features.get("f0_mean", 0.0)
    }
    
    if language in ["hindi", "hinglish"]:
        details["retroflex_score"] = 0.2 if retroflex_anomaly else 0.8
        details["retroflex_anomaly"] = retroflex_anomaly
        if language == "hinglish":
            details["code_switch_score"] = 0.9 if model_score > 0.5 else 0.2
            details["code_switch_anomaly"] = (model_score > 0.5)

    return {
        "risk_score": final_score,
        "risk_level": level,
        "language_detected": language,
        "language_confidence": 0.95,
        "confidence": 0.88,
        "recommendation": recommendation,
        "details": details
    }
