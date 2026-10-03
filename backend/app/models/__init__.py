"""Import all ORM models so SQLAlchemy registers them on Base.metadata."""
from app.models.category import Category
from app.models.course import Course
from app.models.lesson import Lesson
from app.models.quiz import Quiz
from app.models.question import Question
from app.models.question_option import QuestionOption
from app.models.challenge import Challenge
from app.models.module import Module
from app.models.user import AppUser

__all__ = [
    "AppUser",
    "Category",
    "Course",
    "Module",
    "Lesson",
    "Quiz",
    "Question",
    "QuestionOption",
    "Challenge",
    "QuizAttempt",
    "QuizAnswer",
    "ChallengeSubmission",
    "LessonProgress",
]
from app.models.quiz_attempt import QuizAttempt, QuizAnswer
from app.models.challenge_submission import ChallengeSubmission
from app.models.lesson_progress import LessonProgress
