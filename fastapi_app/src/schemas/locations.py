from pydantic import BaseModel, Field, field_validator
from typing import Annotated
from datetime import datetime


class LocationBase(BaseModel):
    name: Annotated[str, Field(max_length=256, min_length=1)]

    is_published: Annotated[
        bool,
        Field(description="Опубликовано")
    ] = True

    @field_validator("name")
    def name_not_empty(cls, v):
        if not v.strip():
            raise ValueError("Name cannot be empty")
        return v


class LocationCreate(LocationBase):
    pass


class LocationRead(LocationBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True