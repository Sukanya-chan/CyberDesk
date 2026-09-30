"""Phase 4A + Phase 5A model foundation tests."""
import pytest
from sqlalchemy.exc import IntegrityError

from app.db.session import Base, SessionLocal, engine
from app.models.category import Category
from app.models.challenge import Challenge
from app.models.course import Course
from app.models.question import Question
from app.models.question_option import QuestionOption
from app.models.quiz import Quiz


@pytest.fixture(autouse=True)
def _clean_tables():
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


def _course(db):
    category = Category(name="Security")
    db.add(category)
    db.flush()
    course = Course(
        category_id=category.id,
        slug="security-foundations",
        title="Security Foundations",
        status="published",
    )
    db.add(course)
    db.commit()
    db.refresh(course)
    return course


def test_quiz_question_option_relationship_chain(db):
    course = _course(db)
    quiz = Quiz(course_id=course.id, title="Security Quiz", status="published")
    db.add(quiz)
    db.flush()

    question = Question(
        quiz_id=quiz.id,
        question_text="Which protocol is used for secure web traffic?",
        position=0,
    )
    db.add(question)
    db.flush()

    db.add_all(
        [
            QuestionOption(
                question_id=question.id,
                option_text="HTTPS",
                position=0,
                is_correct=True,
            ),
            QuestionOption(
                question_id=question.id,
                option_text="FTP",
                position=1,
                is_correct=False,
            ),
        ]
    )
    db.commit()
    db.refresh(quiz)
    db.refresh(question)

    assert quiz.course.id == course.id
    assert quiz.questions == [question]
    assert question.quiz.id == quiz.id
    assert [option.option_text for option in question.options] == ["HTTPS", "FTP"]
    assert question.options[0].is_correct is True


def test_quiz_status_is_restricted(db):
    course = _course(db)
    db.add(Quiz(course_id=course.id, title="Bad", status="archived"))
    with pytest.raises(IntegrityError):
        db.commit()
    db.rollback()


def test_question_type_is_mcq_only(db):
    course = _course(db)
    quiz = Quiz(course_id=course.id, title="Quiz")
    db.add(quiz)
    db.flush()
    db.add(Question(quiz_id=quiz.id, question_text="x", type="true_false"))
    with pytest.raises(IntegrityError):
        db.commit()
    db.rollback()


def test_deleting_quiz_cascades_questions_and_options(db):
    course = _course(db)
    quiz = Quiz(course_id=course.id, title="Quiz")
    db.add(quiz)
    db.flush()
    question = Question(quiz_id=quiz.id, question_text="x")
    db.add(question)
    db.flush()
    option = QuestionOption(question_id=question.id, option_text="x")
    db.add(option)
    db.commit()

    question_id, option_id = question.id, option.id
    db.delete(quiz)
    db.commit()

    assert db.get(Question, question_id) is None
    assert db.get(QuestionOption, option_id) is None


def test_challenge_model_stores_hash_not_plaintext(db):
    challenge = Challenge(
        slug="decode-message",
        title="Decode the Message",
        description="Decode the supplied message.",
        instructions="Use the provided encoding reference.",
        hint="Start by identifying the encoding.",
        difficulty="easy",
        category="cryptography",
        points=100,
        flag_hash="sha256$examplehash",
        status="published",
    )
    db.add(challenge)
    db.commit()
    db.refresh(challenge)

    assert challenge.flag_hash == "sha256$examplehash"
    assert not hasattr(challenge, "flag")
    assert challenge.is_published is True


def test_challenge_status_and_difficulty_are_restricted(db):
    db.add(
        Challenge(
            slug="bad-status",
            title="Bad",
            description="x",
            difficulty="nightmare",
            category="linux",
            points=100,
            flag_hash="hash",
            status="archived",
        )
    )
    with pytest.raises(IntegrityError):
        db.commit()
    db.rollback()


def test_challenge_points_must_be_positive(db):
    db.add(
        Challenge(
            slug="zero-points",
            title="Zero",
            description="x",
            difficulty="easy",
            category="linux",
            points=0,
            flag_hash="hash",
            status="draft",
        )
    )
    with pytest.raises(IntegrityError):
        db.commit()
    db.rollback()


def test_challenge_slug_is_unique(db):
    common = dict(
        title="Duplicate",
        description="x",
        difficulty="easy",
        category="linux",
        points=50,
        flag_hash="hash",
        status="draft",
    )
    db.add(Challenge(slug="duplicate", **common))
    db.commit()
    db.add(Challenge(slug="duplicate", **common))
    with pytest.raises(IntegrityError):
        db.commit()
    db.rollback()
