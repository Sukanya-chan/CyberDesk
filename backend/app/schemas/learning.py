"""Pydantic schemas for the Phase 3 learning-content system."""
from pydantic import BaseModel, ConfigDict, Field, field_validator

VALID_STATUSES = {"draft", "published"}


def _clean(value: str) -> str:
    value = value.strip()
    if not value:
        raise ValueError("value must not be empty")
    return value


class CategoryCreate(BaseModel):
    name: str = Field(min_length=2, max_length=255)
    description: str | None = Field(default=None, max_length=2000)

    @field_validator("name")
    @classmethod
    def clean_name(cls, value: str) -> str:
        return _clean(value)


class CategoryUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=2, max_length=255)
    description: str | None = Field(default=None, max_length=2000)

    @field_validator("name")
    @classmethod
    def clean_name(cls, value: str | None) -> str | None:
        return None if value is None else _clean(value)


class CategoryResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    description: str | None = None


class CourseCreate(BaseModel):
    category_id: int = Field(gt=0)
    slug: str = Field(min_length=2, max_length=255)
    title: str = Field(min_length=2, max_length=255)
    description: str | None = Field(default=None, max_length=5000)
    status: str = "draft"

    @field_validator("slug", "title")
    @classmethod
    def clean_text(cls, value: str) -> str:
        return _clean(value)

    @field_validator("status")
    @classmethod
    def valid_status(cls, value: str) -> str:
        if value not in VALID_STATUSES:
            raise ValueError("status must be draft or published")
        return value


class CourseUpdate(BaseModel):
    category_id: int | None = Field(default=None, gt=0)
    slug: str | None = Field(default=None, min_length=2, max_length=255)
    title: str | None = Field(default=None, min_length=2, max_length=255)
    description: str | None = Field(default=None, max_length=5000)
    status: str | None = None

    @field_validator("slug", "title")
    @classmethod
    def clean_text(cls, value: str | None) -> str | None:
        return None if value is None else _clean(value)

    @field_validator("status")
    @classmethod
    def valid_status(cls, value: str | None) -> str | None:
        if value is not None and value not in VALID_STATUSES:
            raise ValueError("status must be draft or published")
        return value


class CourseSummary(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    category_id: int
    category_name: str
    slug: str
    title: str
    description: str | None = None


class LessonSummary(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    slug: str
    title: str
    position: int


class ModuleResponse(BaseModel):
    id: int
    course_id: int
    title: str
    position: int
    lessons: list[LessonSummary] = []


class CourseDetail(BaseModel):
    id: int
    category_id: int
    category_name: str
    slug: str
    title: str
    description: str | None = None
    modules: list[ModuleResponse]


class LessonCreate(BaseModel):
    module_id: int = Field(gt=0)
    slug: str = Field(min_length=2, max_length=255)
    title: str = Field(min_length=2, max_length=255)
    content: str = Field(min_length=1)
    position: int | None = Field(default=None, ge=0)
    status: str = "draft"

    @field_validator("slug", "title")
    @classmethod
    def clean_text(cls, value: str) -> str:
        return _clean(value)

    @field_validator("status")
    @classmethod
    def valid_status(cls, value: str) -> str:
        if value not in VALID_STATUSES:
            raise ValueError("status must be draft or published")
        return value


class LessonUpdate(BaseModel):
    module_id: int | None = Field(default=None, gt=0)
    slug: str | None = Field(default=None, min_length=2, max_length=255)
    title: str | None = Field(default=None, min_length=2, max_length=255)
    content: str | None = None
    position: int | None = Field(default=None, ge=0)
    status: str | None = None

    @field_validator("slug", "title")
    @classmethod
    def clean_text(cls, value: str | None) -> str | None:
        return None if value is None else _clean(value)

    @field_validator("status")
    @classmethod
    def valid_status(cls, value: str | None) -> str | None:
        if value is not None and value not in VALID_STATUSES:
            raise ValueError("status must be draft or published")
        return value


class LessonResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    course_id: int
    module_id: int
    slug: str
    title: str
    content: str
    position: int
    status: str


class ModuleCreate(BaseModel):
    course_id: int = Field(gt=0)
    title: str = Field(min_length=2, max_length=255)
    position: int | None = Field(default=None, ge=0)

    @field_validator("title")
    @classmethod
    def clean_title(cls, value: str) -> str:
        return _clean(value)


class ModuleUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=2, max_length=255)
    position: int | None = Field(default=None, ge=0)

    @field_validator("title")
    @classmethod
    def clean_title(cls, value: str | None) -> str | None:
        return None if value is None else _clean(value)


class AdminModuleResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    course_id: int
    title: str
    position: int


class AdminLessonResponse(LessonResponse):
    pass


class ReorderRequest(BaseModel):
    ordered_ids: list[int] = Field(min_length=1)

    @field_validator("ordered_ids")
    @classmethod
    def unique_ids(cls, value: list[int]) -> list[int]:
        if len(value) != len(set(value)):
            raise ValueError("ordered_ids must not contain duplicates")
        return value
