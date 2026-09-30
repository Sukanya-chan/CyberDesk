"""Admin challenge CRUD API. Plaintext flags are accepted only on write and never returned."""
from fastapi import APIRouter,Depends,HTTPException
from sqlalchemy.orm import Session
from app.api.deps import require_role
from app.db.session import get_db
from app.schemas.challenges import ChallengeCreate,ChallengeUpdate,ChallengeAdmin
from app.services import challenges as svc
router=APIRouter(prefix='/admin/challenges',tags=['admin-challenges'],dependencies=[Depends(require_role('admin'))])
def err(e): raise HTTPException(status_code=e.status_code,detail=e.message)
def out(c): return c
@router.get('',response_model=list[ChallengeAdmin])
def list_admin(db:Session=Depends(get_db)): return svc.admin_challenges(db)
@router.post('',response_model=ChallengeAdmin,status_code=201)
def create(p:ChallengeCreate,db:Session=Depends(get_db)):
    try:return svc.create(db,p.model_dump())
    except svc.ChallengeError as e:err(e)
@router.patch('/{challenge_id}',response_model=ChallengeAdmin)
def update(challenge_id:int,p:ChallengeUpdate,db:Session=Depends(get_db)):
    try:return svc.update(db,challenge_id,p.model_dump(exclude_unset=True))
    except svc.ChallengeError as e:err(e)
@router.delete('/{challenge_id}',status_code=204)
def delete(challenge_id:int,db:Session=Depends(get_db)):
    try:svc.delete(db,challenge_id)
    except svc.ChallengeError as e:err(e)
