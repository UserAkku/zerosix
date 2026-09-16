import React from "react";

export default function Header() {
  return (
    <header className="fixed top-0 w-full h-16 bg-white border-b border-gray-200 z-50 flex items-center px-6 justify-between">
      <div className="flex items-center gap-2">
        <img src="/logo.png" alt="Team ZeroSix Logo" className="w-8 h-8 object-contain" />
        <span className="font-bold text-xl text-black tracking-tight">TEAM ZEROSIX</span>
      </div>
      <div className="text-sm font-medium text-gray-500">
        AI Voice Clone Detection (Hindi & English)
      </div>
    </header>
  );
}
