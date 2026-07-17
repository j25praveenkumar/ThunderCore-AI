"""
Thunder AI — Voice Output
Uses pyttsx3 (offline TTS) — no internet required.
Install: pip install pyttsx3
"""
import logging
import threading

logger = logging.getLogger(__name__)

_engine = None
_lock = threading.Lock()


def _get_engine():
    """Lazy-init the TTS engine (thread-safe)."""
    global _engine
    if _engine is None:
        try:
            import pyttsx3
            _engine = pyttsx3.init()
            _engine.setProperty("rate", 170)    # words per minute
            _engine.setProperty("volume", 0.9)
            # Pick a clear English voice if available
            voices = _engine.getProperty("voices")
            for v in voices:
                if "english" in v.name.lower() or "zira" in v.name.lower():
                    _engine.setProperty("voice", v.id)
                    break
        except ImportError:
            logger.warning("pyttsx3 not installed. Run: pip install pyttsx3")
        except Exception as e:
            logger.error(f"TTS init error: {e}")
    return _engine


def speak(text: str, blocking: bool = False) -> None:
    """
    Speak the given text aloud.
    blocking=False runs in a background thread so it doesn't freeze the API.
    """
    if not text or not text.strip():
        return

    def _say():
        with _lock:
            engine = _get_engine()
            if engine is None:
                return
            try:
                engine.say(text)
                engine.runAndWait()
            except Exception as e:
                logger.error(f"TTS speak error: {e}")

    if blocking:
        _say()
    else:
        t = threading.Thread(target=_say, daemon=True)
        t.start()
