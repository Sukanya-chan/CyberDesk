from pydantic import BaseModel, Field

class AIAssistRequest(BaseModel):
    prompt: str = Field(min_length=1, max_length=2000)
    context: str | None = Field(default=None, max_length=4000)

class AIAssistResponse(BaseModel):
    answer: str
    model: str
