from app.models.lesson_progress import LessonProgress
from app.services.progress import ProgressError

def test_lesson_progress_model_has_unique_pair():
    constraints = {c.name for c in LessonProgress.__table__.constraints}
    assert "uq_lesson_progress_user_lesson" in constraints

def test_progress_error_contract():
    err = ProgressError(404, "missing")
    assert err.status_code == 404
    assert err.message == "missing"
