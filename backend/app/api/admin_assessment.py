"""Admin assessment management API."""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.api.deps import require_role
from app.db.session import get_db
from app.schemas.assessment import QuizCreate,QuizUpdate,QuizAdminDetail,QuizSummary,QuestionCreate,QuestionUpdate,QuestionAdmin,OptionAdmin
from app.services import assessment as svc
router=APIRouter(prefix='/admin/assessments',tags=['admin-assessments'],dependencies=[Depends(require_role('admin'))])
def err(e): raise HTTPException(status_code=e.status_code,detail=e.message)
def detail(q):
    return QuizAdminDetail(id=q.id,course_id=q.course_id,title=q.title,description=q.description,status=q.status,questions=[QuestionAdmin(id=x.id,question_text=x.question_text,position=x.position,options=[OptionAdmin(id=o.id,option_text=o.option_text,position=o.position,is_correct=o.is_correct) for o in x.options]) for x in q.questions])
@router.get('/quizzes',response_model=list[QuizSummary])
def quizzes(db:Session=Depends(get_db)): return svc.admin_quizzes(db)
@router.post('/quizzes',response_model=QuizSummary,status_code=201)
def create_quiz(p:QuizCreate,db:Session=Depends(get_db)):
    try:return svc.create_quiz(db,p.model_dump())
    except svc.AssessmentError as e:err(e)
@router.patch('/quizzes/{quiz_id}',response_model=QuizSummary)
def update_quiz(quiz_id:int,p:QuizUpdate,db:Session=Depends(get_db)):
    try:return svc.update_quiz(db,quiz_id,p.model_dump(exclude_unset=True))
    except svc.AssessmentError as e:err(e)
@router.delete('/quizzes/{quiz_id}',status_code=204)
def delete_quiz(quiz_id:int,db:Session=Depends(get_db)):
    try:svc.delete_quiz(db,quiz_id)
    except svc.AssessmentError as e:err(e)
@router.get('/quizzes/{quiz_id}',response_model=QuizAdminDetail)
def get_quiz(quiz_id:int,db:Session=Depends(get_db)):
    try:return detail(svc._quiz(db,quiz_id))
    except svc.AssessmentError as e:err(e)
@router.post('/quizzes/{quiz_id}/questions',response_model=QuestionAdmin,status_code=201)
def create_question(quiz_id:int,p:QuestionCreate,db:Session=Depends(get_db)):
    try:
        q=svc.create_question(db,quiz_id,p); return QuestionAdmin(id=q.id,question_text=q.question_text,position=q.position,options=[OptionAdmin(id=o.id,option_text=o.option_text,position=o.position,is_correct=o.is_correct) for o in q.options])
    except svc.AssessmentError as e:err(e)
@router.patch('/questions/{question_id}',response_model=QuestionAdmin)
def update_question(question_id:int,p:QuestionUpdate,db:Session=Depends(get_db)):
    try:
        q=svc.update_question(db,question_id,p); return QuestionAdmin(id=q.id,question_text=q.question_text,position=q.position,options=[OptionAdmin(id=o.id,option_text=o.option_text,position=o.position,is_correct=o.is_correct) for o in q.options])
    except svc.AssessmentError as e:err(e)
@router.delete('/questions/{question_id}',status_code=204)
def delete_question(question_id:int,db:Session=Depends(get_db)):
    try:svc.delete_question(db,question_id)
    except svc.AssessmentError as e:err(e)
