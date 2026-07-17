"""
Thunder AI — Global Configuration
"""
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Database
DATABASE_URL = f"sqlite:///{os.path.join(BASE_DIR, 'database', 'thunder.db')}"

# LLM
OLLAMA_BASE_URL = "http://localhost:11434"
DEFAULT_MODEL = "llama3.2:3b"       # swap to any model you have pulled in Ollama

# Speech
WHISPER_MODEL = "base"              # tiny / base / small / medium
PIPER_VOICE = "en_US-lessac-medium"

# Wake word
WAKE_WORD = "thunder"

# Vision
EMOTION_MODEL_PATH = os.path.join(BASE_DIR, "models", "emotion_cnn.h5")
ENABLE_EMOTION = False              # set True when model is ready

# App
APP_NAME = "Thunder AI"
APP_VERSION = "1.0.0"
DEBUG = True
LOG_DIR = os.path.join(BASE_DIR, "logs")
