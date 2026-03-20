from sqlalchemy import Column, Integer, Text, DateTime, ForeignKey
from sqlalchemy.orm import declarative_base

from .base import Base


class Comment(Base):
    __tablename__ = "blog_comment"

    id = Column(Integer, primary_key=True, index=True)
    post_id = Column(Integer, ForeignKey("blog_post.id"))
    author_id = Column(Integer)
    text = Column(Text)
    created_at = Column(DateTime)