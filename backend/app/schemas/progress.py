"""Progress and dashboard response schemas."""
from datetime import datetime
from pydantic import BaseModel, ConfigDict

class LessonProgressResponse(BaseModel):
    lesson_id: int
    completed: bool
    completed_at: datetime | None = None

class CourseProgress(BaseModel):
    course_id: int
    course_slug: str
    title: str
    completed_lessons: int
    total_lessons: int
    percent: int

class DashboardResponse(BaseModel):
    completed_lessons: int
    total_lessons: int
    lesson_percent: int
    quiz_attempts: int
    best_quiz_score: int | None
    solved_challenges: int
    challenge_points: int
    courses: list[CourseProgress]
    recent_course_slug: str | None = None
    model_config = ConfigDict(from_attributes=True)
