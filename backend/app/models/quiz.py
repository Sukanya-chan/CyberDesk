"""Assessment foundation models for Phase 4.

MVP assessment scope is multiple-choice quizzes. Correct answers are stored
server-side and must not be exposed by public response schemas.
"""
from datetime import datetime, timezone
from typing import TYPE_CHECKING

from sqlalchemy import CheckConstraint, DateTime, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.session import Base

if TYPE_CHECKING:
    from app.models.course import Course
    from app.models.question import Question

VALID_ASSESSMENT_STATUSES = ("draft", "published")


class Quiz(Base):
    """A multiple-choice assessment associated with one course."""

    __tablename__ = "quizzes"
    __table_args__ = (
        CheckConstraint(
            "status IN ('draft', 'published')",
            name="ck_quizzes_status_valid",
        ),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    course_id: Mapped[int] = mapped_column(
        ForeignKey("courses.id", ondelete="CASCADE"), nullable=False, index=True
    )
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    status: Mapped[str] = mapped_column(String(16), nullable=False, default="draft")

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )

    course: Mapped["Course"] = relationship("Course")
    questions: Mapped[list["Question"]] = relationship(
        "Question",
        back_populates="quiz",
        cascade="all, delete-orphan",
        order_by="Question.position",
    )

    @property
    def is_published(self) -> bool:
        return self.status == "published"
