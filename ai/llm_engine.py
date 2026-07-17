"""
Thunder AI — LLM Engine (Ollama backend)
Handles prompt construction, context management, and response generation.
"""
import requests
import json
import logging
from typing import List, Dict

import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config.settings import OLLAMA_BASE_URL, DEFAULT_MODEL

logger = logging.getLogger(__name__)

SYSTEM_PROMPT = """You are Thunder AI, a fully offline AI desktop assistant running on Windows.
You are helpful, concise, and friendly. You can help with:
- Answering questions
- Controlling Windows (open apps, files, system commands)
- Managing notes and reminders
- Remembering user preferences
Always respond in plain text unless the user asks for code or lists."""


def build_messages(history: List[Dict], user_input: str, memory_context: str = "") -> List[Dict]:
    """Build the messages list for Ollama chat API."""
    system_content = SYSTEM_PROMPT
    if memory_context:
        system_content += f"\n\nUser memory context:\n{memory_context}"

    messages = [{"role": "system", "content": system_content}]
    # Keep last 10 turns to avoid token overflow
    for turn in history[-10:]:
        messages.append({"role": turn["role"], "content": turn["content"]})
    messages.append({"role": "user", "content": user_input})
    return messages


def chat(history: List[Dict], user_input: str, memory_context: str = "") -> str:
    """Send a message to Ollama and return the assistant reply."""
    messages = build_messages(history, user_input, memory_context)
    payload = {
        "model": DEFAULT_MODEL,
        "messages": messages,
        "stream": False,
        "options": {
            "temperature": 0.7,
            "num_predict": 512,
        }
    }
    try:
        response = requests.post(
            f"{OLLAMA_BASE_URL}/api/chat",
            json=payload,
            timeout=120
        )
        response.raise_for_status()
        data = response.json()
        return data["message"]["content"].strip()
    except requests.exceptions.ConnectionError:
        logger.error("Ollama is not running. Start it with: ollama serve")
        return "⚠️ Ollama is not running. Please start Ollama and try again."
    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 404:
            logger.error(f"Model '{DEFAULT_MODEL}' not found. Run: ollama pull {DEFAULT_MODEL}")
            return f"⚠️ Model '{DEFAULT_MODEL}' not found. Open a terminal and run:\n\n  ollama pull {DEFAULT_MODEL}\n\nThen try again."
        logger.error(f"Ollama HTTP error: {e}")
        return f"⚠️ Ollama error: {str(e)}"
    except requests.exceptions.Timeout:
        logger.error("Ollama request timed out")
        return "⚠️ The AI took too long to respond. Please try again."
    except Exception as e:
        logger.error(f"LLM error: {e}")
        return f"⚠️ AI error: {str(e)}"


def list_models() -> List[str]:
    """Return available Ollama models."""
    try:
        r = requests.get(f"{OLLAMA_BASE_URL}/api/tags", timeout=10)
        r.raise_for_status()
        return [m["name"] for m in r.json().get("models", [])]
    except Exception:
        return []
