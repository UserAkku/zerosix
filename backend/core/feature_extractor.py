import numpy as np
import librosa
import matplotlib.pyplot as plt
import io
import base64

def extract_mfcc(audio, sr, n_mfcc=13):
    """Extract MFCC features."""
    return librosa.feature.mfcc(y=audio, sr=sr, n_mfcc=n_mfcc)

def extract_mel_spectrogram(audio, sr, n_mels=80):
    """Extract Mel-Spectrogram and convert to dB scale."""
    S = librosa.feature.melspectrogram(y=audio, sr=sr, n_mels=n_mels)
    S_dB = librosa.power_to_db(S, ref=np.max)
    return S_dB

def extract_f0(audio, sr):
    """Extract fundamental frequency (pitch)."""
    f0, _, _ = librosa.pyin(audio, fmin=60, fmax=400, sr=sr)
    return f0

def compute_jitter(f0):
    """Compute local jitter (cycle-to-cycle F0 variation)."""
    f0_clean = f0[~np.isnan(f0)]
    if len(f0_clean) < 2:
        return 0.0
    diffs = np.abs(np.diff(f0_clean))
    mean_f0 = np.mean(f0_clean)
    if mean_f0 == 0:
        return 0.0
    return float(np.mean(diffs) / mean_f0)

def compute_shimmer(audio, sr):
    """Compute shimmer (amplitude variation). Simplified frame-level."""
    frame_length = int(sr * 0.02) # 20ms
    hop_length = int(sr * 0.01) # 10ms
    rms = librosa.feature.rms(y=audio, frame_length=frame_length, hop_length=hop_length)[0]
    rms_clean = rms[rms > 0.001]
    if len(rms_clean) < 2:
        return 0.0
    diffs = np.abs(np.diff(rms_clean))
    mean_rms = np.mean(rms_clean)
    return float(np.mean(diffs) / mean_rms) if mean_rms > 0 else 0.0

def compute_hnr(audio, sr):
    """Estimate Harmonics-to-Noise Ratio (HNR)."""
    # Simplified HNR using harmonics/percussive separation
    y_harmonic, y_percussive = librosa.effects.hpss(audio)
    h_energy = np.sum(y_harmonic**2)
    p_energy = np.sum(y_percussive**2)
    if p_energy == 0:
        return 50.0 # Max typical HNR
    hnr_db = 10 * np.log10(h_energy / p_energy)
    return float(hnr_db)

def compute_speaking_rate(audio, sr):
    """Estimate syllables per second."""
    onset_env = librosa.onset.onset_strength(y=audio, sr=sr)
    peaks = librosa.util.peak_pick(onset_env, pre_max=3, post_max=3, pre_avg=3, post_avg=5, delta=0.5, wait=10)
    duration = len(audio) / sr
    return float(len(peaks) / duration) if duration > 0 else 0.0

def generate_spectrogram_image(mel_spec):
    """Generate a base64 encoded grayscale spectrogram image."""
    plt.figure(figsize=(6, 3))
    librosa.display.specshow(mel_spec, cmap='gray_r')
    plt.tight_layout(pad=0)
    
    buf = io.BytesIO()
    plt.savefig(buf, format='png', bbox_inches='tight', pad_inches=0)
    plt.close()
    
    buf.seek(0)
    b64_string = base64.b64encode(buf.read()).decode('utf-8')
    return f"data:image/png;base64,{b64_string}"

def generate_waveform_data(audio, target_length=200):
    """Downsample audio to a fixed length array for UI visualization."""
    if len(audio) <= target_length:
        return audio.tolist()
    
    # Simple windowed max pooling for visualization
    window_size = len(audio) // target_length
    downsampled = [float(np.max(np.abs(audio[i*window_size:(i+1)*window_size]))) for i in range(target_length)]
    return downsampled

def compute_spectral_features(audio, sr):
    """Compute Spectral Centroid, Rolloff, ZCR, Flatness, and Bandwidth for Deep Learning."""
    centroid = librosa.feature.spectral_centroid(y=audio, sr=sr)[0]
    rolloff = librosa.feature.spectral_rolloff(y=audio, sr=sr, roll_percent=0.85)[0]
    zcr = librosa.feature.zero_crossing_rate(audio)[0]
    flatness = librosa.feature.spectral_flatness(y=audio)[0]
    bandwidth = librosa.feature.spectral_bandwidth(y=audio, sr=sr)[0]
    
    return (
        float(np.mean(centroid)), float(np.mean(rolloff)), float(np.mean(zcr)),
        float(np.mean(flatness)), float(np.mean(bandwidth))
    )

def extract_all(audio, sr):
    """Extract all features required for detection."""
    mel_spec = extract_mel_spectrogram(audio, sr)
    f0 = extract_f0(audio, sr)
    f0_clean = f0[~np.isnan(f0)]
    
    # Advanced Spectral Features
    cen, ro, zcr, flat, bw = compute_spectral_features(audio, sr)
    
    # Advanced MFCC Features (20 Mean + 20 Std = 40 Features for DNN)
    mfccs = librosa.feature.mfcc(y=audio, sr=sr, n_mfcc=20)
    mfcc_mean = np.mean(mfccs, axis=1).tolist()
    mfcc_std = np.std(mfccs, axis=1).tolist()
    
    return {
        "mel_spec": mel_spec,
        "f0_mean": float(np.mean(f0_clean)) if len(f0_clean) > 0 else 0.0,
        "f0_std": float(np.std(f0_clean)) if len(f0_clean) > 0 else 0.0,
        "jitter": compute_jitter(f0),
        "shimmer": compute_shimmer(audio, sr),
        "hnr": compute_hnr(audio, sr),
        "speaking_rate": compute_speaking_rate(audio, sr),
        "spectral_centroid": cen,
        "spectral_rolloff": ro,
        "zcr": zcr,
        "spectral_flatness": flat,
        "spectral_bandwidth": bw,
        "mfcc_mean": mfcc_mean,
        "mfcc_std": mfcc_std,
        "spectrogram_image": generate_spectrogram_image(mel_spec),
        "waveform_data": generate_waveform_data(audio)
    }
