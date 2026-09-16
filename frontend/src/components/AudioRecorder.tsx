"use client";

import React, { useState, useRef } from "react";

interface AudioRecorderProps {
  onFileSelect: (file: File) => void;
  isLoading: boolean;
}

export default function AudioRecorder({ onFileSelect, isLoading }: AudioRecorderProps) {
  const [isRecording, setIsRecording] = useState(false);
  const [time, setTime] = useState(0);
  const mediaRecorderRef = useRef<MediaRecorder | null>(null);
  const chunksRef = useRef<Blob[]>([]);
  const timerRef = useRef<NodeJS.Timeout | null>(null);

  const startRecording = async () => {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      const mediaRecorder = new MediaRecorder(stream);
      mediaRecorderRef.current = mediaRecorder;
      chunksRef.current = [];

      mediaRecorder.ondataavailable = (e) => {
        if (e.data.size > 0) chunksRef.current.push(e.data);
      };

      mediaRecorder.onstop = () => {
        const blob = new Blob(chunksRef.current, { type: "audio/webm" });
        // We package it as a .webm file which the backend preprocessor will read perfectly via librosa/ffmpeg
        const file = new File([blob], "live_recording.webm", { type: "audio/webm" });
        onFileSelect(file);
        
        // Release the microphone tracks
        stream.getTracks().forEach(track => track.stop());
      };

      mediaRecorder.start();
      setIsRecording(true);
      setTime(0);
      
      // Start timer
      timerRef.current = setInterval(() => {
        setTime((t) => t + 1);
      }, 1000);
      
    } catch (err) {
      console.error("Error accessing mic:", err);
      alert("Microphone access denied. Please allow microphone permissions in your browser.");
    }
  };

  const stopRecording = () => {
    if (mediaRecorderRef.current && isRecording) {
      mediaRecorderRef.current.stop();
      setIsRecording(false);
      if (timerRef.current) clearInterval(timerRef.current);
    }
  };

  const formatTime = (seconds: number) => {
    const m = Math.floor(seconds / 60).toString().padStart(2, "0");
    const s = (seconds % 60).toString().padStart(2, "0");
    return `${m}:${s}`;
  };

  return (
    <div className="flex flex-col items-center justify-center p-6 border-2 border-gray-100 rounded-xl bg-white mt-4 w-full max-w-2xl mx-auto shadow-sm">
      <p className="text-xs font-bold text-gray-400 uppercase tracking-widest mb-5">Or Record Live Audio</p>
      
      {!isRecording ? (
        <button 
          onClick={startRecording}
          disabled={isLoading}
          className={`flex items-center gap-2 px-6 py-3 rounded-full font-bold text-white transition-all shadow-md
            ${isLoading ? "bg-gray-300 cursor-not-allowed" : "bg-black hover:bg-gray-800 hover:shadow-lg active:scale-95"}`}
        >
          <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round">
            <path d="M12 2a3 3 0 0 0-3 3v7a3 3 0 0 0 6 0V5a3 3 0 0 0-3-3Z"></path>
            <path d="M19 10v2a7 7 0 0 1-14 0v-2"></path>
            <line x1="12" x2="12" y1="19" y2="22"></line>
          </svg>
          {isLoading ? "Analyzing..." : "Start Recording"}
        </button>
      ) : (
        <div className="flex flex-col items-center gap-4">
          <div className="flex items-center gap-3 text-red-500 font-mono text-2xl font-bold bg-red-50 px-4 py-1 rounded-full">
            <span className="w-3 h-3 rounded-full bg-red-500 animate-pulse"></span>
            {formatTime(time)}
          </div>
          <button 
            onClick={stopRecording}
            className="flex items-center gap-2 px-6 py-3 rounded-full font-bold text-red-600 border-2 border-red-100 bg-white hover:bg-red-50 transition-all active:scale-95 shadow-sm"
          >
            <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="currentColor" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
              <rect width="12" height="12" x="6" y="6" rx="2" ry="2"></rect>
            </svg>
            Stop & Analyze
          </button>
          <p className="text-xs text-gray-400 font-medium">Speak now, or play an audio from another device...</p>
        </div>
      )}
    </div>
  );
}
