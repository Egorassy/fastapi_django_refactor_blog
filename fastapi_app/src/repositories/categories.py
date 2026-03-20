from sqlalchemy.orm import Session
from ..models.categories import Category


class CategoryRepository:

    def get_all(self, db: Session):
        return db.query(Category).all()

    def get_by_id(self, db: Session, item_id: int):
        return db.query(Category).filter(Category.id == item_id).first()

    def create(self, db: Session, data: dict):
        obj = Category(**data)
        db.add(obj)
        db.commit()
        db.refresh(obj)
        return obj

    def update(self, db: Session, item_id: int, data: dict):
        obj = self.get_by_id(db, item_id)
        for key, value in data.items():
            setattr(obj, key, value)
        db.commit()
        db.refresh(obj)
        return obj

    def delete(self, db: Session, item_id: int):
        obj = self.get_by_id(db, item_id)
        db.delete(obj)
        db.commit()