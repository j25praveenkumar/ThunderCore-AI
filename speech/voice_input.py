"""
Thunder AI — Voice Input
Uses sounddevice (no pyaudio needed) for mic recording + SpeechRecognition for transcription.
Works on Python 3.14+.

Install: pip install sounddevice scipy SpeechRecognition
"""
import io
import logging
import wave
import numpy as np

logger = logging.getLogger(__name__)

SAMPLE_RATE = 16000   # Hz — optimal for speech recognition
CHANNELS = 1


def is_microphone_available() -> bool:
    """Check if a microphone is accessible via sounddevice."""
    try:
        import sounddevice as sd
        devices = sd.query_devices()
        # Check if any input device exists
        for d in devices:
            if d["max_input_channels"] > 0:
                return True
        return False
    except Exception as e:
        logger.debug(f"Mic check failed: {e}")
        return False


def _record_audio(duration: int = 6) -> bytes | None:
    """
    Record `duration` seconds of audio using sounddevice.
    Returns raw WAV bytes or None on failure.
    """
    try:
        import sounddevice as sd

        logger.info(f"Recording {duration}s of audio...")
        audio = sd.rec(
            int(duration * SAMPLE_RATE),
            samplerate=SAMPLE_RATE,
            channels=CHANNELS,
            dtype="int16",
        )
        sd.wait()  # block until done

        # Convert numpy array to WAV bytes in memory
        buf = io.BytesIO()
        with wave.open(buf, "wb") as wf:
            wf.setnchannels(CHANNELS)
            wf.setsampwidth(2)          # int16 = 2 bytes
            wf.setframerate(SAMPLE_RATE)
            wf.writeframes(audio.tobytes())
        buf.seek(0)
        return buf.read()

    except Exception as e:
        logger.error(f"Audio recording error: {e}")
        return None


def _is_silent(audio_bytes: bytes, threshold: int = 200) -> bool:
    """Return True if the audio is essentially silence (no speech detected)."""
    try:
        buf = io.BytesIO(audio_bytes)
        with wave.open(buf, "rb") as wf:
            raw = wf.readframes(wf.getnframes())
        samples = np.frombuffer(raw, dtype=np.int16)
        return float(np.abs(samples).mean()) < threshold
    except Exception:
        return False


def listen_once(timeout: int = 6, phrase_limit: int = 10) -> str:
    """
    Record audio from mic and transcribe it using Google Speech Recognition.
    Returns transcribed text, or empty string on failure/silence.

    `timeout` and `phrase_limit` map to the recording duration.
    """
    try:
        import speech_recognition as sr
    except ImportError:
        logger.warning("SpeechRecognition not installed. Run: pip install SpeechRecognition")
        return ""

    # Record raw audio
    wav_bytes = _record_audio(duration=phrase_limit)
    if not wav_bytes:
        return ""

    # Skip if silent
    if _is_silent(wav_bytes):
        logger.debug("Audio was silent — skipping transcription")
        return ""

    # Transcribe using SpeechRecognition with AudioData from raw WAV
    recognizer = sr.Recognizer()
    try:
        audio = sr.AudioData(wav_bytes, SAMPLE_RATE, 2)
        text = recognizer.recognize_google(audio)
        logger.info(f"Transcribed: {text}")
        return text.strip()
    except sr.UnknownValueError:
        logger.debug("Could not understand audio")
        return ""
    except sr.RequestError as e:
        logger.error(f"Speech recognition service error: {e}")
        return ""
    except Exception as e:
        logger.error(f"Transcription error: {e}")
        return ""
