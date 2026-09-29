"""Module model — sits between Course and Lesson.

Modules have no draft/published state of their own: "A published course's
module must remain visible even when every lesson inside it is draft" (see
Phase 3 spec), so visibility is derived purely from the parent Course's
status and each Lesson's own status, not from anything stored here.
"""
from datetime import datetime, timezone
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, ForeignKey, Integer, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.session import Base

if TYPE_CHECKING:
    from app.models.course import Course
    from app.models.lesson import Lesson


class Module(Base):
    """A module groups an ordered set of lessons within one course."""

    __tablename__ = "modules"
    __table_args__ = (
        # A plain UNIQUE constraint on (id, course_id), even though `id`
        # alone is already unique as the primary key. This exists solely so
        # Lesson can declare a composite FK against (module_id, course_id)
        # -> (modules.id, modules.course_id): SQLite requires the
        # referenced column set to be covered by an explicit unique index,
        # and this is what makes "a lesson cannot reference a module
        # belonging to another course" an enforced DB constraint rather
        # than just an application-level check.
        UniqueConstraint("id", "course_id", name="uq_modules_id_course_id"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    course_id: Mapped[int] = mapped_column(
        ForeignKey("courses.id", ondelete="CASCADE"), nullable=False, index=True
    )

    title: Mapped[str] = mapped_column(String(255), nullable=False)
    position: Mapped[int] = mapped_column(Integer, nullable=False, default=0)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )

    course: Mapped["Course"] = relationship("Course", back_populates="modules")

    lessons: Mapped[list["Lesson"]] = relationship(
        "Lesson",
        back_populates="module",
        cascade="all, delete-orphan",
        order_by="Lesson.position",
        foreign_keys="Lesson.module_id",
    )
