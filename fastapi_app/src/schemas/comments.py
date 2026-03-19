from pydantic import BaseModel
from datetime import datetime


class CommentBase(BaseModel):
    post_id: int
    author_id: int
    text: str


class CommentCreate(CommentBase):
    pass


class CommentRead(CommentBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True