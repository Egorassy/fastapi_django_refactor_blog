from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError, SQLAlchemyError

from ..module.models.users import User
from ..module.exceptions import DatabaseError, IntegrityDatabaseError, NotFoundError


class UserRepository:

    def get_by_username(self, db: Session, username: str):
        return db.query(User).filter(User.username == username).first()

    def get_by_id(self, db: Session, user_id: int):
        obj = db.query(User).filter(User.id == user_id).first()
        if not obj:
            raise NotFoundError("User", user_id)
        return obj

    def create(self, db: Session, data: dict):
        try:
            obj = User(**data)
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