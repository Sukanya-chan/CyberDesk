"""Student quiz attempt and answer models for Phase 4."""
from datetime import datetime, timezone
from typing import TYPE_CHECKING
from sqlalchemy import DateTime, ForeignKey, Integer, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.session import Base

if TYPE_CHECKING:
    from app.models.quiz import Quiz
    from app.models.question import Question
    from app.models.question_option import QuestionOption
    from app.models.user import AppUser

class QuizAttempt(Base):
    __tablename__ = "quiz_attempts"
    id: Mapped[int] = mapped_column(primary_key=True)
    quiz_id: Mapped[int] = mapped_column(ForeignKey("quizzes.id", ondelete="CASCADE"), nullable=False, index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("app_users.id", ondelete="CASCADE"), nullable=False, index=True)
    score: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    total_questions: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    submitted_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    quiz: Mapped["Quiz"] = relationship("Quiz")
    user: Mapped["AppUser"] = relationship("AppUser")
    answers: Mapped[list["QuizAnswer"]] = relationship("QuizAnswer", back_populates="attempt", cascade="all, delete-orphan", order_by="QuizAnswer.id")

class QuizAnswer(Base):
    __tablename__ = "quiz_answers"
    __table_args__ = (UniqueConstraint("attempt_id", "question_id", name="uq_quiz_answers_attempt_question"),)
    id: Mapped[int] = mapped_column(primary_key=True)
    attempt_id: Mapped[int] = mapped_column(ForeignKey("quiz_attempts.id", ondelete="CASCADE"), nullable=False, index=True)
    question_id: Mapped[int] = mapped_column(ForeignKey("questions.id", ondelete="CASCADE"), nullable=False, index=True)
    selected_option_id: Mapped[int | None] = mapped_column(ForeignKey("question_options.id", ondelete="SET NULL"), nullable=True)
    is_correct: Mapped[bool] = mapped_column(nullable=False, default=False)
    attempt: Mapped["QuizAttempt"] = relationship("QuizAttempt", back_populates="answers")
    question: Mapped["Question"] = relationship("Question")
    selected_option: Mapped["QuestionOption | None"] = relationship("QuestionOption")
