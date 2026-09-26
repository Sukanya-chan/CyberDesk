"""Health check endpoint.

Verifies the API process is up and that the database connection layer
can be reached, without depending on any domain tables (none exist yet).
"""
from fastapi import APIRouter, Depends
from sqlalchemy import text
from sqlalchemy.orm import Session

from app.core.config import get_settings
from app.db.session import get_db

router = APIRouter(tags=["health"])


@router.get("/health")
def health_check(db: Session = Depends(get_db)) -> dict:
    """Return API and database status."""
    settings = get_settings()

    db_status = "ok"
    try:
        db.execute(text("SELECT 1"))
    except Exception:
        db_status = "error"

    return {
        "status": "ok",
        "service": settings.app_name,
        "environment": settings.environment,
        "database": db_status,
    }
