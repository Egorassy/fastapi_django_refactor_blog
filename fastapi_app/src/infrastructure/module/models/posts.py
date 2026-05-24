from datetime import datetime
from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column

from ..base import Base


class Post(Base):
    __tablename__ = "blog_post"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String(256), nullable=False)
    text: Mapped[str] = mapped_column(Text, nullable=False)
    pub_date: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    author_id: Mapped[int] = mapped_column(Integer, nullable=False)
    location_id: Mapped[int | None] = mapped_column(
        Integer,
        ForeignKey(
            "blog_location.id",
            ondelete="SET NULL",
        ),
        nullable=True,
    )

    category_id: Mapped[int | None] = mapped_column(
        Integer,
        ForeignKey(
            "blog_category.id",
            ondelete="SET NULL",
        ),
        nullable=True,
    )
    image: Mapped[str | None] = mapped_column(String, nullable=True)
    is_published: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )