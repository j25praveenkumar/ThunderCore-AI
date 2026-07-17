"""
Thunder AI — Conversation History API Routes
"""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database.models import get_db, ConversationHistory

router = APIRouter(prefix="/api/history", tags=["history"])


@router.get("")
def get_history(limit: int = 50, db: Session = Depends(get_db)):
    rows = (
        db.query(ConversationHistory)
        .order_by(ConversationHistory.timestamp.asc())
        .limit(limit)
        .all()
    )
    return [{"id": r.id, "role": r.role, "content": r.content,
             "timestamp": str(r.timestamp)} for r in rows]


@router.delete("")
def clear_history(db: Session = Depends(get_db)):
    db.query(ConversationHistory).delete()
    db.commit()
    return {"status": "history cleared"}
