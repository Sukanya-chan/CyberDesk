"""Optional AI learning-assistant API."""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.api.deps import get_current_user
from app.db.session import get_db
from app.models.user import AppUser
from app.schemas.ai import AIAssistRequest, AIAssistResponse
from app.services import ai

router = APIRouter(tags=["ai"])

@router.post("/ai/assist", response_model=AIAssistResponse)
async def ai_assist(payload: AIAssistRequest, current: AppUser = Depends(get_current_user), db: Session = Depends(get_db)):
    del current, db
    try:
        answer, model = await ai.assist(payload.prompt, payload.context)
    except ai.AIError as exc:
        raise HTTPException(status_code=exc.status_code, detail=exc.message)
    return AIAssistResponse(answer=answer, model=model)
