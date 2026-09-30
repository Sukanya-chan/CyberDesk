"""Answer-option model for Phase 4 MCQ questions."""
from datetime import datetime, timezone
from typing import TYPE_CHECKING

from sqlalchemy import Boolean, CheckConstraint, DateTime, ForeignKey, Integer, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.session import Base

if TYPE_CHECKING:
    from app.models.question import Question


class QuestionOption(Base):
    """One selectable option for an MCQ question.

    ``is_correct`` is private server-side assessment data. Exactly one correct
    option per question will be enforced by the Phase 4 service layer during
    create/update validation; a cross-row SQL CHECK cannot enforce that rule.
    """

    __tablename__ = "question_options"
    __table_args__ = (
        CheckConstraint("position >= 0", name="ck_question_options_position_nonnegative"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    question_id: Mapped[int] = mapped_column(
        ForeignKey("questions.id", ondelete="CASCADE"), nullable=False, index=True
    )
    option_text: Mapped[str] = mapped_column(Text, nullable=False)
    position: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    is_correct: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )

    question: Mapped["Question"] = relationship("Question", back_populates="options")
