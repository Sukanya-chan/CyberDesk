"""Public learning-content API."""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.learning import (
    CategoryResponse,
    CourseDetail,
    CourseSummary,
    LessonResponse,
    LessonSummary,
    ModuleResponse,
)
from app.services.learning import LearningError, public_categories, public_course, public_courses, public_lesson

router = APIRouter(tags=["learning"])


def _error(exc: LearningError):
    from fastapi import HTTPException
    raise HTTPException(status_code=exc.status_code, detail=exc.message)


@router.get("/categories", response_model=list[CategoryResponse])
def list_categories(db: Session = Depends(get_db)):
    return public_categories(db)


@router.get("/courses", response_model=list[CourseSummary])
def list_courses(db: Session = Depends(get_db)):
    courses = public_courses(db)
    return [
        CourseSummary(
            id=c.id,
            category_id=c.category_id,
            category_name=c.category.name,
            slug=c.slug,
            title=c.title,
            description=c.description,
        )
        for c in courses
    ]


@router.get("/courses/{course_slug}", response_model=CourseDetail)
def read_course(course_slug: str, db: Session = Depends(get_db)):
    try:
        course = public_course(db, course_slug)
    except LearningError as exc:
        _error(exc)
    modules = []
    for module in sorted(course.modules, key=lambda item: item.position):
        lessons = [
            LessonSummary(id=l.id, slug=l.slug, title=l.title, position=l.position)
            for l in sorted(module.lessons, key=lambda item: item.position)
            if l.status == "published"
        ]
        modules.append(
            ModuleResponse(
                id=module.id,
                course_id=module.course_id,
                title=module.title,
                position=module.position,
                lessons=lessons,
            )
        )
    return CourseDetail(
        id=course.id,
        category_id=course.category_id,
        category_name=course.category.name,
        slug=course.slug,
        title=course.title,
        description=course.description,
        modules=modules,
    )


@router.get("/lessons/{course_slug}/{lesson_slug}", response_model=LessonResponse)
def read_lesson(course_slug: str, lesson_slug: str, db: Session = Depends(get_db)):
    try:
        return public_lesson(db, course_slug, lesson_slug)
    except LearningError as exc:
        _error(exc)
