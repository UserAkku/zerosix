# 🛡️ VoiceShield — Real-Time AI Voice Clone Detection (SIH 2026)

**Team Zerosix** | **Problem Statement ID:** 26104 (AICTE Cyber Security Cell) | **Theme:** Blockchain & Cybersecurity

![VoiceShield Dashboard Preview](https://img.shields.io/badge/Status-Prototype_Ready-success) ![License](https://img.shields.io/badge/License-MIT-blue)

VoiceShield is an advanced Deepfake and AI Voice Clone detection system designed to operate in real-time. Instead of relying on black-box machine learning models that can be easily fooled by newer AI generators, VoiceShield analyzes the **physical acoustic properties (Acoustic Fingerprint)** of an audio signal to catch sophisticated synthetic voices (e.g., ElevenLabs, Coqui XTTS) that bypass traditional detectors.

---

## 🚀 The Vision vs. Current Prototype

### 🔮 The Complete Solution (Vision)
Our ultimate solution is a **C++ / Python SDK** designed to be integrated directly into Telecom Operator networks (Jio, Airtel) or VoIP applications (WhatsApp, Zoom). 
- It intercepts active call audio streams.
- Runs a lightweight, highly optimized ONNX model on the edge.
- Flashes a real-time "Deepfake Warning" to the user if the caller's voice is synthetic.

### 💻 The Current Prototype (This Repository)
For the SIH Prototype, we have built a fully functional **Web-Based Simulation Dashboard** that mimics the Telecom Intercept capability:
- **FastAPI Backend:** Acts as the deepfake detection engine, exposing a REST API. It extracts 48-dimensional acoustic features directly from raw audio bytes.
- **Deterministic DSP Engine:** We implemented a SOTA (State-of-the-Art) Multi-Variate Correlation Matrix that flags anomalies based on acoustic physics.
- **Next.js Frontend:** A transparent analytics dashboard that not only provides a Risk Score (0-100) but also shows the exact DSP metrics causing the anomaly, proving the system is not a black box.

---

## 🧠 Core Innovation: The "Acoustic Fingerprint"
Modern Text-to-Speech (TTS) models can perfectly mimic a human's tone, pitch, and accent, but they fail to replicate the microscopic physics of the human vocal tract. VoiceShield targets these specific flaws:

1. **Phase-Vocoder Trap (HNR Anomaly):** AI synthesizers (like HiFi-GAN) mathematically guess audio phase, causing the Harmonics-to-Noise Ratio (HNR) to drop into extreme negatives (-20dB to -40dB), even when the audio sounds perfectly clear to human ears.
2. **Synthetic Fricatives (ZCR vs. Flatness):** When humans say "S" or "Sh", it creates chaotic wind noise (High Zero-Crossing Rate + High Spectral Flatness). AI mathematically generates High ZCR to trick our ears, but fails to generate true chaotic wind (Low Flatness). We flag this physical impossibility.
3. **Micro-Tremor Analysis:** AI voices are often mathematically "too perfect". We analyze pitch micro-tremors (Jitter) and amplitude variations (Shimmer) to catch unnaturally smooth generation signatures.

---

## 🛠️ Technology Stack
* **Signal Processing:** `Librosa`, `NumPy`, `Soundfile` (DSP Feature Extraction)
* **Backend API:** `FastAPI`, `Uvicorn`, `Python 3.10+`
* **Frontend:** `Next.js 14`, `React`, `TypeScript`, `Tailwind CSS`

---

## ⚙️ Local Setup Instructions (For Judges & Testing)

This project is optimized to run locally on your machine for the best performance and zero latency during demos.

### Prerequisites
- Python 3.10 or higher
- Node.js 18 or higher
- `ffmpeg` (Required for Librosa audio decoding)
  - *Mac:* `brew install ffmpeg`
  - *Windows:* Download via `winget install ffmpeg`

### 1️⃣ Start the Backend Engine (FastAPI)
Open your terminal and run the following commands:
```bash
# 1. Clone the repository and enter the directory
git clone https://github.com/YOUR_USERNAME/zerosix.git
cd zerosix

# 2. Create and activate a virtual environment
python3 -m venv backend/venv
source backend/venv/bin/activate  # On Windows use: backend\venv\Scripts\activate

# 3. Install the required dependencies
pip install -r backend/requirements.txt

# 4. Run the API Server
uvicorn backend.main:app --reload --port 8000
```
*(The backend is now running and listening on `http://127.0.0.1:8000`)*

### 2️⃣ Start the Analytics Dashboard (Next.js)
Open a **new, separate terminal tab** and run:
```bash
# 1. Enter the frontend directory
cd zerosix/frontend

# 2. Install Node modules
npm install

# 3. Start the development server
npm run dev
```
*(The frontend is now running on `http://localhost:3000`)*

---

## 🧪 Demo & Testing Guide (For Evaluators)
1. Open your browser and go to `http://localhost:3000`.
2. **Test a Real Human Voice:** Record your own voice or upload a standard recording (use `.wav` for best compatibility). The dashboard will show natural acoustic metrics (Positive HNR, normal Jitter) and yield a **LOW RISK** score.
3. **Test a Deepfake (ElevenLabs/XTTS):** Upload an AI-generated audio file. The dashboard will instantly detect the synthetic phase artifacts, highlight the specific anomalies in **RED** (e.g., HNR -27dB, Jitter < 0.035), and yield a **CRITICAL RISK** score.

---

## ⚠️ Troubleshooting & Common Evaluator Issues

If you are setting this up on a fresh machine to evaluate our project, please ensure the following:

**1. `audioread.NoBackendError` or File Upload Fails**
- **Cause:** Our backend uses `librosa` to analyze microscopic audio frequencies. Librosa requires the system-level `ffmpeg` library to decode `.mp3` or `.m4a` files.
- **Fix (Mac):** Run `brew install ffmpeg` in your terminal.
- **Fix (Windows):** Run `winget install ffmpeg` in PowerShell, or download it from the official site.
- **Quick Bypass:** If you don't want to install `ffmpeg`, simply upload **`.wav`** files! Our system can process raw `.wav` files natively without `ffmpeg`.

**2. Node Modules Error**
- **Cause:** Missing frontend dependencies.
- **Fix:** Ensure you run `npm install` inside the `frontend/` directory before running `npm run dev`.

**3. Port 8000 Already in Use**
- **Cause:** Another application is using the backend port.
- **Fix:** Run the backend on a different port: `uvicorn backend.main:app --reload --port 8080`, and update the `.env.local` file in the frontend directory with `NEXT_PUBLIC_API_URL=http://127.0.0.1:8080`.

---
*Developed with ❤️ by Team Zerosix for a secure digital India.*
