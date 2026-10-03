"""Authenticated student progress APIs."""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.api.deps import get_current_user
from app.db.session import get_db
from app.models.user import AppUser
from app.schemas.progress import DashboardResponse, LessonProgressResponse
from app.services import progress as svc

router = APIRouter(tags=["progress"])

def _error(exc: svc.ProgressError):
    raise HTTPException(status_code=exc.status_code, detail=exc.message)

@router.get("/progress/dashboard", response_model=DashboardResponse)
def read_dashboard(current: AppUser = Depends(get_current_user), db: Session = Depends(get_db)):
    return svc.dashboard(db, current)

@router.post("/lessons/{lesson_id}/complete", response_model=LessonProgressResponse, status_code=status.HTTP_200_OK)
def mark_lesson_complete(lesson_id: int, current: AppUser = Depends(get_current_user), db: Session = Depends(get_db)):
    try:
        row = svc.complete_lesson(db, current, lesson_id)
    except svc.ProgressError as exc:
        _error(exc)
    return LessonProgressResponse(lesson_id=row.lesson_id, completed=True, completed_at=row.completed_at)

@router.get("/lessons/{lesson_id}/progress", response_model=LessonProgressResponse)
def read_lesson_progress(lesson_id: int, current: AppUser = Depends(get_current_user), db: Session = Depends(get_db)):
    row = svc.lesson_status(db, current, lesson_id)
    return LessonProgressResponse(
        lesson_id=lesson_id,
        completed=row is not None,
        completed_at=row.completed_at if row else None,
    )
