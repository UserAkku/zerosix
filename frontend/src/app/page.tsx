"use client";

import React, { useState, useEffect } from "react";
import Header from "@/components/Header";
import AudioUploader from "@/components/AudioUploader";
import { analyzeAudio, checkHealth } from "@/lib/api";
import { AnalysisResponse, HealthResponse } from "@/lib/types";

// ... (keep rest unchanged)
// We will replace the return block below


export default function Home() {
  const [file, setFile] = useState<File | null>(null);
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<AnalysisResponse | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [health, setHealth] = useState<HealthResponse | null>(null);

  useEffect(() => {
    checkHealth().then(setHealth).catch(() => console.error("Backend offline"));
  }, []);

  const handleFile = async (selectedFile: File) => {
    setFile(selectedFile);
    setLoading(true);
    setError(null);
    setResult(null);

    try {
      const data = await analyzeAudio(selectedFile);
      setResult(data);
    } catch (err: any) {
      setError(err.message || "Something went wrong");
    } finally {
      setLoading(false);
    }
  };

  const getRiskColor = (level: string) => {
    switch (level) {
      case "LOW": return "text-green-500 border-green-500 stroke-green-500";
      case "MEDIUM": return "text-yellow-500 border-yellow-500 stroke-yellow-500";
      case "HIGH": return "text-orange-500 border-orange-500 stroke-orange-500";
      case "CRITICAL": return "text-red-500 border-red-500 stroke-red-500";
      default: return "text-gray-500 border-gray-500 stroke-gray-500";
    }
  };

  return (
    <div className="min-h-screen bg-white font-sans text-black selection:bg-black selection:text-white pb-20">
      <Header />
      
      <main className="pt-28 px-6 max-w-5xl mx-auto">
        <div className="text-center mb-12">
          <h1 className="text-4xl font-extrabold tracking-tight mb-4">Analyze Voice Authenticity</h1>
          <p className="text-gray-500 text-lg">Upload an audio file to detect AI generation or voice cloning.</p>
          
          {health && (
            <div className="mt-4 flex items-center justify-center gap-2 text-xs text-gray-400">
              <span className="w-2 h-2 rounded-full bg-green-500"></span>
              Backend Ready • {health.device.toUpperCase()} Accelerated • Mode: {health.model_mode}
            </div>
          )}
        </div>

        <AudioUploader onFileSelect={handleFile} isLoading={loading} />

        {error && (
          <div className="mt-8 p-4 bg-red-50 text-red-700 rounded-lg text-center font-medium">
            Error: {error}
          </div>
        )}

        {result && (
          <div className="mt-16 animate-in fade-in duration-500">
            {/* Top Stats Section */}
            <div className="grid md:grid-cols-2 gap-8 items-center mb-12">
              
              {/* Risk Gauge */}
              <div className="flex flex-col items-center justify-center p-8 rounded-2xl border border-gray-200">
                <div className="relative w-48 h-48 flex items-center justify-center">
                  <svg className="absolute inset-0 w-full h-full transform -rotate-90">
                    <circle cx="96" cy="96" r="88" fill="none" stroke="#f3f4f6" strokeWidth="12" />
                    <circle 
                      cx="96" cy="96" r="88" fill="none" 
                      className={`transition-all duration-1000 ease-out ${getRiskColor(result.risk_level)}`}
                      strokeWidth="12" strokeDasharray="552.9" 
                      strokeDashoffset={552.9 - (552.9 * result.risk_score) / 100} 
                      strokeLinecap="round"
                    />
                  </svg>
                  <div className="text-center flex flex-col items-center justify-center z-10">
                    <span className="text-6xl font-black tabular-nums tracking-tighter leading-none">
                      {result.risk_score}
                    </span>
                    <span className="text-sm font-bold text-gray-400 uppercase tracking-widest mt-2">
                      Score
                    </span>
                  </div>
                </div>
                
                <div className="mt-6 flex flex-col items-center gap-3">
                  <span className={`text-xl font-bold tracking-widest ${getRiskColor(result.risk_level).split(' ')[0]}`}>
                    {result.risk_level} RISK
                  </span>
                  <div className="flex items-center gap-2">
                    <span className="text-xs text-gray-500">Latency: {result.processing_time_ms}ms</span>
                  </div>
                </div>
              </div>

              {/* Spectrogram & Waveform */}
              <div className="flex flex-col gap-4">
                <div className="border border-gray-200 rounded-xl overflow-hidden bg-white p-1">
                  <p className="text-xs font-semibold text-gray-400 uppercase tracking-widest p-2">Mel-Spectrogram</p>
                  <img src={result.spectrogram_image} alt="Spectrogram" className="w-full h-32 object-fill rounded-lg filter contrast-125 grayscale" />
                </div>
                
                <div className="border border-gray-200 rounded-xl overflow-hidden bg-white p-1 h-24 flex flex-col">
                  <p className="text-xs font-semibold text-gray-400 uppercase tracking-widest p-2 pb-0">Waveform</p>
                  <div className="flex-1 flex items-center justify-between px-2 pb-2 gap-[1px]">
                    {result.waveform_data.map((val, i) => (
                      <div key={i} className="bg-black w-full rounded-full" style={{ height: `${Math.max(4, val * 100)}%` }}></div>
                    ))}
                  </div>
                </div>
              </div>
            </div>


            {/* Feature Breakdown Details */}
            <div>
              <h3 className="text-xl font-bold mb-6">Detection Analysis (Acoustic Fingerprint)</h3>
              <div className="grid md:grid-cols-2 gap-x-12 gap-y-6">
                <FeatureBar label="Pitch Variance (F0 Std)" value={result.details.f0_std ?? 0} max={60} anomaly={(result.details.f0_std ?? 0) > 20.0 && (result.details.f0_std ?? 0) < 35.0} formatter={(v) => (v || 0).toFixed(1) + " Hz"} />
                <FeatureBar label="Jitter (Micro-tremors)" value={result.details.jitter ?? 0} max={0.06} anomaly={result.details.jitter_status === "anomaly"} formatter={(v) => (v || 0).toFixed(4)} />
                <FeatureBar label="Shimmer (Amplitude Var)" value={result.details.shimmer ?? 0} max={0.15} anomaly={result.details.shimmer_status === "anomaly"} formatter={(v) => (v || 0).toFixed(4)} />
                <FeatureBar label="Harmonics-to-Noise (HNR)" value={result.details.hnr ?? 0} max={50} anomaly={result.details.hnr_status === "anomaly"} formatter={(v) => (v || 0).toFixed(1) + " dB"} />
                <FeatureBar label="Zero Crossing Rate (ZCR)" value={result.details.zcr ?? 0} max={0.15} anomaly={(result.details.zcr ?? 0) > 0.05 && (result.details.spectral_flatness ?? 0) < 0.015} formatter={(v) => (v || 0).toFixed(4)} />
                <FeatureBar label="Spectral Flatness" value={result.details.spectral_flatness ?? 0} max={0.05} anomaly={(result.details.zcr ?? 0) > 0.05 && (result.details.spectral_flatness ?? 0) < 0.015} formatter={(v) => (v || 0).toFixed(5)} />
                <FeatureBar label="Spectral Rolloff" value={result.details.spectral_rolloff ?? 0} max={8000} anomaly={(result.details.spectral_rolloff ?? 0) > 0 && (result.details.spectral_rolloff ?? 0) < 3500} formatter={(v) => (v || 0).toFixed(0) + " Hz"} />
                <FeatureBar label="Spectral Bandwidth" value={result.details.spectral_bandwidth ?? 0} max={4000} anomaly={(result.details.spectral_bandwidth ?? 0) > 0 && (result.details.spectral_bandwidth ?? 0) < 1800} formatter={(v) => (v || 0).toFixed(0) + " Hz"} />
                
                {result.details.retroflex_score != null && (
                   <FeatureBar label="Retroflex Consonant Quality" value={result.details.retroflex_score} max={1} anomaly={result.details.retroflex_anomaly || false} formatter={(v) => v.toFixed(2)} />
                )}
                {result.details.code_switch_score != null && (
                   <FeatureBar label="Code-Switch Anomaly" value={result.details.code_switch_score} max={1} anomaly={result.details.code_switch_anomaly || false} formatter={(v) => v.toFixed(2)} />
                )}
              </div>
            </div>

          </div>
        )}
      </main>
    </div>
  );
}

function FeatureBar({ label, value, max, anomaly, formatter }: { label: string, value: number, max: number, anomaly: boolean, formatter: (v: number) => string }) {
  const percentage = Math.min(100, (value / max) * 100);
  return (
    <div className="flex flex-col gap-2">
      <div className="flex justify-between items-end">
        <span className="font-medium text-sm">{label}</span>
        <div className="flex items-center gap-2">
          {anomaly && <span className="text-[10px] uppercase font-bold tracking-wider text-red-500 bg-red-50 px-2 py-0.5 rounded">Anomaly</span>}
          {!anomaly && <span className="text-[10px] uppercase font-bold tracking-wider text-green-600 bg-green-50 px-2 py-0.5 rounded">Normal</span>}
          <span className="text-sm font-mono text-gray-500">{formatter(value)}</span>
        </div>
      </div>
      <div className="h-2 w-full bg-gray-100 rounded-full overflow-hidden">
        <div className={`h-full rounded-full ${anomaly ? "bg-red-500" : "bg-black"}`} style={{ width: `${percentage}%` }}></div>
      </div>
    </div>
  );
}
