from pydantic import BaseModel, Field
from typing import Annotated
from datetime import datetime


class CommentBase(BaseModel):
    post_id: Annotated[int, Field(ge=1)]
    author_id: Annotated[int, Field(ge=1)]
    text: str


class CommentCreate(CommentBase):
    pass


class CommentRead(CommentBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True