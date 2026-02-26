from sqlalchemy import (
    Column,
    Integer,
    String,
    Text,
    Boolean,
    DateTime,
    ForeignKey,
)
from sqlalchemy.orm import relationship, declarative_base
from sqlalchemy.sql import func

Base = declarative_base()


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, nullable=False)

    def __repr__(self):
        return f"<User id={self.id} username={self.username}>"


class BaseModelMixin:
    is_published = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)

class Category(Base, BaseModelMixin):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(256), nullable=False)
    description = Column(Text, nullable=True)
    slug = Column(String(256), unique=True, nullable=False)

    def __repr__(self):
        return f"<Category id={self.id} title={self.title}>"


class Location(Base, BaseModelMixin):
    __tablename__ = "locations"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(256), nullable=False)

    def __repr__(self):
        return f"<Location id={self.id} name={self.name}>"


class Post(Base, BaseModelMixin):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(256), nullable=False)
    text = Column(Text, nullable=False)
    pub_date = Column(DateTime, nullable=False)

    author_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    author = relationship("User", backref="posts")

    location_id = Column(Integer, ForeignKey("locations.id"), nullable=True)
    location = relationship("Location", backref="posts")

    category_id = Column(Integer, ForeignKey("categories.id"), nullable=True)
    category = relationship("Category", backref="posts")

    image = Column(String, nullable=True)

    def __repr__(self):
        return f"<Post id={self.id} title={self.title}>"


class Comment(Base):
    __tablename__ = "comments"

    id = Column(Integer, primary_key=True, index=True)

    post_id = Column(Integer, ForeignKey("posts.id"), nullable=False)
    post = relationship("Post", backref="comments")

    author_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    text = Column(Text, nullable=False)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)

    def __repr__(self):
        return f"<Comment id={self.id} post_id={self.post_id}>"
