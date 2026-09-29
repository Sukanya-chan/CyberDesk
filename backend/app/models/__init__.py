"""Import all ORM models so SQLAlchemy registers them on Base.metadata."""
from app.models.category import Category
from app.models.course import Course
from app.models.lesson import Lesson
from app.models.module import Module
from app.models.user import AppUser

__all__ = ["AppUser", "Category", "Course", "Module", "Lesson"]
