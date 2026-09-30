"""Public and authenticated safe challenge APIs."""
from fastapi import APIRouter,Depends,HTTPException,status
from sqlalchemy.orm import Session
from app.api.deps import get_current_user
from app.db.session import get_db
from app.models.user import AppUser
from app.schemas.challenges import ChallengePublic,FlagSubmission,ChallengeSubmissionResponse,ChallengeProgress
from app.services import challenges as svc
router=APIRouter(tags=['challenges'])
def err(e): raise HTTPException(status_code=e.status_code,detail=e.message)
@router.get('/challenges',response_model=list[ChallengePublic])
def list_challenges(db:Session=Depends(get_db)): return svc.public_challenges(db)
@router.get('/challenges/{challenge_id}',response_model=ChallengePublic)
def get_challenge(challenge_id:int,db:Session=Depends(get_db)):
    try:return svc.public(db,challenge_id)
    except svc.ChallengeError as e:err(e)
@router.post('/challenges/{challenge_id}/submit',response_model=ChallengeSubmissionResponse)
def submit_challenge(challenge_id:int,p:FlagSubmission,current:AppUser=Depends(get_current_user),db:Session=Depends(get_db)):
    try:
        correct,points,total=svc.submit(db,current,challenge_id,p.flag)
        return {'correct':correct,'points_awarded':points,'total_points':total,'message':'Correct flag.' if correct else 'Incorrect flag.'}
    except svc.ChallengeError as e:err(e)
@router.get('/challenges/{challenge_id}/progress',response_model=ChallengeProgress)
def progress(challenge_id:int,current:AppUser=Depends(get_current_user),db:Session=Depends(get_db)):
    try:svc.public(db,challenge_id)
    except svc.ChallengeError as e:err(e)
    solved,points=svc.progress(db,current.id,challenge_id)
    return {'solved':solved,'points_earned':points}
