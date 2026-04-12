from pydantic import BaseModel, Field, field_validator
from typing import Annotated
from datetime import datetime


class PostBase(BaseModel):
    title: Annotated[str, Field(max_length=256, min_length=1)]

    text: Annotated[str, Field(min_length=1)]

    pub_date: datetime

    author_id: Annotated[int, Field(ge=1)]

    location_id: Annotated[int | None, Field(ge=1)] = None

    category_id: Annotated[int | None, Field(ge=1)] = None

    image: str | None = None

    is_published: Annotated[
        bool,
        Field(description="Опубликовано")
    ] = True

    @field_validator("text")
    def text_not_empty(cls, v):
        if not v.strip():
            raise ValueError("Text cannot be empty")
        return v


class PostCreate(PostBase):
    pass


class PostRead(PostBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True