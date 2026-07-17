import React, { useState, useEffect, useCallback } from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import Sidebar from './components/Sidebar';
import ChatPage from './pages/ChatPage';
import NotesPage from './pages/NotesPage';
import MemoryPage from './pages/MemoryPage';
import HistoryPage from './pages/HistoryPage';
import SettingsPage from './pages/SettingsPage';
import StatusBar from './components/StatusBar';
import { checkStatus } from './api/thunder';

export default function App() {
  const [backendOnline, setBackendOnline] = useState(false);
  const [voiceReady, setVoiceReady] = useState(false);

  const checkBackend = useCallback(async () => {
    try {
      const s = await checkStatus();
      setBackendOnline(true);
      setVoiceReady(s.voice_ready === true);
    } catch {
      setBackendOnline(false);
      setVoiceReady(false);
    }
  }, []);

  useEffect(() => {
    // Check immediately
    checkBackend();
    // Then poll every 2 seconds
    const interval = setInterval(checkBackend, 2000);
    return () => clearInterval(interval);
  }, [checkBackend]);

  return (
    <Router>
      <div className="flex h-screen w-screen overflow-hidden bg-thunder-bg">
        <Sidebar />
        <div className="flex flex-col flex-1 overflow-hidden">
          <StatusBar backendOnline={backendOnline} voiceReady={voiceReady} />
          <main className="flex-1 overflow-hidden">
            <Routes>
              <Route path="/" element={<Navigate to="/chat" replace />} />
              <Route path="/chat" element={<ChatPage voiceReady={voiceReady} />} />
              <Route path="/notes" element={<NotesPage />} />
              <Route path="/memory" element={<MemoryPage />} />
              <Route path="/history" element={<HistoryPage />} />
              <Route path="/settings" element={<SettingsPage />} />
            </Routes>
          </main>
        </div>
      </div>
    </Router>
  );
}
