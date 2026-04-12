from sqlalchemy.orm import Session

from ..infrastructure.repositories.comments import CommentRepository
from ..infrastructure.module.exceptions import NotFoundError
from use_case.exceptions import EntityNotFoundError


class CommentUseCase:

    def __init__(self):
        self.repo = CommentRepository()

    def get_all(self, db: Session):
        return self.repo.get_all(db)

    def get_one(self, db: Session, item_id: int):
        try:
            return self.repo.get_by_id(db, item_id)
        except NotFoundError:
            raise EntityNotFoundError("Comment", item_id)

    def create(self, db: Session, data: dict):
        return self.repo.create(db, data)

    def update(self, db: Session, item_id: int, data: dict):
        try:
            return self.repo.update(db, item_id, data)
        except NotFoundError:
            raise EntityNotFoundError("Comment", item_id)

    def delete(self, db: Session, item_id: int):
        try:
            self.repo.delete(db, item_id)
        except NotFoundError:
            raise EntityNotFoundError("Comment", item_id)