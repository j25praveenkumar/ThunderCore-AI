"""
Thunder AI — Chat Service
Orchestrates: intent detection → memory → LLM → automation → response.
"""
import re
import logging
from sqlalchemy.orm import Session

from ai.llm_engine import chat
from ai.intent_detector import detect_intent
from ai.memory_manager import (
    save_memory, get_all_memory, save_conversation, get_recent_history
)
from automation.windows_control import (
    shutdown_pc, restart_pc, lock_pc, sleep_pc, cancel_shutdown,
    volume_up, volume_down, mute_volume,
    open_app, close_app,
    open_website, search_google, search_youtube,
    create_folder, delete_path, list_folder
)
from database.models import Note, Reminder
from datetime import datetime

logger = logging.getLogger(__name__)


def _extract_quoted(text: str) -> str:
    """Extract first quoted string or return text after keyword."""
    match = re.search(r'"([^"]+)"', text)
    if match:
        return match.group(1)
    return text


def _handle_automation(intent: str, raw: str, db: Session) -> str | None:
    """Execute automation commands. Returns None if intent == 'chat'."""

    if intent == "shutdown":
        return shutdown_pc()
    if intent == "restart":
        return restart_pc()
    if intent == "lock":
        return lock_pc()
    if intent == "sleep":
        return sleep_pc()
    if intent == "volume_up":
        return volume_up()
    if intent == "volume_down":
        return volume_down()
    if intent == "mute":
        return mute_volume()

    if intent == "open_app":
        # Extract app name: "open chrome" → chrome
        match = re.search(r"(?:open|launch|start)\s+(.+)", raw, re.IGNORECASE)
        app = match.group(1).strip() if match else raw
        return open_app(app)

    if intent == "close_app":
        match = re.search(r"(?:close|kill|exit)\s+(.+)", raw, re.IGNORECASE)
        app = match.group(1).strip() if match else raw
        return close_app(app)

    if intent == "open_website":
        match = re.search(r"(?:open|go to|browse)\s+(.+)", raw, re.IGNORECASE)
        url = match.group(1).strip() if match else raw
        return open_website(url)

    if intent == "search_google":
        match = re.search(r"(?:search google for|google)\s+(.+)", raw, re.IGNORECASE)
        q = match.group(1).strip() if match else raw
        return search_google(q)

    if intent == "search_youtube":
        match = re.search(r"(?:search youtube for|youtube)\s+(.+)", raw, re.IGNORECASE)
        q = match.group(1).strip() if match else raw
        return search_youtube(q)

    if intent == "create_folder":
        match = re.search(r"(?:create|make|new)\s+folder\s+(.+)", raw, re.IGNORECASE)
        path = match.group(1).strip() if match else "NewFolder"
        return create_folder(path)

    if intent == "delete_file":
        match = re.search(r"(?:delete|remove)\s+(?:file|folder)?\s*(.+)", raw, re.IGNORECASE)
        path = match.group(1).strip() if match else ""
        return delete_path(path) if path else "Please specify a file or folder path."

    # Notes
    if intent == "create_note":
        match = re.search(r"(?:note|write|add note)\s+(?:that\s+)?(.+)", raw, re.IGNORECASE)
        content = match.group(1).strip() if match else raw
        note = Note(title=f"Note {datetime.utcnow().strftime('%H:%M')}", content=content)
        db.add(note)
        db.commit()
        return f"Note saved: {content}"

    if intent == "read_notes":
        notes = db.query(Note).order_by(Note.created_at.desc()).limit(10).all()
        if not notes:
            return "You have no notes yet."
        return "Your notes:\n" + "\n".join(f"• [{n.id}] {n.title}: {n.content}" for n in notes)

    if intent == "delete_note":
        match = re.search(r"delete note\s+(\d+)", raw, re.IGNORECASE)
        if match:
            note_id = int(match.group(1))
            note = db.query(Note).filter(Note.id == note_id).first()
            if note:
                db.delete(note)
                db.commit()
                return f"Note {note_id} deleted."
            return f"Note {note_id} not found."
        return "Please specify the note ID to delete."

    # Memory
    if intent == "remember":
        # "remember my favorite editor is VS Code"
        match = re.search(r"remember\s+(?:that\s+)?(?:my\s+)?(.+?)\s+is\s+(.+)", raw, re.IGNORECASE)
        if match:
            key, value = match.group(1).strip(), match.group(2).strip()
            save_memory(db, key, value)
            return f"Got it! I'll remember: {key} = {value}"
        return "Sure, I'll remember that. (Tip: say 'remember my X is Y' for best results.)"

    if intent == "recall":
        facts = get_all_memory(db)
        return f"Here's what I remember:\n{facts}" if facts else "I don't have any saved memories yet."

    # Reminders
    if intent == "set_reminder":
        return "Reminder feature: say 'remind me to X at HH:MM'. Full scheduler coming in Phase 5."

    if intent == "show_reminders":
        reminders = db.query(Reminder).filter(Reminder.is_done == False).all()
        if not reminders:
            return "No pending reminders."
        return "Reminders:\n" + "\n".join(
            f"• [{r.id}] {r.title} at {r.remind_at.strftime('%Y-%m-%d %H:%M')}" for r in reminders
        )

    return None  # falls through to LLM chat


def process_message(user_input: str, db: Session) -> str:
    """Main entry point — processes a user message and returns assistant reply."""
    if not user_input.strip():
        return "Please say or type something."

    # 1. Detect intent
    result = detect_intent(user_input)
    intent = result["intent"]
    logger.info(f"Intent: {intent} | Input: {user_input}")

    # 2. Save user turn
    save_conversation(db, "user", user_input)

    # 3. Try automation first
    auto_response = _handle_automation(intent, user_input, db)
    if auto_response:
        save_conversation(db, "assistant", auto_response)
        return auto_response

    # 4. Fall back to LLM
    history = get_recent_history(db, limit=10)
    memory_ctx = get_all_memory(db)
    reply = chat(history, user_input, memory_ctx)
    save_conversation(db, "assistant", reply)
    return reply
