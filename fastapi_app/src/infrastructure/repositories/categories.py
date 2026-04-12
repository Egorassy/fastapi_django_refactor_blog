from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError, SQLAlchemyError

from infrastructure.module.models.categories import Category
from infrastructure.module.exceptions import (
    DatabaseError,
    IntegrityDatabaseError,
    NotFoundError,
)


class CategoryRepository:

    def get_all(self, db: Session):
        return db.query(Category).all()

    def get_by_id(self, db: Session, item_id: int):
        obj = db.query(Category).filter(Category.id == item_id).first()
        if not obj:
            raise NotFoundError()
        return obj

    def create(self, db: Session, data: dict):
        try:
            obj = Category(**data)
            db.add(obj)
            db.commit()
            db.refresh(obj)
            return obj

        except IntegrityError:
            db.rollback()
            raise IntegrityDatabaseError()

        except SQLAlchemyError:
            db.rollback()
            raise DatabaseError()

    def update(self, db: Session, item_id: int, data: dict):
        obj = self.get_by_id(db, item_id)

        try:
            for key, value in data.items():
                setattr(obj, key, value)

            db.commit()
            db.refresh(obj)
            return obj

        except SQLAlchemyError:
            db.rollback()
            raise DatabaseError()

    def delete(self, db: Session, item_id: int):
        obj = self.get_by_id(db, item_id)

        try:
            db.delete(obj)
            db.commit()
        except SQLAlchemyError:
            db.rollback()
            raise DatabaseError()