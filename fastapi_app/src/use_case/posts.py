from sqlalchemy.orm import Session

from ..infrastructure.repositories.posts import PostRepository
from ..infrastructure.module.exceptions import NotFoundError as RepoNotFoundError, IntegrityDatabaseError

from ..core.exceptions.http import NotFoundError, ConflictError, ForbiddenError


class PostUseCase:

    def __init__(self):
        self.repo = PostRepository()

    def get_all(self, db: Session):
        return self.repo.get_all(db)

    def get_one(self, db: Session, item_id: int):
        try:
            return self.repo.get_by_id(db, item_id)
        except RepoNotFoundError:
            raise NotFoundError(f"Post {item_id} not found", code="post_not_found")

    def create(self, db: Session, data: dict):
        try:
            return self.repo.create(db, data)
        except IntegrityDatabaseError:
            raise ConflictError("Post already exists", code="post_conflict")

    def update(self, db: Session, item_id: int, data: dict, user_id: int):
        try:
            post = self.repo.get_by_id(db, item_id)
        except RepoNotFoundError:
            raise NotFoundError(f"Post {item_id} not found", code="post_not_found")

        if post.author_id != user_id:
            raise ForbiddenError("You are not the owner of this post")

        return self.repo.update(db, item_id, data)

    def delete(self, db: Session, item_id: int, user_id: int):
        try:
            post = self.repo.get_by_id(db, item_id)
        except RepoNotFoundError:
            raise NotFoundError(f"Post {item_id} not found", code="post_not_found")

        if post.author_id != user_id:
            raise ForbiddenError("You are not the owner of this post")

        self.repo.delete(db, item_id)