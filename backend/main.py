"""
Thunder AI — FastAPI Backend Entry Point
Run: uvicorn backend.main:app --host 127.0.0.1 --port 8000 --reload
"""
import logging
import sys
import os

# Make project root importable
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from database.models import init_db
from backend.routes.assistant import router as assistant_router
from backend.routes.memory import router as memory_router
from backend.routes.notes import router as notes_router
from backend.routes.history import router as history_router
from backend.routes.system import router as system_router
from config.settings import APP_NAME, APP_VERSION, DEBUG, LOG_DIR

# ── Logging ───────────────────────────────────────────────────────────────────
os.makedirs(LOG_DIR, exist_ok=True)
logging.basicConfig(
    level=logging.DEBUG if DEBUG else logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s — %(message)s",
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler(os.path.join(LOG_DIR, "thunder.log"), encoding="utf-8"),
    ],
)
logger = logging.getLogger(__name__)

# ── App ───────────────────────────────────────────────────────────────────────
app = FastAPI(
    title=APP_NAME,
    version=APP_VERSION,
    docs_url="/docs",
    redoc_url=None,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── DB Init ───────────────────────────────────────────────────────────────────
@app.on_event("startup")
def startup():
    logger.info(f"Starting {APP_NAME} v{APP_VERSION}")
    init_db()
    logger.info("Database initialized.")

# ── Routes ────────────────────────────────────────────────────────────────────
app.include_router(assistant_router)   # /api/assistant/chat + /listen + /speak + /status
app.include_router(memory_router)      # /api/memory
app.include_router(notes_router)       # /api/notes
app.include_router(history_router)     # /api/history
app.include_router(system_router)      # /api/system


@app.get("/")
def root():
    return {"app": APP_NAME, "version": APP_VERSION, "status": "running"}


@app.get("/health")
def health():
    return {"status": "ok"}
