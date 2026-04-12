from pydantic import BaseModel, Field, field_validator
from typing import Annotated
from datetime import datetime


class CommentBase(BaseModel):
    post_id: Annotated[int, Field(ge=1)]
    author_id: Annotated[int, Field(ge=1)]

    text: Annotated[str, Field(min_length=1)]

    @field_validator("text")
    def text_not_empty(cls, v):
        if not v.strip():
            raise ValueError("Comment cannot be empty")
        return v


class CommentCreate(CommentBase):
    pass


class CommentRead(CommentBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True