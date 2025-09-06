"""Pydantic response models"""

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class BaseSchema(BaseModel):
    """Base pydantic model"""

    model_config = ConfigDict(from_attributes=True)


class QuestionCreate(BaseSchema):
    """Question create pydantic model"""

    text: str


class QuestionResponse(QuestionCreate):
    """Question response pydantic model"""

    id: int
    created_at: datetime


class AnswerCreate(BaseSchema):
    """Answer create pydantic model"""

    question_id: int
    user_id: UUID
    text: str


class AnswerResponse(AnswerCreate):
    """Answer response pydantic model"""

    id: int
    created_at: datetime
