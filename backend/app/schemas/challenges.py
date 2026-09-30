"""API schemas for Phase 5 safe flag-based challenges."""
from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field
class ChallengeCreate(BaseModel):
    slug: str = Field(min_length=2, max_length=255); title: str = Field(min_length=2, max_length=255); description: str = Field(min_length=1, max_length=10000); instructions: str | None = Field(default=None, max_length=10000); hint: str | None = Field(default=None, max_length=5000); difficulty: str = "easy"; category: str = Field(min_length=2, max_length=64); points: int = Field(default=100, gt=0); flag: str = Field(min_length=1, max_length=500); status: str = "draft"
class ChallengeUpdate(BaseModel):
    slug: str | None = Field(default=None, min_length=2, max_length=255); title: str | None = Field(default=None, min_length=2, max_length=255); description: str | None = Field(default=None, min_length=1, max_length=10000); instructions: str | None = Field(default=None, max_length=10000); hint: str | None = Field(default=None, max_length=5000); difficulty: str | None = None; category: str | None = Field(default=None, min_length=2, max_length=64); points: int | None = Field(default=None, gt=0); flag: str | None = Field(default=None, min_length=1, max_length=500); status: str | None = None
class ChallengePublic(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int; slug: str; title: str; description: str; instructions: str | None; hint: str | None; difficulty: str; category: str; points: int; status: str
class ChallengeAdmin(ChallengePublic):
    flag_hash: str
class FlagSubmission(BaseModel):
    flag: str = Field(min_length=1, max_length=500)
class ChallengeSubmissionResponse(BaseModel):
    correct: bool; points_awarded: int; total_points: int; message: str
class ChallengeProgress(BaseModel):
    solved: bool
    points_earned: int
