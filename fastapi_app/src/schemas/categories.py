from pydantic import BaseModel, Field, field_validator
from typing import Annotated
from datetime import datetime


class CategoryBase(BaseModel):
    title: Annotated[str, Field(max_length=256, min_length=1)]

    description: Annotated[
        str | None,
        Field(max_length=500)
    ] = None

    slug: Annotated[
        str,
        Field(pattern=r"^[a-z0-9_-]+$")
    ]

    is_published: Annotated[
        bool,
        Field(description="Опубликовано")
    ] = True

    @field_validator("title")
    def title_not_empty(cls, v):
        if not v.strip():
            raise ValueError("Title cannot be empty")
        return v

    @field_validator("slug")
    def slug_lowercase(cls, v):
        if v != v.lower():
            raise ValueError("Slug must be lowercase")
        return v


class CategoryCreate(CategoryBase):
    pass


class CategoryRead(CategoryBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True