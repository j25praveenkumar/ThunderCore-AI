import React from 'react';

const SETTINGS = [
  { label: 'AI Model', value: 'llama3.2:3b (Ollama)', note: 'Change in config/settings.py' },
  { label: 'Whisper Model', value: 'base', note: 'tiny / base / small / medium' },
  { label: 'Backend URL', value: 'http://127.0.0.1:8000', note: 'Local FastAPI server' },
  { label: 'Database', value: 'thunder.db (SQLite)', note: 'database/thunder.db' },
  { label: 'Wake Word', value: '"thunder"', note: 'OpenWakeWord (Phase 3)' },
  { label: 'Emotion Recognition', value: 'Disabled', note: 'Enable in config/settings.py' },
  { label: 'Version', value: '1.0.0', note: 'Thunder AI' },
];

export default function SettingsPage() {
  return (
    <div className="h-full overflow-y-auto p-6">
      <h1 className="text-xl font-semibold text-thunder-text mb-2">⚙️ Settings</h1>
      <p className="text-thunder-muted text-sm mb-6">
        Core configuration. Advanced settings can be changed in <code className="text-thunder-accent2">config/settings.py</code>.
      </p>

      <div className="flex flex-col gap-3">
        {SETTINGS.map(({ label, value, note }) => (
          <div
            key={label}
            className="flex items-center justify-between bg-thunder-card border border-thunder-border
                       rounded-xl px-4 py-3"
          >
            <div>
              <p className="text-thunder-text text-sm font-medium">{label}</p>
              <p className="text-thunder-muted text-xs mt-0.5">{note}</p>
            </div>
            <span className="text-thunder-accent2 text-sm font-mono ml-4">{value}</span>
          </div>
        ))}
      </div>

      <div className="mt-8 bg-thunder-card border border-thunder-border rounded-2xl p-4">
        <h2 className="text-thunder-text font-medium mb-3">Development Phases</h2>
        {[
          ['✅ Phase 1', 'Project setup, backend, DB, frontend skeleton'],
          ['✅ Phase 2', 'Chat UI, LLM integration (Ollama)'],
          ['⏳ Phase 3', 'Voice recognition, wake word, TTS'],
          ['⏳ Phase 4', 'Windows automation, file management'],
          ['⏳ Phase 5', 'Memory engine, notes, reminders'],
          ['⏳ Phase 6', 'Facial emotion recognition'],
          ['⏳ Phase 7', 'Plugin system, installer'],
        ].map(([phase, desc]) => (
          <div key={phase} className="flex gap-3 py-1.5 text-sm">
            <span className="text-thunder-accent2 flex-shrink-0 w-24">{phase}</span>
            <span className="text-thunder-muted">{desc}</span>
          </div>
        ))}
      </div>
    </div>
  );
}
