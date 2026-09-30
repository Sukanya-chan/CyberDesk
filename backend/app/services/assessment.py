"""Assessment services: CRUD, safe public views, and deterministic scoring."""
from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.models.course import Course
from app.models.quiz import Quiz
from app.models.question import Question
from app.models.question_option import QuestionOption
from app.models.quiz_attempt import QuizAttempt, QuizAnswer

class AssessmentError(Exception):
    def __init__(self, status_code: int, message: str): self.status_code=status_code; self.message=message

def _quiz(db, quiz_id):
    q=db.get(Quiz, quiz_id)
    if not q: raise AssessmentError(404,"quiz not found")
    return q

def _validate_status(status):
    if status not in ("draft","published"): raise AssessmentError(400,"status must be draft or published")

def _validate_course(db, course_id):
    if not db.get(Course, course_id): raise AssessmentError(404,"course not found")

def _validate_questions(payload):
    if not payload.options or sum(o.is_correct for o in payload.options) != 1: raise AssessmentError(400,"exactly one option must be correct")

def admin_quizzes(db): return db.query(Quiz).order_by(Quiz.id).all()
def public_quizzes(db): return db.query(Quiz).join(Course).filter(Quiz.status=="published", Course.status=="published").order_by(Quiz.id).all()

def create_quiz(db,p):
    _validate_course(db,p["course_id"]); _validate_status(p.get("status","draft")); q=Quiz(**p); db.add(q); db.commit(); db.refresh(q); return q

def update_quiz(db, quiz_id, p):
    q=_quiz(db,quiz_id)
    if "course_id" in p: _validate_course(db,p["course_id"])
    if "status" in p: _validate_status(p["status"])
    for k,v in p.items(): setattr(q,k,v)
    db.commit(); db.refresh(q); return q

def delete_quiz(db,quiz_id):
    q=_quiz(db,quiz_id); db.delete(q); db.commit()

def get_public_quiz(db, quiz_id):
    q=_quiz(db,quiz_id)
    if q.status!="published" or q.course.status!="published": raise AssessmentError(404,"quiz not found")
    return q

def create_question(db, quiz_id, p):
    qz=_quiz(db,quiz_id); _validate_questions(p)
    q=Question(quiz_id=qz.id,question_text=p.question_text,position=p.position)
    db.add(q); db.flush()
    for o in p.options: db.add(QuestionOption(question_id=q.id,option_text=o.option_text,position=o.position,is_correct=o.is_correct))
    db.commit(); db.refresh(q); return q

def update_question(db, question_id, p):
    q=db.get(Question,question_id)
    if not q: raise AssessmentError(404,"question not found")
    data=p.model_dump(exclude_unset=True) if hasattr(p,"model_dump") else p
    options=data.pop("options",None)
    if options is not None and sum(o["is_correct"] for o in options)!=1: raise AssessmentError(400,"exactly one option must be correct")
    for k,v in data.items(): setattr(q,k,v)
    if options is not None:
        q.options.clear(); db.flush()
        for o in options: db.add(QuestionOption(question_id=q.id,**o))
    db.commit(); db.refresh(q); return q

def delete_question(db, question_id):
    q=db.get(Question,question_id)
    if not q: raise AssessmentError(404,"question not found")
    db.delete(q); db.commit()

def submit_attempt(db,user,quiz_id,answers):
    quiz=get_public_quiz(db,quiz_id)
    questions={q.id:q for q in quiz.questions}
    if not questions: raise AssessmentError(400,"quiz has no questions")
    provided={a.question_id:a.option_id for a in answers}
    unknown=set(provided)-set(questions)
    if unknown: raise AssessmentError(400,"answer contains a question outside this quiz")
    attempt=QuizAttempt(quiz_id=quiz.id,user_id=user.id,total_questions=len(questions),score=0)
    db.add(attempt); db.flush(); score=0
    for question in questions.values():
        selected=provided.get(question.id)
        valid_option=next((o for o in question.options if o.id==selected),None) if selected else None
        correct=bool(valid_option and valid_option.is_correct)
        if correct: score += 1
        db.add(QuizAnswer(attempt_id=attempt.id,question_id=question.id,selected_option_id=selected,is_correct=correct))
    attempt.score=score; db.commit(); db.refresh(attempt); return attempt

def user_attempts(db,user_id,quiz_id=None):
    q=db.query(QuizAttempt).filter(QuizAttempt.user_id==user_id)
    if quiz_id: q=q.filter(QuizAttempt.quiz_id==quiz_id)
    return q.order_by(QuizAttempt.id.desc()).all()
