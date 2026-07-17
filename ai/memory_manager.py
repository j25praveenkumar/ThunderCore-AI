"""
Thunder AI — Memory Manager
Handles reading/writing user memory facts from the database.
"""
from sqlalchemy.orm import Session
from database.models import UserMemory, ConversationHistory
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


def save_memory(db: Session, key: str, value: str) -> None:
    """Save or update a user memory fact."""
    existing = db.query(UserMemory).filter(UserMemory.key == key).first()
    if existing:
        existing.value = value
    else:
        db.add(UserMemory(key=key, value=value))
    db.commit()
    logger.info(f"Memory saved: {key} = {value}")


def get_all_memory(db: Session) -> str:
    """Return all memory facts as a formatted string for LLM context."""
    facts = db.query(UserMemory).all()
    if not facts:
        return ""
    return "\n".join(f"- {f.key}: {f.value}" for f in facts)


def delete_memory(db: Session, key: str) -> bool:
    """Delete a memory fact by key."""
    item = db.query(UserMemory).filter(UserMemory.key == key).first()
    if item:
        db.delete(item)
        db.commit()
        return True
    return False


def save_conversation(db: Session, role: str, content: str) -> None:
    """Persist a single conversation turn."""
    db.add(ConversationHistory(role=role, content=content, timestamp=datetime.utcnow()))
    db.commit()


def get_recent_history(db: Session, limit: int = 20):
    """Return recent conversation history as list of dicts."""
    rows = (
        db.query(ConversationHistory)
        .order_by(ConversationHistory.timestamp.desc())
        .limit(limit)
        .all()
    )
    return [{"role": r.role, "content": r.content} for r in reversed(rows)]
