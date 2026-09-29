# Domain models are added in the phase that implements their area, per
# context/Decisions.md (ADR-005: vertical slices). Quiz/Challenge/Progress
# models remain unimplemented until their own phases.
#
# Importing model modules here ensures they register on Base.metadata
# before create_all() (or a future migration tool) runs. Import order
# follows the FK dependency chain (Category -> Course -> Module -> Lesson)
# for readability; SQLAlchemy's mapper configuration doesn't actually
# require this order since string-based relationship() targets and
# TYPE_CHECKING-only imports avoid circular-import issues.
from app.models.user import AppUser  # noqa: F401
from app.models.category import Category  # noqa: F401
from app.models.course import Course  # noqa: F401
from app.models.module import Module  # noqa: F401
from app.models.lesson import Lesson  # noqa: F401
