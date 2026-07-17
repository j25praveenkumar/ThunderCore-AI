import React, { useState, useEffect } from 'react';
import { getHistory, clearHistory } from '../api/thunder';

export default function HistoryPage() {
  const [history, setHistory] = useState([]);

  const load = () => getHistory(100).then(setHistory).catch(() => {});

  useEffect(() => { load(); }, []);

  const handleClear = async () => {
    if (!window.confirm('Clear all conversation history?')) return;
    await clearHistory();
    setHistory([]);
  };

  return (
    <div className="h-full flex flex-col p-6">
      <div className="flex justify-between items-center mb-6">
        <h1 className="text-xl font-semibold text-thunder-text">🕐 History</h1>
        {history.length > 0 && (
          <button
            onClick={handleClear}
            className="px-3 py-1.5 text-xs bg-thunder-card border border-thunder-border
                       text-thunder-muted hover:text-thunder-accent hover:border-thunder-accent
                       rounded-lg transition-colors duration-200"
          >
            Clear All
          </button>
        )}
      </div>

      <div className="flex-1 overflow-y-auto flex flex-col gap-2">
        {history.length === 0 && (
          <p className="text-thunder-muted text-sm text-center py-8">No conversation history yet.</p>
        )}
        {history.map((msg) => (
          <div
            key={msg.id}
            className={`flex gap-3 px-4 py-3 rounded-xl text-sm
              ${msg.role === 'user'
                ? 'bg-thunder-card border border-thunder-border'
                : 'bg-thunder-surface'
              }`}
          >
            <span className={`font-medium flex-shrink-0 w-20 text-xs pt-0.5
              ${msg.role === 'user' ? 'text-thunder-accent' : 'text-thunder-accent2'}`}>
              {msg.role === 'user' ? '👤 You' : '⚡ Thunder'}
            </span>
            <p className="text-thunder-text leading-relaxed flex-1 whitespace-pre-wrap">
              {msg.content}
            </p>
            <span className="text-xs text-thunder-muted flex-shrink-0 pt-0.5">
              {new Date(msg.timestamp).toLocaleTimeString()}
            </span>
          </div>
        ))}
      </div>
    </div>
  );
}
