"""Phase 3A tests: Category/Course/Module/Lesson models and constraints.

These exercise the SQLAlchemy layer directly (no HTTP client, no auth) —
relationships, FK enforcement, and the composite
(module_id, course_id) -> (modules.id, modules.course_id) constraint that
makes "a lesson cannot reference a module belonging to another course" a
database-level guarantee rather than only an application-level check.
"""
import pytest
from sqlalchemy import text
from sqlalchemy.exc import IntegrityError

from app.db.session import Base, SessionLocal, engine
from app.models.category import Category
from app.models.course import Course
from app.models.lesson import Lesson
from app.models.module import Module


@pytest.fixture(autouse=True)
def _clean_tables():
    """Reset tables between tests so they don't interfere with each other."""
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    yield


@pytest.fixture
def db():
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()


def _make_category(db, name="Web Security") -> Category:
    category = Category(name=name, description="desc")
    db.add(category)
    db.commit()
    db.refresh(category)
    return category


def _make_course(db, category: Category, slug="intro-appsec", status="draft") -> Course:
    course = Course(
        category_id=category.id,
        slug=slug,
        title="Intro to AppSec",
        description="desc",
        status=status,
    )
    db.add(course)
    db.commit()
    db.refresh(course)
    return course


def _make_module(db, course: Course, position=0) -> Module:
    module = Module(course_id=course.id, title="Module 1", position=position)
    db.add(module)
    db.commit()
    db.refresh(module)
    return module


def _make_lesson(db, module: Module, course_id: int, slug="lesson-1", status="draft") -> Lesson:
    lesson = Lesson(
        module_id=module.id,
        course_id=course_id,
        slug=slug,
        title="Lesson 1",
        content="# Hello",
        position=0,
        status=status,
    )
    db.add(lesson)
    db.commit()
    db.refresh(lesson)
    return lesson


# --- Foreign key enforcement is actually turned on -------------------------


def test_sqlite_foreign_keys_pragma_is_enabled():
    with engine.connect() as conn:
        result = conn.execute(text("PRAGMA foreign_keys")).scalar()
    assert result == 1


# --- Relationships -----------------------------------------------------


def test_category_course_module_lesson_relationship_chain(db):
    category = _make_category(db)
    course = _make_course(db, category)
    module = _make_module(db, course)
    lesson = _make_lesson(db, module, course.id)

    db.refresh(category)
    db.refresh(course)
    db.refresh(module)

    assert category.courses == [course]
    assert course.category.id == category.id
    assert course.modules == [module]
    assert module.course.id == course.id
    assert module.lessons == [lesson]
    assert lesson.module.id == module.id


# --- Composite course/module consistency --------------------------------


def test_lesson_cannot_reference_module_from_another_course(db):
    category = _make_category(db)
    course_a = _make_course(db, category, slug="course-a")
    course_b = _make_course(db, category, slug="course-b")
    module_a = _make_module(db, course_a)

    # module_a belongs to course_a, but this lesson claims course_b.
    bad_lesson = Lesson(
        module_id=module_a.id,
        course_id=course_b.id,
        slug="mismatched",
        title="Mismatched lesson",
        content="x",
        position=0,
        status="draft",
    )
    db.add(bad_lesson)
    with pytest.raises(IntegrityError):
        db.commit()
    db.rollback()


def test_lesson_course_id_must_match_an_existing_module(db):
    category = _make_category(db)
    course = _make_course(db, category)

    orphan_lesson = Lesson(
        module_id=999999,
        course_id=course.id,
        slug="orphan",
        title="Orphan",
        content="x",
        position=0,
        status="draft",
    )
    db.add(orphan_lesson)
    with pytest.raises(IntegrityError):
        db.commit()
    db.rollback()


# --- Uniqueness ----------------------------------------------------------


def test_course_slug_is_globally_unique(db):
    category = _make_category(db)
    _make_course(db, category, slug="dup-slug")

    db.add(Course(category_id=category.id, slug="dup-slug", title="Other", status="draft"))
    with pytest.raises(IntegrityError):
        db.commit()
    db.rollback()


def test_lesson_slug_unique_within_course_but_not_across_courses(db):
    category = _make_category(db)
    course_a = _make_course(db, category, slug="course-a")
    course_b = _make_course(db, category, slug="course-b")
    module_a = _make_module(db, course_a)
    module_b = _make_module(db, course_b)

    _make_lesson(db, module_a, course_a.id, slug="same-slug")

    # Same slug, different course: allowed.
    other_course_lesson = _make_lesson(db, module_b, course_b.id, slug="same-slug")
    assert other_course_lesson.id is not None

    # Same slug, same course: rejected.
    db.add(
        Lesson(
            module_id=module_a.id,
            course_id=course_a.id,
            slug="same-slug",
            title="Dup",
            content="x",
            position=1,
            status="draft",
        )
    )
    with pytest.raises(IntegrityError):
        db.commit()
    db.rollback()


# --- Status check constraints --------------------------------------------


def test_course_status_must_be_draft_or_published(db):
    category = _make_category(db)
    db.add(Course(category_id=category.id, slug="bad-status", title="X", status="archived"))
    with pytest.raises(IntegrityError):
        db.commit()
    db.rollback()


def test_lesson_status_must_be_draft_or_published(db):
    category = _make_category(db)
    course = _make_course(db, category)
    module = _make_module(db, course)
    db.add(
        Lesson(
            module_id=module.id,
            course_id=course.id,
            slug="bad-status",
            title="X",
            content="x",
            position=0,
            status="archived",
        )
    )
    with pytest.raises(IntegrityError):
        db.commit()
    db.rollback()


# --- Delete behavior -------------------------------------------------------


def test_category_delete_is_restricted_when_it_has_courses(db):
    category = _make_category(db)
    _make_course(db, category)

    db.delete(category)
    with pytest.raises(IntegrityError):
        db.commit()
    db.rollback()


def test_deleting_course_cascades_to_modules_and_lessons(db):
    category = _make_category(db)
    course = _make_course(db, category)
    module = _make_module(db, course)
    lesson = _make_lesson(db, module, course.id)

    db.delete(course)
    db.commit()

    assert db.get(Module, module.id) is None
    assert db.get(Lesson, lesson.id) is None


def test_deleting_module_cascades_to_its_lessons_only(db):
    category = _make_category(db)
    course = _make_course(db, category)
    module = _make_module(db, course)
    lesson = _make_lesson(db, module, course.id)

    db.delete(module)
    db.commit()

    assert db.get(Lesson, lesson.id) is None
    assert db.get(Course, course.id) is not None
