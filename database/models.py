"""
Thunder AI — SQLAlchemy ORM Models
"""
from datetime import datetime
from sqlalchemy import (
    Column, Integer, String, Text, DateTime, Boolean, Float, create_engine
)
from sqlalchemy.orm import declarative_base, sessionmaker
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config.settings import DATABASE_URL

Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    id         = Column(Integer, primary_key=True, index=True)
    name       = Column(String(100), nullable=False, default="User")
    created_at = Column(DateTime, default=datetime.utcnow)

class ConversationHistory(Base):
    __tablename__ = "conversation_history"
    id         = Column(Integer, primary_key=True, index=True)
    role       = Column(String(20), nullable=False)   # user / assistant
    content    = Column(Text, nullable=False)
    timestamp  = Column(DateTime, default=datetime.utcnow)

class UserMemory(Base):
    __tablename__ = "user_memory"
    id         = Column(Integer, primary_key=True, index=True)
    key        = Column(String(255), nullable=False)
    value      = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

class Note(Base):
    __tablename__ = "notes"
    id         = Column(Integer, primary_key=True, index=True)
    title      = Column(String(255), nullable=False)
    content    = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

class Reminder(Base):
    __tablename__ = "reminders"
    id          = Column(Integer, primary_key=True, index=True)
    title       = Column(String(255), nullable=False)
    remind_at   = Column(DateTime, nullable=False)
    is_done     = Column(Boolean, default=False)
    created_at  = Column(DateTime, default=datetime.utcnow)

class InstalledApp(Base):
    __tablename__ = "installed_apps"
    id            = Column(Integer, primary_key=True, index=True)
    name          = Column(String(255), nullable=False)
    executable    = Column(String(512), nullable=False)

class SystemLog(Base):
    __tablename__ = "system_logs"
    id         = Column(Integer, primary_key=True, index=True)
    level      = Column(String(20), nullable=False)
    message    = Column(Text, nullable=False)
    timestamp  = Column(DateTime, default=datetime.utcnow)

class Setting(Base):
    __tablename__ = "settings"
    id    = Column(Integer, primary_key=True, index=True)
    key   = Column(String(255), unique=True, nullable=False)
    value = Column(Text, nullable=False)

class EmotionLog(Base):
    __tablename__ = "emotion_logs"
    id        = Column(Integer, primary_key=True, index=True)
    emotion   = Column(String(50), nullable=False)
    confidence= Column(Float, default=0.0)
    timestamp = Column(DateTime, default=datetime.utcnow)


# ── Engine & session ──────────────────────────────────────────────────────────
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def init_db() -> None:
    """Create all tables if they don't exist."""
    Base.metadata.create_all(bind=engine)

def get_db():
    """FastAPI dependency — yields a DB session."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
