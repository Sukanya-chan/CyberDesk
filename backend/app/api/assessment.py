"""Public and authenticated assessment APIs."""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.api.deps import get_current_user
from app.db.session import get_db
from app.models.user import AppUser
from app.schemas.assessment import QuizSummary, QuizDetail, QuizAttemptCreate, QuizAttemptResponse, AttemptSummary
from app.services import assessment as svc
router=APIRouter(tags=["assessments"])
def err(e): raise HTTPException(status_code=e.status_code, detail=e.message)
def _public(q):
    return QuizDetail(id=q.id,course_id=q.course_id,title=q.title,description=q.description,status=q.status,questions=[{"id":x.id,"question_text":x.question_text,"position":x.position,"options":[{"id":o.id,"option_text":o.option_text,"position":o.position} for o in x.options]} for x in q.questions])
@router.get('/quizzes',response_model=list[QuizSummary])
def list_quizzes(db:Session=Depends(get_db)):
    return svc.public_quizzes(db)
@router.get('/quizzes/{quiz_id}',response_model=QuizDetail)
def get_quiz(quiz_id:int,db:Session=Depends(get_db)):
    try:return _public(svc.get_public_quiz(db,quiz_id))
    except svc.AssessmentError as e:err(e)
@router.post('/quizzes/{quiz_id}/attempts',response_model=QuizAttemptResponse,status_code=status.HTTP_201_CREATED)
def submit_quiz(quiz_id:int,payload:QuizAttemptCreate,current:AppUser=Depends(get_current_user),db:Session=Depends(get_db)):
    try:
        a=svc.submit_attempt(db,current,quiz_id,payload.answers)
        return a
    except svc.AssessmentError as e:err(e)
@router.get('/quizzes/{quiz_id}/attempts',response_model=list[AttemptSummary])
def attempts(quiz_id:int,current:AppUser=Depends(get_current_user),db:Session=Depends(get_db)):
    return svc.user_attempts(db,current.id,quiz_id)
@router.get('/attempts/{attempt_id}',response_model=QuizAttemptResponse)
def attempt(attempt_id:int,current:AppUser=Depends(get_current_user),db:Session=Depends(get_db)):
    a=db.get(__import__('app.models.quiz_attempt',fromlist=['QuizAttempt']).QuizAttempt,attempt_id)
    if not a or a.user_id!=current.id: raise HTTPException(404,'attempt not found')
    return a
