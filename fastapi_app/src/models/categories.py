from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime
from sqlalchemy.orm import declarative_base

from .base import Base


class Category(Base):
    __tablename__ = "blog_category"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(256))
    description = Column(Text)
    slug = Column(String, unique=True)
    is_published = Column(Boolean, default=True)
    created_at = Column(DateTime)