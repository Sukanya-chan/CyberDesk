"""Admin-only CRUD API for Phase 3 learning content."""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.deps import require_role
from app.db.session import get_db
from app.models.category import Category
from app.schemas.learning import (
    AdminLessonResponse,
    AdminModuleResponse,
    CategoryCreate,
    CategoryResponse,
    CategoryUpdate,
    CourseCreate,
    CourseSummary,
    CourseUpdate,
    LessonCreate,
    LessonResponse,
    LessonUpdate,
    ModuleCreate,
    ModuleUpdate,
    ReorderRequest,
)
from app.services import learning as svc

router = APIRouter(
    prefix="/admin",
    tags=["admin-learning"],
    dependencies=[Depends(require_role("admin"))],
)


def _raise(exc: svc.LearningError):
    raise HTTPException(status_code=exc.status_code, detail=exc.message)


@router.get("/categories", response_model=list[CategoryResponse])
def categories(db: Session = Depends(get_db)):
    return list(db.query(Category).order_by(Category.name).all())


@router.post("/categories", response_model=CategoryResponse, status_code=status.HTTP_201_CREATED)
def create_category(payload: CategoryCreate, db: Session = Depends(get_db)):
    try:
        return svc.create_category(db, payload.name, payload.description)
    except svc.LearningError as exc:
        _raise(exc)


@router.patch("/categories/{category_id}", response_model=CategoryResponse)
def update_category(category_id: int, payload: CategoryUpdate, db: Session = Depends(get_db)):
    try:
        return svc.update_category(db, category_id, payload.model_dump(exclude_unset=True))
    except svc.LearningError as exc:
        _raise(exc)


@router.delete("/categories/{category_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_category(category_id: int, db: Session = Depends(get_db)):
    try:
        svc.delete_category(db, category_id)
    except svc.LearningError as exc:
        _raise(exc)


@router.get("/courses", response_model=list[CourseSummary])
def courses(db: Session = Depends(get_db)):
    return [
        CourseSummary(
            id=c.id, category_id=c.category_id, category_name=c.category.name,
            slug=c.slug, title=c.title, description=c.description
        )
        for c in svc.admin_courses(db)
    ]


@router.post("/courses", response_model=CourseSummary, status_code=status.HTTP_201_CREATED)
def create_course(payload: CourseCreate, db: Session = Depends(get_db)):
    try:
        c = svc.create_course(db, payload.model_dump())
        db.refresh(c)
        return CourseSummary(
            id=c.id, category_id=c.category_id, category_name=c.category.name,
            slug=c.slug, title=c.title, description=c.description
        )
    except svc.LearningError as exc:
        _raise(exc)


@router.patch("/courses/{course_id}", response_model=CourseSummary)
def update_course(course_id: int, payload: CourseUpdate, db: Session = Depends(get_db)):
    try:
        c = svc.update_course(db, course_id, payload.model_dump(exclude_unset=True))
        return CourseSummary(
            id=c.id, category_id=c.category_id, category_name=c.category.name,
            slug=c.slug, title=c.title, description=c.description
        )
    except svc.LearningError as exc:
        _raise(exc)


@router.delete("/courses/{course_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_course(course_id: int, db: Session = Depends(get_db)):
    try:
        svc.delete_course(db, course_id)
    except svc.LearningError as exc:
        _raise(exc)


@router.get("/courses/{course_id}/modules", response_model=list[AdminModuleResponse])
def modules(course_id: int, db: Session = Depends(get_db)):
    try:
        return svc.admin_modules(db, course_id)
    except svc.LearningError as exc:
        _raise(exc)


@router.post("/modules", response_model=AdminModuleResponse, status_code=status.HTTP_201_CREATED)
def create_module(payload: ModuleCreate, db: Session = Depends(get_db)):
    try:
        return svc.create_module(db, payload.model_dump())
    except svc.LearningError as exc:
        _raise(exc)


@router.patch("/modules/{module_id}", response_model=AdminModuleResponse)
def update_module(module_id: int, payload: ModuleUpdate, db: Session = Depends(get_db)):
    try:
        return svc.update_module(db, module_id, payload.model_dump(exclude_unset=True))
    except svc.LearningError as exc:
        _raise(exc)


@router.delete("/modules/{module_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_module(module_id: int, db: Session = Depends(get_db)):
    try:
        svc.delete_module(db, module_id)
    except svc.LearningError as exc:
        _raise(exc)


@router.patch("/courses/{course_id}/modules/reorder", response_model=list[AdminModuleResponse])
def reorder_modules(course_id: int, payload: ReorderRequest, db: Session = Depends(get_db)):
    try:
        return svc.reorder_modules(db, course_id, payload.ordered_ids)
    except svc.LearningError as exc:
        _raise(exc)


@router.get("/modules/{module_id}/lessons", response_model=list[AdminLessonResponse])
def lessons(module_id: int, db: Session = Depends(get_db)):
    try:
        return svc.admin_lessons(db, module_id)
    except svc.LearningError as exc:
        _raise(exc)


@router.post("/lessons", response_model=AdminLessonResponse, status_code=status.HTTP_201_CREATED)
def create_lesson(payload: LessonCreate, db: Session = Depends(get_db)):
    try:
        return svc.create_lesson(db, payload.model_dump())
    except svc.LearningError as exc:
        _raise(exc)


@router.patch("/lessons/{lesson_id}", response_model=AdminLessonResponse)
def update_lesson(lesson_id: int, payload: LessonUpdate, db: Session = Depends(get_db)):
    try:
        return svc.update_lesson(db, lesson_id, payload.model_dump(exclude_unset=True))
    except svc.LearningError as exc:
        _raise(exc)


@router.delete("/lessons/{lesson_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_lesson(lesson_id: int, db: Session = Depends(get_db)):
    try:
        svc.delete_lesson(db, lesson_id)
    except svc.LearningError as exc:
        _raise(exc)


@router.patch("/modules/{module_id}/lessons/reorder", response_model=list[AdminLessonResponse])
def reorder_lessons(module_id: int, payload: ReorderRequest, db: Session = Depends(get_db)):
    try:
        return svc.reorder_lessons(db, module_id, payload.ordered_ids)
    except svc.LearningError as exc:
        _raise(exc)
