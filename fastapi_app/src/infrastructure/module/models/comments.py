from datetime import datetime
from sqlalchemy import DateTime, ForeignKey, Integer, Text, func
from sqlalchemy.orm import Mapped, mapped_column

from ..base import Base


class Comment(Base):
    __tablename__ = "blog_comment"

    id: Mapped[int] = mapped_column(primary_key=True)

    post_id: Mapped[int] = mapped_column(
        ForeignKey(
            "blog_post.id",
            ondelete="CASCADE"
        )
    )

    author_id: Mapped[int] = mapped_column(
        ForeignKey(
            "users.id",
            ondelete="CASCADE"
        )
    )

    text: Mapped[str]
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )
