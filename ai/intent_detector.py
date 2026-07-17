"""
Thunder AI — Intent Detector
Simple rule-based intent classification before sending to LLM.
"""
import re
from typing import Dict, Any


INTENT_PATTERNS = {
    "shutdown":        [r"\bshutdown\b", r"\bshut down\b", r"\bturn off.*pc\b", r"\bpower off\b"],
    "restart":         [r"\brestart\b", r"\breboot\b"],
    "lock":            [r"\block.*pc\b", r"\block.*screen\b", r"\block.*computer\b"],
    "sleep":           [r"\bsleep\b", r"\bhibernate\b"],
    "volume_up":       [r"\bvolume up\b", r"\bincrease volume\b", r"\blouder\b"],
    "volume_down":     [r"\bvolume down\b", r"\bdecrease volume\b", r"\bquieter\b"],
    "mute":            [r"\bmute\b", r"\bsilence\b"],
    "open_app":        [r"\bopen\b.+", r"\blaunch\b.+", r"\bstart\b.+"],
    "close_app":       [r"\bclose\b.+", r"\bkill\b.+", r"\bexit\b.+"],
    "open_website":    [r"\bopen\b.*\.(com|org|net|io)\b", r"\bgo to\b.+", r"\bbrowse\b.+"],
    "search_google":   [r"\bsearch google\b", r"\bgoogle\b.+"],
    "search_youtube":  [r"\bsearch youtube\b", r"\byoutube\b.+", r"\bplay on youtube\b"],
    "create_note":     [r"\bcreate.*note\b", r"\badd.*note\b", r"\bwrite.*note\b", r"\bnote.*that\b"],
    "read_notes":      [r"\bshow.*note\b", r"\bread.*note\b", r"\bmy notes\b", r"\blist.*note\b"],
    "delete_note":     [r"\bdelete.*note\b", r"\bremove.*note\b"],
    "set_reminder":    [r"\bremind me\b", r"\bset.*reminder\b", r"\balarm\b"],
    "show_reminders":  [r"\bmy reminders\b", r"\bshow.*reminder\b", r"\blist.*reminder\b"],
    "remember":        [r"\bremember\b", r"\bdon.?t forget\b", r"\bsave.*fact\b"],
    "recall":          [r"\bdo you remember\b", r"\bwhat did i\b", r"\bwhat.?s my\b"],
    "create_folder":   [r"\bcreate.*folder\b", r"\bmake.*folder\b", r"\bnew.*folder\b"],
    "delete_file":     [r"\bdelete.*file\b", r"\bremove.*file\b", r"\bdelete.*folder\b"],
    "calculator":      [r"\bcalculate\b", r"\bwhat is \d", r"\b\d+[\+\-\*\/]\d+\b"],
}


def detect_intent(text: str) -> Dict[str, Any]:
    """
    Returns dict with 'intent' (str) and 'raw' (original text).
    Falls back to 'chat' intent when no pattern matches.
    """
    lowered = text.lower().strip()
    for intent, patterns in INTENT_PATTERNS.items():
        for pattern in patterns:
            if re.search(pattern, lowered):
                return {"intent": intent, "raw": text}
    return {"intent": "chat", "raw": text}
