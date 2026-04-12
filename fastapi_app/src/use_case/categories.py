from sqlalchemy.orm import Session

from ..infrastructure.repositories.categories import CategoryRepository
from ..infrastructure.module.exceptions import NotFoundError as RepoNotFoundError, IntegrityDatabaseError

from ..core.exceptions.http import NotFoundError, ConflictError


class CategoryUseCase:

    def __init__(self):
        self.repo = CategoryRepository()

    def get_all(self, db: Session):
        return self.repo.get_all(db)

    def get_one(self, db: Session, item_id: int):
        try:
            return self.repo.get_by_id(db, item_id)
        except RepoNotFoundError:
            raise NotFoundError(f"Category {item_id} not found", code="category_not_found")

    def create(self, db: Session, data: dict):
        try:
            return self.repo.create(db, data)
        except IntegrityDatabaseError:
            raise ConflictError("Category already exists", code="category_conflict")

    def update(self, db: Session, item_id: int, data: dict):
        try:
            return self.repo.update(db, item_id, data)
        except RepoNotFoundError:
            raise NotFoundError(f"Category {item_id} not found", code="category_not_found")

    def delete(self, db: Session, item_id: int):
        try:
            self.repo.delete(db, item_id)
        except RepoNotFoundError:
            raise NotFoundError(f"Category {item_id} not found", code="category_not_found")