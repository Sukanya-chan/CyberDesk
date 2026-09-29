"""Business logic for CyberDesk learning content."""
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session, selectinload

from app.models.category import Category
from app.models.course import Course
from app.models.lesson import Lesson
from app.models.module import Module


class LearningError(Exception):
    def __init__(self, status_code: int, message: str):
        self.status_code = status_code
        self.message = message
        super().__init__(message)


def _commit(db: Session) -> None:
    try:
        db.commit()
    except IntegrityError as exc:
        db.rollback()
        raise LearningError(409, "Resource conflicts with existing data") from exc


def get_category(db: Session, category_id: int) -> Category:
    category = db.get(Category, category_id)
    if category is None:
        raise LearningError(404, "Category not found")
    return category


def create_category(db: Session, name: str, description: str | None) -> Category:
    category = Category(name=name, description=description)
    db.add(category)
    _commit(db)
    db.refresh(category)
    return category


def update_category(db: Session, category_id: int, data: dict) -> Category:
    category = get_category(db, category_id)
    for key, value in data.items():
        setattr(category, key, value)
    _commit(db)
    db.refresh(category)
    return category


def delete_category(db: Session, category_id: int) -> None:
    category = get_category(db, category_id)
    if db.scalar(select(Course.id).where(Course.category_id == category_id).limit(1)) is not None:
        raise LearningError(409, "CATEGORY_HAS_COURSES")
    db.delete(category)
    _commit(db)


def get_course(db: Session, course_id: int) -> Course:
    course = db.get(Course, course_id)
    if course is None:
        raise LearningError(404, "Course not found")
    return course


def create_course(db: Session, data: dict) -> Course:
    get_category(db, data["category_id"])
    course = Course(**data)
    db.add(course)
    _commit(db)
    db.refresh(course)
    return course


def update_course(db: Session, course_id: int, data: dict) -> Course:
    course = get_course(db, course_id)
    if "category_id" in data:
        get_category(db, data["category_id"])
    for key, value in data.items():
        setattr(course, key, value)
    _commit(db)
    db.refresh(course)
    return course


def delete_course(db: Session, course_id: int) -> None:
    course = get_course(db, course_id)
    db.delete(course)
    _commit(db)


def get_module(db: Session, module_id: int) -> Module:
    module = db.get(Module, module_id)
    if module is None:
        raise LearningError(404, "Module not found")
    return module


def create_module(db: Session, data: dict) -> Module:
    course = get_course(db, data["course_id"])
    position = data.get("position")
    if position is None:
        position = (max((m.position for m in course.modules), default=-1) + 1)
    module = Module(course_id=course.id, title=data["title"], position=position)
    db.add(module)
    _commit(db)
    db.refresh(module)
    return module


def update_module(db: Session, module_id: int, data: dict) -> Module:
    module = get_module(db, module_id)
    for key, value in data.items():
        setattr(module, key, value)
    _commit(db)
    db.refresh(module)
    return module


def delete_module(db: Session, module_id: int) -> None:
    module = get_module(db, module_id)
    db.delete(module)
    _commit(db)


def get_lesson(db: Session, lesson_id: int) -> Lesson:
    lesson = db.get(Lesson, lesson_id)
    if lesson is None:
        raise LearningError(404, "Lesson not found")
    return lesson


def create_lesson(db: Session, data: dict) -> Lesson:
    module = get_module(db, data["module_id"])
    position = data.get("position")
    if position is None:
        position = max((l.position for l in module.lessons), default=-1) + 1
    lesson = Lesson(
        module_id=module.id,
        course_id=module.course_id,
        slug=data["slug"],
        title=data["title"],
        content=data["content"],
        position=position,
        status=data.get("status", "draft"),
    )
    db.add(lesson)
    _commit(db)
    db.refresh(lesson)
    return lesson


def update_lesson(db: Session, lesson_id: int, data: dict) -> Lesson:
    lesson = get_lesson(db, lesson_id)
    if "module_id" in data:
        module = get_module(db, data["module_id"])
        lesson.module_id = module.id
        lesson.course_id = module.course_id
    for key, value in data.items():
        if key != "module_id":
            setattr(lesson, key, value)
    _commit(db)
    db.refresh(lesson)
    return lesson


def delete_lesson(db: Session, lesson_id: int) -> None:
    lesson = get_lesson(db, lesson_id)
    db.delete(lesson)
    _commit(db)


def reorder_modules(db: Session, course_id: int, ordered_ids: list[int]) -> list[Module]:
    get_course(db, course_id)
    modules = list(db.scalars(select(Module).where(Module.course_id == course_id)).all())
    actual = {m.id for m in modules}
    if actual != set(ordered_ids):
        raise LearningError(400, "ordered_ids must contain every module exactly once")
    by_id = {m.id: m for m in modules}
    for index, item_id in enumerate(ordered_ids):
        by_id[item_id].position = index
    db.commit()
    return sorted(modules, key=lambda m: m.position)


def reorder_lessons(db: Session, module_id: int, ordered_ids: list[int]) -> list[Lesson]:
    module = get_module(db, module_id)
    lessons = list(db.scalars(select(Lesson).where(Lesson.module_id == module.id)).all())
    actual = {l.id for l in lessons}
    if actual != set(ordered_ids):
        raise LearningError(400, "ordered_ids must contain every lesson exactly once")
    by_id = {l.id: l for l in lessons}
    for index, item_id in enumerate(ordered_ids):
        by_id[item_id].position = index
    db.commit()
    return sorted(lessons, key=lambda l: l.position)


def public_categories(db: Session) -> list[Category]:
    stmt = (
        select(Category)
        .join(Course)
        .where(Course.status == "published")
        .distinct()
        .order_by(Category.name)
    )
    return list(db.scalars(stmt).all())


def public_courses(db: Session) -> list[Course]:
    stmt = (
        select(Course)
        .options(selectinload(Course.category))
        .where(Course.status == "published")
        .order_by(Course.title)
    )
    return list(db.scalars(stmt).all())


def public_course(db: Session, slug: str) -> Course:
    stmt = (
        select(Course)
        .options(
            selectinload(Course.category),
            selectinload(Course.modules).selectinload(Module.lessons),
        )
        .where(Course.slug == slug, Course.status == "published")
    )
    course = db.scalar(stmt)
    if course is None:
        raise LearningError(404, "Course not found")
    return course


def public_lesson(db: Session, course_slug: str, lesson_slug: str) -> Lesson:
    stmt = (
        select(Lesson)
        .join(Course, Lesson.course_id == Course.id)
        .options(selectinload(Lesson.module))
        .where(
            Course.slug == course_slug,
            Course.status == "published",
            Lesson.slug == lesson_slug,
            Lesson.status == "published",
        )
    )
    lesson = db.scalar(stmt)
    if lesson is None:
        raise LearningError(404, "Lesson not found")
    return lesson


def admin_courses(db: Session) -> list[Course]:
    stmt = select(Course).options(selectinload(Course.category)).order_by(Course.title)
    return list(db.scalars(stmt).all())


def admin_modules(db: Session, course_id: int) -> list[Module]:
    get_course(db, course_id)
    return list(db.scalars(select(Module).where(Module.course_id == course_id).order_by(Module.position)).all())


def admin_lessons(db: Session, module_id: int) -> list[Lesson]:
    get_module(db, module_id)
    return list(db.scalars(select(Lesson).where(Lesson.module_id == module_id).order_by(Lesson.position)).all())
