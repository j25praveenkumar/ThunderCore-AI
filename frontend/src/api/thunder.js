/**
 * Thunder AI — API Client
 * All chat and voice go through /api/assistant
 */
import axios from 'axios';

const BASE_URL = 'http://127.0.0.1:8000';

const api = axios.create({
  baseURL: BASE_URL,
  timeout: 120000,
  headers: { 'Content-Type': 'application/json' },
});

// ── Assistant (unified chat + voice) ─────────────────────────────────────────

/** Send a text message, get a reply string */
export const sendMessage = (message) =>
  api.post('/api/assistant/chat', { message }).then((r) => r.data.reply);

/** Listen on mic, returns { transcript, reply } */
export const voiceListen = () =>
  api.post('/api/assistant/listen').then((r) => r.data);

/** Speak any text via TTS */
export const voiceSpeak = (text) =>
  api.post('/api/assistant/speak', { text }).then((r) => r.data);

// ── History ───────────────────────────────────────────────────────────────────
export const getHistory = (limit = 50) =>
  api.get(`/api/history?limit=${limit}`).then((r) => r.data);

export const clearHistory = () =>
  api.delete('/api/history').then((r) => r.data);

// ── Notes ─────────────────────────────────────────────────────────────────────
export const getNotes = () =>
  api.get('/api/notes').then((r) => r.data);

export const createNote = (title, content) =>
  api.post('/api/notes', { title, content }).then((r) => r.data);

export const deleteNote = (id) =>
  api.delete(`/api/notes/${id}`).then((r) => r.data);

// ── Memory ────────────────────────────────────────────────────────────────────
export const getMemory = () =>
  api.get('/api/memory').then((r) => r.data);

export const addMemory = (key, value) =>
  api.post('/api/memory', { key, value }).then((r) => r.data);

export const deleteMemory = (id) =>
  api.delete(`/api/memory/${id}`).then((r) => r.data);

// ── Health (for StatusBar polling) ───────────────────────────────────────────
// Uses a short timeout so the UI recovers quickly when backend starts
const healthApi = axios.create({
  baseURL: BASE_URL,
  timeout: 3000,
  headers: { 'Content-Type': 'application/json' },
});

export const checkHealth = () =>
  healthApi.get('/health').then((r) => r.data);

export const checkStatus = () =>
  healthApi.get('/api/assistant/status').then((r) => r.data);
