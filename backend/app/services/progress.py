"""Authoritative student progress aggregation and completion rules."""
from sqlalchemy import func
from sqlalchemy.orm import Session
from app.models.lesson import Lesson
from app.models.course import Course
from app.models.lesson_progress import LessonProgress
from app.models.quiz_attempt import QuizAttempt
from app.models.challenge_submission import ChallengeSubmission
from app.models.challenge import Challenge
from app.models.user import AppUser

class ProgressError(Exception):
    def __init__(self, status_code: int, message: str):
        self.status_code = status_code
        self.message = message

def complete_lesson(db: Session, user: AppUser, lesson_id: int) -> LessonProgress:
    lesson = db.get(Lesson, lesson_id)
    if not lesson or lesson.status != "published":
        raise ProgressError(404, "Published lesson not found.")
    course = db.get(Course, lesson.course_id)
    if not course or course.status != "published":
        raise ProgressError(404, "Published lesson not found.")
    existing = db.query(LessonProgress).filter_by(user_id=user.id, lesson_id=lesson.id).first()
    if existing:
        return existing
    row = LessonProgress(user_id=user.id, lesson_id=lesson.id)
    db.add(row)
    db.commit()
    db.refresh(row)
    return row

def lesson_status(db: Session, user: AppUser, lesson_id: int) -> LessonProgress | None:
    return db.query(LessonProgress).filter_by(user_id=user.id, lesson_id=lesson_id).first()

def dashboard(db: Session, user: AppUser) -> dict:
    published_lessons = (
        db.query(Lesson)
        .join(Course, Lesson.course_id == Course.id)
        .filter(Lesson.status == "published", Course.status == "published")
        .all()
    )
    total = len(published_lessons)
    completed_ids = {
        row.lesson_id for row in db.query(LessonProgress).filter_by(user_id=user.id).all()
    }
    completed = sum(1 for lesson in published_lessons if lesson.id in completed_ids)

    courses = []
    for course in db.query(Course).filter(Course.status == "published").order_by(Course.id).all():
        lessons = [l for l in course.modules for l in l.lessons if l.status == "published"]
        count = sum(1 for l in lessons if l.id in completed_ids)
        courses.append({
            "course_id": course.id,
            "course_slug": course.slug,
            "title": course.title,
            "completed_lessons": count,
            "total_lessons": len(lessons),
            "percent": round((count / len(lessons)) * 100) if lessons else 0,
        })

    attempts = db.query(QuizAttempt).filter_by(user_id=user.id).all()
    best = max((a.score for a in attempts), default=None)
    solved_rows = (
        db.query(ChallengeSubmission)
        .join(Challenge, ChallengeSubmission.challenge_id == Challenge.id)
        .filter(
            ChallengeSubmission.user_id == user.id,
            ChallengeSubmission.is_correct.is_(True),
            Challenge.status == "published",
        )
        .all()
    )
    solved_ids = {r.challenge_id for r in solved_rows}
    points = sum(db.get(Challenge, cid).points for cid in solved_ids if db.get(Challenge, cid))
    recent = None
    latest = (
        db.query(LessonProgress)
        .filter_by(user_id=user.id)
        .order_by(LessonProgress.completed_at.desc())
        .first()
    )
    if latest:
        lesson = db.get(Lesson, latest.lesson_id)
        if lesson:
            course = db.get(Course, lesson.course_id)
            recent = course.slug if course else None

    return {
        "completed_lessons": completed,
        "total_lessons": total,
        "lesson_percent": round((completed / total) * 100) if total else 0,
        "quiz_attempts": len(attempts),
        "best_quiz_score": best,
        "solved_challenges": len(solved_ids),
        "challenge_points": points,
        "courses": courses,
        "recent_course_slug": recent,
    }
