from pydantic import BaseModel, Field
from typing import Annotated, Optional
from datetime import datetime


class CategoryBase(BaseModel):
    title: Annotated[str, Field(max_length=256)]

    description: Annotated[
        str | None,
        Field(max_length=500)
    ] = None

    slug: Annotated[str, Field(pattern=r"^[a-zA-Z0-9_-]+$")]

    is_published: Annotated[
        bool,
        Field(description="Опубликовано")
    ] = True


class CategoryCreate(CategoryBase):
    pass


class CategoryRead(CategoryBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True