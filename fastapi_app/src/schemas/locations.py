from pydantic import BaseModel, Field
from typing import Annotated
from datetime import datetime


class LocationBase(BaseModel):
    name: Annotated[str, Field(max_length=256)]
    is_published: bool = True


class LocationCreate(LocationBase):
    pass


class LocationRead(LocationBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True