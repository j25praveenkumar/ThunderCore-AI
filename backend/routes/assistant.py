"""
Thunder AI — Unified Assistant Route
Single endpoint handles both text chat and voice input/output.

POST /api/assistant/chat    → text message → reply
POST /api/assistant/listen  → mic listen → transcript + reply (also speaks)
POST /api/assistant/speak   → TTS any text
GET  /api/assistant/status  → health + mic/tts availability
"""
import logging
from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session

from database.models import get_db
from backend.services.chat_service import process_message
from speech.voice_input import listen_once, is_microphone_available
from speech.voice_output import speak

router = APIRouter(prefix="/api/assistant", tags=["assistant"])
logger = logging.getLogger(__name__)


# ── Request / Response models ─────────────────────────────────────────────────

class ChatRequest(BaseModel):
    message: str
    speak_reply: bool = False   # set True to also speak the reply aloud


class ChatResponse(BaseModel):
    reply: str
    source: str = "text"        # "text" or "voice"


class SpeakRequest(BaseModel):
    text: str


class VoiceResponse(BaseModel):
    transcript: str
    reply: str
    source: str = "voice"


# ── Routes ────────────────────────────────────────────────────────────────────

@router.get("/status")
def assistant_status():
    """Backend + mic + TTS availability check."""
    mic_ok = False
    tts_ok = False

    try:
        mic_ok = is_microphone_available()
    except Exception:
        pass

    try:
        import pyttsx3
        tts_ok = True
    except ImportError:
        pass

    return {
        "status": "ok",
        "microphone": mic_ok,
        "tts": tts_ok,
        "voice_ready": mic_ok and tts_ok,
    }


@router.post("/chat", response_model=ChatResponse)
def text_chat(req: ChatRequest, db: Session = Depends(get_db)):
    """Send a text message, get a reply. Optionally speaks the reply."""
    logger.info(f"[text] {req.message}")
    reply = process_message(req.message, db)
    if req.speak_reply:
        speak(reply)
    return ChatResponse(reply=reply, source="text")


@router.post("/listen", response_model=VoiceResponse)
def voice_listen(db: Session = Depends(get_db)):
    """Listen on mic, transcribe, process through the AI pipeline, speak reply."""
    transcript = listen_once(timeout=6, phrase_limit=12)

    if not transcript:
        msg = "I didn't catch that. Please try again."
        speak(msg)
        return VoiceResponse(transcript="", reply=msg)

    logger.info(f"[voice] {transcript}")
    reply = process_message(transcript, db)
    speak(reply)
    return VoiceResponse(transcript=transcript, reply=reply)


@router.post("/speak")
def voice_speak(req: SpeakRequest):
    """Speak any text via TTS."""
    speak(req.text)
    return {"status": "speaking", "text": req.text}
