"""Lesson model — the leaf of the Category -> Course -> Module -> Lesson tree."""
from datetime import datetime, timezone
from typing import TYPE_CHECKING

from sqlalchemy import (
    CheckConstraint,
    DateTime,
    ForeignKey,
    ForeignKeyConstraint,
    Integer,
    String,
    Text,
    UniqueConstraint,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.session import Base

if TYPE_CHECKING:
    from app.models.module import Module


class Lesson(Base):
    """A single piece of learning content within a module."""

    __tablename__ = "lessons"
    __table_args__ = (
        # course_id is denormalized (always derived server-side from the
        # lesson's module — see the learning service layer, added in 3B)
        # purely so course-scoped queries and this uniqueness constraint
        # don't require a join through modules. This composite FK is what
        # makes "a lesson's module must belong to the same course" a real
        # database constraint, not just an application-level check: SQLite
        # rejects, at the FK-enforcement layer, any row whose
        # (module_id, course_id) pair doesn't match an existing
        # (modules.id, modules.course_id) pair — i.e. a lesson can never
        # reference a module belonging to a different course.
        ForeignKeyConstraint(
            ["module_id", "course_id"],
            ["modules.id", "modules.course_id"],
            name="fk_lessons_module_course",
            ondelete="CASCADE",
        ),
        UniqueConstraint("course_id", "slug", name="uq_lessons_course_id_slug"),
        CheckConstraint(
            "status IN ('draft', 'published')", name="ck_lessons_status_valid"
        ),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    module_id: Mapped[int] = mapped_column(nullable=False, index=True)
    course_id: Mapped[int] = mapped_column(nullable=False, index=True)

    slug: Mapped[str] = mapped_column(String(255), nullable=False)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False, default="")

    position: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    status: Mapped[str] = mapped_column(String(16), nullable=False, default="draft")

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )

    module: Mapped["Module"] = relationship(
        "Module", back_populates="lessons", foreign_keys=[module_id]
    )

    @property
    def is_published(self) -> bool:
        return self.status == "published"
