from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.orm import declarative_base

from .base import Base


class Location(Base):
    __tablename__ = "blog_location"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(256))
    is_published = Column(Boolean, default=True)
    created_at = Column(DateTime)