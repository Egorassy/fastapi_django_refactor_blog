from sqlalchemy.orm import Session

from ..infrastructure.repositories.comments import CommentRepository
from ..infrastructure.module.exceptions import NotFoundError as RepoNotFoundError

from ..core.exceptions.http import NotFoundError, ForbiddenError


class CommentUseCase:

    def __init__(self):
        self.repo = CommentRepository()

    def get_all(self, db: Session):
        return self.repo.get_all(db)

    def get_one(self, db: Session, item_id: int):
        try:
            return self.repo.get_by_id(db, item_id)
        except RepoNotFoundError:
            raise NotFoundError(f"Comment {item_id} not found", code="comment_not_found")

    def create(self, db: Session, data: dict):
        return self.repo.create(db, data)

    def update(self, db: Session, item_id: int, data: dict, user_id: int):
        try:
            comment = self.repo.get_by_id(db, item_id)
        except RepoNotFoundError:
            raise NotFoundError(f"Comment {item_id} not found", code="comment_not_found")

        if comment.author_id != user_id:
            raise ForbiddenError("You are not the owner of this comment")

        return self.repo.update(db, item_id, data)

    def delete(self, db: Session, item_id: int, user_id: int):
        try:
            comment = self.repo.get_by_id(db, item_id)
        except RepoNotFoundError:
            raise NotFoundError(f"Comment {item_id} not found", code="comment_not_found")

        if comment.author_id != user_id:
            raise ForbiddenError("You are not the owner of this comment")

        self.repo.delete(db, item_id)