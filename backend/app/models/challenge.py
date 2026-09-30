"""Safe cybersecurity challenge model for Phase 5."""
from datetime import datetime, timezone

from sqlalchemy import CheckConstraint, DateTime, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.db.session import Base

VALID_CHALLENGE_STATUSES = ("draft", "published")
VALID_CHALLENGE_DIFFICULTIES = ("easy", "medium", "hard")


class Challenge(Base):
    """A safe, flag-based cybersecurity challenge.

    Phase 5 explicitly forbids arbitrary submitted-code execution, external
    target scanning, malware execution, and credential theft. The challenge
    stores only a server-side hash of the expected flag; plaintext flags must
    never be returned by public APIs.
    """

    __tablename__ = "challenges"
    __table_args__ = (
        CheckConstraint(
            "status IN ('draft', 'published')",
            name="ck_challenges_status_valid",
        ),
        CheckConstraint(
            "difficulty IN ('easy', 'medium', 'hard')",
            name="ck_challenges_difficulty_valid",
        ),
        CheckConstraint("points > 0", name="ck_challenges_points_positive"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    slug: Mapped[str] = mapped_column(String(255), unique=True, nullable=False, index=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    instructions: Mapped[str | None] = mapped_column(Text, nullable=True)
    hint: Mapped[str | None] = mapped_column(Text, nullable=True)
    difficulty: Mapped[str] = mapped_column(String(16), nullable=False, default="easy")
    category: Mapped[str] = mapped_column(String(64), nullable=False, index=True)
    points: Mapped[int] = mapped_column(Integer, nullable=False, default=100)
    flag_hash: Mapped[str] = mapped_column(String(128), nullable=False)
    status: Mapped[str] = mapped_column(String(16), nullable=False, default="draft")

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )

    @property
    def is_published(self) -> bool:
        return self.status == "published"
