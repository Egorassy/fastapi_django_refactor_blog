from sqlalchemy.orm import Session

from infrastructure.repositories.locations import LocationRepository
from infrastructure.module.exceptions import NotFoundError
from use_case.exceptions import EntityNotFoundError


class LocationUseCase:

    def __init__(self):
        self.repo = LocationRepository()

    def get_all(self, db: Session):
        return self.repo.get_all(db)

    def get_one(self, db: Session, item_id: int):
        try:
            return self.repo.get_by_id(db, item_id)
        except NotFoundError:
            raise EntityNotFoundError("Location", item_id)

    def create(self, db: Session, data: dict):
        return self.repo.create(db, data)

    def update(self, db: Session, item_id: int, data: dict):
        try:
            return self.repo.update(db, item_id, data)
        except NotFoundError:
            raise EntityNotFoundError("Location", item_id)

    def delete(self, db: Session, item_id: int):
        try:
            self.repo.delete(db, item_id)
        except NotFoundError:
            raise EntityNotFoundError("Location", item_id)