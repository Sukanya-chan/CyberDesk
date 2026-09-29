"""Database connection layer.

Phase 1 only establishes the connection/session foundation. No domain
tables are defined yet — those arrive with the modules that need them,
each via a documented migration/decision (see context/Decisions.md).
"""
from collections.abc import Generator

from sqlalchemy import create_engine, event
from sqlalchemy.engine import Engine
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker

from app.core.config import get_settings

settings = get_settings()

# check_same_thread=False is required for SQLite when accessed across
# FastAPI's request-handling threads; it is a no-op for other DB backends,
# which keeps this compatible with a future PostgreSQL migration.
connect_args = (
    {"check_same_thread": False} if settings.database_url.startswith("sqlite") else {}
)

engine = create_engine(settings.database_url, connect_args=connect_args)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# SQLite does not enforce FOREIGN KEY constraints by default; it silently
# accepts inserts/updates that violate them unless this pragma is set on
# every new DBAPI connection. Phase 3 relies on FK enforcement (e.g. the
# composite Lesson -> Module/Course constraint), so this must be enabled
# here rather than left as an app-level assumption. No-op for non-SQLite
# backends (e.g. a future PostgreSQL migration), which enforce FKs natively.
@event.listens_for(Engine, "connect")
def _set_sqlite_pragma(dbapi_connection, connection_record) -> None:  # noqa: ANN001
    if not settings.database_url.startswith("sqlite"):
        return
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()


class Base(DeclarativeBase):
    """Shared declarative base for future ORM models."""


def get_db() -> Generator[Session, None, None]:
    """FastAPI dependency that yields a request-scoped DB session."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
