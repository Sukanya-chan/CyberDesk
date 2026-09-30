"""API schemas for Phase 4 assessments."""
from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field, field_validator

class OptionCreate(BaseModel):
    option_text: str = Field(min_length=1, max_length=1000)
    position: int = Field(default=0, ge=0)
    is_correct: bool = False
class OptionUpdate(BaseModel):
    option_text: str | None = Field(default=None, min_length=1, max_length=1000)
    position: int | None = Field(default=None, ge=0)
    is_correct: bool | None = None
class OptionPublic(BaseModel):
    id: int; option_text: str; position: int
    model_config = ConfigDict(from_attributes=True)
class QuestionCreate(BaseModel):
    question_text: str = Field(min_length=1, max_length=5000)
    position: int = Field(default=0, ge=0)
    options: list[OptionCreate] = Field(min_length=2, max_length=6)
    @field_validator("options")
    @classmethod
    def one_correct(cls, value):
        if sum(o.is_correct for o in value) != 1: raise ValueError("exactly one option must be correct")
        return value
class QuestionUpdate(BaseModel):
    question_text: str | None = Field(default=None, min_length=1, max_length=5000)
    position: int | None = Field(default=None, ge=0)
    options: list[OptionCreate] | None = Field(default=None, min_length=2, max_length=6)
    @field_validator("options")
    @classmethod
    def one_correct(cls, value):
        if value is not None and sum(o.is_correct for o in value) != 1: raise ValueError("exactly one option must be correct")
        return value
class QuestionPublic(BaseModel):
    id: int; question_text: str; position: int; options: list[OptionPublic]
class QuizCreate(BaseModel):
    course_id: int = Field(gt=0); title: str = Field(min_length=2, max_length=255); description: str | None = Field(default=None, max_length=5000); status: str = "draft"
class QuizUpdate(BaseModel):
    course_id: int | None = Field(default=None, gt=0); title: str | None = Field(default=None, min_length=2, max_length=255); description: str | None = Field(default=None, max_length=5000); status: str | None = None
class QuizSummary(BaseModel):
    id: int; course_id: int; title: str; description: str | None; status: str
class QuizDetail(QuizSummary):
    questions: list[QuestionPublic]
class QuizAdminDetail(QuizSummary):
    questions: list["QuestionAdmin"]
class QuestionAdmin(QuestionPublic):
    options: list["OptionAdmin"]
class OptionAdmin(OptionPublic):
    is_correct: bool
class AnswerInput(BaseModel):
    question_id: int = Field(gt=0); option_id: int | None = Field(default=None, gt=0)
class QuizAttemptCreate(BaseModel):
    answers: list[AnswerInput] = []
class QuizAnswerResult(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    question_id: int; selected_option_id: int | None; is_correct: bool
class QuizAttemptResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int; quiz_id: int; score: int; total_questions: int; submitted_at: datetime; answers: list[QuizAnswerResult]
class AttemptSummary(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int; quiz_id: int; score: int; total_questions: int; submitted_at: datetime
