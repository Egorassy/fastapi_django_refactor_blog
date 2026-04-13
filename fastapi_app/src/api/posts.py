from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ..schemas.posts import PostCreate, PostRead
from .dependencies import get_db
from ..use_case.posts import PostUseCase

router = APIRouter(prefix="/posts")

use_case = PostUseCase()


@router.get("/", response_model=list[PostRead])
def get_all(db: Session = Depends(get_db)):
    return use_case.get_all(db)


@router.get("/{item_id}", response_model=PostRead)
def get_one(item_id: int, db: Session = Depends(get_db)):
    return use_case.get_one(db, item_id)


@router.post("/", response_model=PostRead)
def create(item: PostCreate, db: Session = Depends(get_db)):
    return use_case.create(db, item.dict())


@router.put("/{item_id}", response_model=PostRead)
def update(item_id: int, item: PostCreate, db: Session = Depends(get_db)):
    return use_case.update(db, item_id, item.dict())


@router.delete("/{item_id}")
def delete(item_id: int, db: Session = Depends(get_db)):
    use_case.delete(db, item_id)
    return {"ok": True}