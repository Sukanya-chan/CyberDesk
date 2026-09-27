# Domain models (Course, Lesson, Quiz, etc.) are intentionally not
# implemented yet. See specs/DATABASE.md for the target schema.
# Each model module is added in the phase that implements its module,
# per context/Decisions.md (ADR-005: vertical slices).
#
# Importing model modules here ensures they register on Base.metadata
# before create_all() (or a future migration tool) runs.
from app.models.user import AppUser  # noqa: F401
