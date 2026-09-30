"""Challenge submissions for safe flag-based validation."""
from datetime import datetime, timezone
from typing import TYPE_CHECKING
from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.session import Base
if TYPE_CHECKING:
    from app.models.challenge import Challenge
    from app.models.user import AppUser
class ChallengeSubmission(Base):
    __tablename__ = "challenge_submissions"
    id: Mapped[int] = mapped_column(primary_key=True)
    challenge_id: Mapped[int] = mapped_column(ForeignKey("challenges.id", ondelete="CASCADE"), nullable=False, index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("app_users.id", ondelete="CASCADE"), nullable=False, index=True)
    submitted_hash: Mapped[str] = mapped_column(String(128), nullable=False)
    is_correct: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    points_awarded: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    submitted_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    challenge: Mapped["Challenge"] = relationship("Challenge")
    user: Mapped["AppUser"] = relationship("AppUser")
