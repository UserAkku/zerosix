import io
import os
import tempfile
import numpy as np
import librosa
import soundfile as sf
from . import config

def load_audio(file_path_or_bytes):
    """
    Load audio from a file path or raw bytes.
    Returns: audio array and sample rate.
    """
    if isinstance(file_path_or_bytes, bytes):
        # librosa (via audioread/ffmpeg) cannot decode webm/m4a directly from BytesIO.
        # We must write it to a temporary file first.
        with tempfile.NamedTemporaryFile(delete=False, suffix=".tmp") as tmp:
            tmp.write(file_path_or_bytes)
            tmp_path = tmp.name
            
        try:
            # sr=None preserves the original sample rate (Crucial for detecting AI 24kHz caps vs Real 48kHz)
            audio, sr = librosa.load(tmp_path, sr=None, mono=False)
        finally:
            if os.path.exists(tmp_path):
                os.remove(tmp_path)
    else:
        audio, sr = librosa.load(file_path_or_bytes, sr=None, mono=False)
        
    return audio, sr

def to_mono(audio):
    """Convert stereo to mono."""
    if audio.ndim > 1:
        return librosa.to_mono(audio)
    return audio

def normalize(audio):
    """Peak normalize audio to [-1, 1]."""
    max_val = np.max(np.abs(audio))
    if max_val > 0:
        return audio / max_val
    return audio

def trim_silence(audio):
    """Trim leading and trailing silence so averages (ZCR, Flatness) aren't diluted."""
    audio_trimmed, _ = librosa.effects.trim(audio, top_db=30)
    return audio_trimmed

def preprocess_file(file_path_or_bytes):
    """
    Full pipeline: load -> mono -> trim silence -> normalize.
    Preserves original length and sample rate for maximum forensic accuracy.
    """
    audio, sr = load_audio(file_path_or_bytes)
    audio = to_mono(audio)
    audio = trim_silence(audio)
    audio = normalize(audio)
    return audio, sr
