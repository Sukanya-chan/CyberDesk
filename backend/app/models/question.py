"""Question model for Phase 4 multiple-choice assessments."""
from datetime import datetime, timezone
from typing import TYPE_CHECKING

from sqlalchemy import CheckConstraint, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.session import Base

if TYPE_CHECKING:
    from app.models.quiz import Quiz
    from app.models.question_option import QuestionOption


class Question(Base):
    """A single MCQ question inside a Quiz.

    The correctness of options is intentionally a server-side field. Public
    quiz schemas in later phases must omit ``is_correct`` until submission.
    """

    __tablename__ = "questions"
    __table_args__ = (
        CheckConstraint("type = 'mcq'", name="ck_questions_type_mcq"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    quiz_id: Mapped[int] = mapped_column(
        ForeignKey("quizzes.id", ondelete="CASCADE"), nullable=False, index=True
    )
    question_text: Mapped[str] = mapped_column(Text, nullable=False)
    type: Mapped[str] = mapped_column(String(16), nullable=False, default="mcq")
    position: Mapped[int] = mapped_column(Integer, nullable=False, default=0)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )

    quiz: Mapped["Quiz"] = relationship("Quiz", back_populates="questions")
    options: Mapped[list["QuestionOption"]] = relationship(
        "QuestionOption",
        back_populates="question",
        cascade="all, delete-orphan",
        order_by="QuestionOption.position",
    )
