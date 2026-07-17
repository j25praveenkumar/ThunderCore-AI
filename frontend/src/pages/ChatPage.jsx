import React, { useState, useEffect, useRef } from 'react';
import { motion } from 'framer-motion';
import MessageBubble from '../components/MessageBubble';
import TypingIndicator from '../components/TypingIndicator';
import { sendMessage, getHistory, voiceListen } from '../api/thunder';

const SUGGESTIONS = [
  'Open Chrome', 'Lock my PC', 'Search YouTube for lo-fi music',
  'Create a note', 'Show my memory', 'Volume up',
];

export default function ChatPage({ voiceReady = false }) {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);
  const [listening, setListening] = useState(false);
  const bottomRef = useRef(null);
  const inputRef = useRef(null);

  // Load history on mount
  useEffect(() => {
    getHistory(50)
      .then((hist) => {
        if (hist.length > 0) setMessages(hist);
        else setMessages([{
          role: 'assistant',
          content: "Hey! I'm Thunder AI — your offline desktop assistant. What can I do for you?",
          timestamp: new Date().toISOString(),
        }]);
      })
      .catch(() => {
        setMessages([{
          role: 'assistant',
          content: "Hey! I'm Thunder AI — your offline desktop assistant. What can I do for you?",
          timestamp: new Date().toISOString(),
        }]);
      });
  }, []);

  // Scroll to bottom
  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages, loading]);

  // ── Text send ──────────────────────────────────────────────────────────────
  const handleSend = async (text = input) => {
    const msg = text.trim();
    if (!msg || loading || listening) return;

    setInput('');
    setMessages((prev) => [...prev, {
      role: 'user', content: msg, timestamp: new Date().toISOString(),
    }]);
    setLoading(true);

    try {
      const reply = await sendMessage(msg);
      setMessages((prev) => [...prev, {
        role: 'assistant', content: reply, timestamp: new Date().toISOString(),
      }]);
    } catch {
      setMessages((prev) => [...prev, {
        role: 'assistant',
        content: '⚠️ Backend is offline. Make sure the Python server is running.',
        timestamp: new Date().toISOString(),
      }]);
    } finally {
      setLoading(false);
      inputRef.current?.focus();
    }
  };

  const handleKey = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  // ── Voice listen ───────────────────────────────────────────────────────────
  const handleVoice = async () => {
    if (listening || loading) return;
    setListening(true);

    // Show listening indicator
    setMessages((prev) => [...prev, {
      role: 'assistant',
      content: '🎙️ Listening... speak now.',
      timestamp: new Date().toISOString(),
    }]);

    try {
      const { transcript, reply } = await voiceListen();
      setMessages((prev) => {
        const updated = [...prev];
        // Replace the listening placeholder
        updated[updated.length - 1] = {
          role: 'user',
          content: transcript || '(no speech detected)',
          timestamp: new Date().toISOString(),
        };
        if (reply) {
          updated.push({
            role: 'assistant',
            content: reply,
            timestamp: new Date().toISOString(),
          });
        }
        return updated;
      });
    } catch {
      setMessages((prev) => {
        const updated = [...prev];
        updated[updated.length - 1] = {
          role: 'assistant',
          content: '⚠️ Voice not available. Install deps: pip install SpeechRecognition pyttsx3 pyaudio',
          timestamp: new Date().toISOString(),
        };
        return updated;
      });
    } finally {
      setListening(false);
      inputRef.current?.focus();
    }
  };

  return (
    <div className="flex flex-col h-full bg-thunder-bg">

      {/* Messages */}
      <div className="flex-1 overflow-y-auto px-6 py-4">
        {messages.map((msg, i) => (
          <MessageBubble
            key={i}
            role={msg.role}
            content={msg.content}
            timestamp={msg.timestamp}
          />
        ))}
        {(loading || listening) && <TypingIndicator />}
        <div ref={bottomRef} />
      </div>

      {/* Suggestions (only on empty chat) */}
      {messages.length <= 1 && (
        <div className="px-6 pb-2 flex gap-2 flex-wrap">
          {SUGGESTIONS.map((s) => (
            <button
              key={s}
              onClick={() => handleSend(s)}
              className="text-xs px-3 py-1.5 rounded-full bg-thunder-card border border-thunder-border
                         text-thunder-muted hover:text-thunder-accent hover:border-thunder-accent
                         transition-all duration-200"
            >
              {s}
            </button>
          ))}
        </div>
      )}

      {/* Input bar */}
      <div className="px-4 pb-4 pt-2">
        <div className="flex items-end gap-3 bg-thunder-card border border-thunder-border
                        rounded-2xl px-4 py-3 focus-within:border-thunder-accent transition-colors duration-200">

          <textarea
            ref={inputRef}
            rows={1}
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={handleKey}
            placeholder="Ask Thunder anything..."
            className="flex-1 bg-transparent text-thunder-text placeholder-thunder-muted
                       resize-none outline-none text-sm leading-relaxed max-h-32"
            style={{ fieldSizing: 'content' }}
          />

          {/* Mic button */}
          <motion.button
            whileTap={{ scale: 0.9 }}
            onClick={handleVoice}
            disabled={loading || !voiceReady}
            title={voiceReady ? 'Voice input' : 'Voice unavailable (mic/TTS not ready)'}
            className={`w-9 h-9 rounded-xl flex items-center justify-center flex-shrink-0
                        transition-all duration-200
                        ${listening
                          ? 'bg-red-500 text-white animate-pulse scale-110'
                          : voiceReady
                            ? 'bg-thunder-surface text-thunder-muted hover:text-thunder-accent hover:bg-thunder-card border border-thunder-border'
                            : 'bg-thunder-surface text-thunder-muted opacity-40 border border-thunder-border cursor-not-allowed'
                        }`}
          >
            <svg width="15" height="15" viewBox="0 0 24 24" fill="currentColor">
              <path d="M12 1a4 4 0 0 1 4 4v7a4 4 0 0 1-8 0V5a4 4 0 0 1 4-4zm0 2a2 2 0 0 0-2 2v7a2 2 0 0 0 4 0V5a2 2 0 0 0-2-2zm-7 9a7 7 0 0 0 14 0h2a9 9 0 0 1-8 8.94V23h-2v-2.06A9 9 0 0 1 3 12h2z"/>
            </svg>
          </motion.button>

          {/* Send button */}
          <motion.button
            whileTap={{ scale: 0.9 }}
            onClick={() => handleSend()}
            disabled={!input.trim() || loading || listening}
            className="w-9 h-9 rounded-xl bg-thunder-accent flex items-center justify-center
                       text-white disabled:opacity-40 disabled:cursor-not-allowed
                       hover:bg-red-500 transition-colors duration-200 flex-shrink-0"
          >
            <svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor">
              <path d="M2.01 21L23 12 2.01 3 2 10l15 2-15 2z"/>
            </svg>
          </motion.button>

        </div>
        <p className="text-center text-xs text-thunder-muted mt-2">
          Press Enter to send · Shift+Enter for new line · 🎙️ mic button for voice
        </p>
      </div>
    </div>
  );
}
