"""FastAPI application and static frontend hosting."""

from pathlib import Path

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app.api.routes import router as api_router
from app.api.data import router as data_router
from app.api.research import router as research_router
from app.api.documents import router as documents_router
from app.api.automation import router as automation_router

ROOT_DIR = Path(__file__).resolve().parents[2]
FRONTEND_DIR = ROOT_DIR / "frontend"

app = FastAPI(
    title="Solution Studio API",
    description="Local-first toolkit for custom digital solutions.",
    version="0.1.0",
)

app.include_router(api_router, prefix="/api")
app.include_router(data_router, prefix="/api")
app.include_router(research_router, prefix="/api")
app.include_router(documents_router, prefix="/api")
app.include_router(automation_router, prefix="/api")

# Serve the browser app from the same origin so local development needs no
# separate frontend server or permissive cross-origin configuration.
app.mount("/", StaticFiles(directory=FRONTEND_DIR, html=True), name="frontend")
