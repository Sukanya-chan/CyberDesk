"""Safe challenge services. Flags are hashed and never returned in public APIs."""
import hashlib
from sqlalchemy.orm import Session
from app.models.challenge import Challenge
from app.models.challenge_submission import ChallengeSubmission

def flag_hash(flag: str) -> str:
    return "sha256$" + hashlib.sha256(flag.strip().encode("utf-8")).hexdigest()
class ChallengeError(Exception):
    def __init__(self,status_code,message): self.status_code=status_code; self.message=message

def _get(db,id):
    c=db.get(Challenge,id)
    if not c: raise ChallengeError(404,"challenge not found")
    return c
def _valid(p):
    if p.get("status") not in (None,"draft","published"): raise ChallengeError(400,"status must be draft or published")
    if p.get("difficulty") not in (None,"easy","medium","hard"): raise ChallengeError(400,"difficulty must be easy, medium, or hard")

def admin_challenges(db): return db.query(Challenge).order_by(Challenge.id).all()
def public_challenges(db): return db.query(Challenge).filter(Challenge.status=="published").order_by(Challenge.id).all()
def create(db,p):
    _valid(p); data=dict(p); flag=data.pop("flag"); data["flag_hash"]=flag_hash(flag); c=Challenge(**data); db.add(c); db.commit(); db.refresh(c); return c
def update(db,id,p):
    c=_get(db,id); _valid(p); data=dict(p); flag=data.pop("flag",None)
    if flag is not None: data["flag_hash"]=flag_hash(flag)
    for k,v in data.items(): setattr(c,k,v)
    db.commit(); db.refresh(c); return c
def delete(db,id): c=_get(db,id); db.delete(c); db.commit()
def public(db,id):
    c=_get(db,id)
    if c.status!="published": raise ChallengeError(404,"challenge not found")
    return c
def progress(db,user_id,challenge_id):
    rows=db.query(ChallengeSubmission).filter_by(user_id=user_id,challenge_id=challenge_id,is_correct=True).all()
    return bool(rows), max((r.points_awarded for r in rows), default=0)
def submit(db,user,challenge_id,flag):
    c=public(db,challenge_id); submitted=flag_hash(flag); correct=submitted==c.flag_hash
    points=c.points if correct else 0
    db.add(ChallengeSubmission(challenge_id=c.id,user_id=user.id,submitted_hash=submitted,is_correct=correct,points_awarded=points)); db.commit()
    return correct,points,c.points
