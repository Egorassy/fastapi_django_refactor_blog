from sqlalchemy.orm import Session
from ..models.posts import Post


class PostRepository:

    def get_all(self, db: Session):
        return db.query(Post).all()

    def get_by_id(self, db: Session, item_id: int):
        return db.query(Post).filter(Post.id == item_id).first()

    def create(self, db: Session, data: dict):
        obj = Post(**data)
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