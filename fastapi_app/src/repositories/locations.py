from sqlalchemy.orm import Session
from infrastructure.module.models.locations import Location


class LocationRepository:

    def get_all(self, db: Session):
        return db.query(Location).all()

    def get_by_id(self, db: Session, item_id: int):
        return db.query(Location).filter(Location.id == item_id).first()

    def create(self, db: Session, data: dict):
        obj = Location(**data)
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