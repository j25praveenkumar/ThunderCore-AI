"""
Thunder AI — Memory API Routes
"""
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from database.models import get_db, UserMemory

router = APIRouter(prefix="/api/memory", tags=["memory"])


class MemoryItem(BaseModel):
    key: str
    value: str


@router.get("")
def list_memory(db: Session = Depends(get_db)):
    items = db.query(UserMemory).all()
    return [{"id": m.id, "key": m.key, "value": m.value} for m in items]


@router.post("")
def add_memory(item: MemoryItem, db: Session = Depends(get_db)):
    existing = db.query(UserMemory).filter(UserMemory.key == item.key).first()
    if existing:
        existing.value = item.value
    else:
        db.add(UserMemory(key=item.key, value=item.value))
    db.commit()
    return {"status": "saved", "key": item.key, "value": item.value}


@router.delete("/{memory_id}")
def delete_memory(memory_id: int, db: Session = Depends(get_db)):
    item = db.query(UserMemory).filter(UserMemory.id == memory_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Memory not found")
    db.delete(item)
    db.commit()
    return {"status": "deleted"}
