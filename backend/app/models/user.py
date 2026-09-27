"""Minimal local application-user model.

Clerk is the source of truth for identity (email, name, password, sessions).
This table intentionally does NOT duplicate that profile data — see
context/Decisions.md (ADR-006, ADR-007) for the rationale. It stores only
what CyberDesk itself needs: the link to Clerk, the application role, and
timestamps, so future tables (progress, quiz attempts, challenge
submissions) have a stable local integer FK to join against.
"""
from datetime import datetime, timezone

from sqlalchemy import DateTime, String
from sqlalchemy.orm import Mapped, mapped_column

from app.db.session import Base

VALID_ROLES = ("student", "admin")


class AppUser(Base):
    """A CyberDesk application user, linked 1:1 with a Clerk identity."""

    __tablename__ = "app_users"

    id: Mapped[int] = mapped_column(primary_key=True)
    clerk_user_id: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    role: Mapped[str] = mapped_column(String(32), default="student", nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )
