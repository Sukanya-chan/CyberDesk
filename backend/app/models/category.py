"""Category model — the top of the learning-content hierarchy.

Category -> Course -> Module -> Lesson (see specs/LEARNING_SYSTEM.md and
the Phase 3 spec). A Category has no draft/published state of its own;
visibility is governed entirely by its child Courses/Lessons.
"""
from datetime import datetime, timezone
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.session import Base

if TYPE_CHECKING:
    from app.models.course import Course


class Category(Base):
    """A top-level grouping of courses (e.g. "Web Security", "Networking")."""

    __tablename__ = "categories"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(255), unique=True, nullable=False, index=True)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )

    # No delete cascade: a Category with existing Courses must be rejected
    # with 409 CATEGORY_HAS_COURSES by the service layer, not silently wipe
    # its courses. The FK itself uses ondelete="RESTRICT" (see Course.
    # category_id) as a DB-level backstop against that same mistake.
    courses: Mapped[list["Course"]] = relationship(
        "Course",
        back_populates="category",
        order_by="Course.id",
    )
