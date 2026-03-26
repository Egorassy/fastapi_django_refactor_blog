from pydantic import BaseModel, Field
from typing import Annotated, Optional
from datetime import datetime


class PostBase(BaseModel):
    title: Annotated[str, Field(max_length=256)]
    text: str
    pub_date: datetime
    author_id: Annotated[int, Field(ge=1)]
    location_id: Optional[Annotated[int, Field(ge=1)]] = None
    category_id: Optional[Annotated[int, Field(ge=1)]] = None
    image: Optional[str] = None
    is_published: bool = True


class PostCreate(PostBase):
    pass


class PostRead(PostBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True