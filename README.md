# 🛡️ VoiceShield — Real-Time AI Voice Clone Detection

**By Team Zerosix**  
*Built for Smart India Hackathon (SIH) 2026*

VoiceShield is an advanced, real-time Deepfake and AI Voice Clone detection system. It analyzes the **physical acoustic properties** of a voice rather than just its pitch, allowing it to catch highly sophisticated synthetic voices (like ElevenLabs, XTTS, etc.) that easily bypass traditional detectors.

---

## 🚀 The Core Innovation: Acoustic Fingerprinting
Modern AI text-to-speech models can perfectly mimic human tone and pitch, but they struggle to replicate the physics of the human vocal tract. VoiceShield catches these flaws using a **Multi-Variate Correlation Matrix**:

1. **Phase-Vocoder Trap (HNR):** AI synthesizers mess up phase reconstruction, causing extreme negative Harmonics-to-Noise Ratios (HNR) even when audio sounds perfectly clear.
2. **Synthetic Fricatives:** We detect physically impossible mismatches, like high Zero-Crossing Rates (ZCR) combined with low Spectral Flatness.
3. **Micro-Tremor Analysis:** We analyze Jitter and Shimmer to catch the "unnaturally smooth" generation signatures of AI models.
4. **Bandwidth Loss:** Identifies 24kHz synthesis capping commonly used in real-time AI processing.

---

## 🛠️ Tech Stack
* **Frontend:** Next.js (React, TypeScript, Tailwind CSS)
* **Backend:** FastAPI (Python)
* **DSP & ML:** PyTorch, Librosa, NumPy
* **Deployment Readiness:** Dockerized for Edge/Cloud (Hugging Face Spaces), Vercel

---

## 💻 Local Setup Instructions

### 1. Run the Backend (FastAPI)
The backend extracts 48-dimensional features (including MFCCs) and runs our deterministic risk-scoring engine.

```bash
# Navigate to the project root
cd zerosix

# Activate the virtual environment
source backend/venv/bin/activate

# Install dependencies (if not already installed)
pip install -r backend/requirements.txt

# Start the server
uvicorn backend.main:app --reload
```
*The API will be available at `http://localhost:8000`*

### 2. Run the Frontend (Next.js Dashboard)
The transparent analytics dashboard provides a detailed breakdown of the exact acoustic anomalies detected.

```bash
# Open a new terminal and navigate to the frontend directory
cd zerosix/frontend

# Install dependencies
npm install

# Start the development server
npm run dev
```
*The UI will be available at `http://localhost:3000`*

---

## 🌐 Deployment (Hackathon Ready)
* **Backend:** Contains a `Dockerfile` pre-configured with `libsndfile` and `ffmpeg` system dependencies. Ready for 1-click deployment on **Hugging Face Spaces** (Docker environment).
* **Frontend:** Ready for zero-config deployment on **Vercel**. Ensure you set the `NEXT_PUBLIC_API_URL` environment variable to your deployed backend URL.

---

*Secure the voice. Protect the trust.*
