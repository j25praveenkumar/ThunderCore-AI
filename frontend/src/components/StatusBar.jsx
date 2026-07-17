import React from 'react';

export default function StatusBar({ backendOnline, voiceReady }) {
  return (
    <div className="h-8 flex items-center justify-between px-4 bg-thunder-surface
                    border-b border-thunder-border text-xs text-thunder-muted select-none">
      <span className="font-semibold text-thunder-accent tracking-widest">THUNDER AI</span>
      <div className="flex items-center gap-4">
        {/* Backend status */}
        <div className="flex items-center gap-1.5">
          <span className={`w-2 h-2 rounded-full ${backendOnline ? 'bg-green-400' : 'bg-red-500'}`} />
          <span>{backendOnline ? 'Backend Online' : 'Backend Offline'}</span>
        </div>
        {/* Voice status */}
        <div className="flex items-center gap-1.5">
          <span className={`w-2 h-2 rounded-full ${voiceReady ? 'bg-green-400' : 'bg-yellow-500'}`} />
          <span>{voiceReady ? 'Voice Ready' : 'Voice Unavailable'}</span>
        </div>
      </div>
    </div>
  );
}
