from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError, SQLAlchemyError

from ..module.models import Comment
from ..module.exceptions import (
    NotFoundError,
    DatabaseError,
    IntegrityDatabaseError,
)


class CommentRepository:

    def get_all(self, db: Session):
        return db.query(Comment).all()

    def get_by_id(self, db: Session, item_id: int):
        obj = db.query(Comment).filter(Comment.id == item_id).first()
        if not obj:
            raise NotFoundError("Comment", item_id)
        return obj

    def create(self, db: Session, data: dict):
        try:
            obj = Comment(**data)
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

        except IntegrityError:
            db.rollback()
            raise IntegrityDatabaseError()

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