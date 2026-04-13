from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ..schemas.comments import CommentCreate, CommentRead
from .dependencies import get_db
from ..use_case.comments import CommentUseCase

router = APIRouter(prefix="/comments")

use_case = CommentUseCase()


@router.get("/", response_model=list[CommentRead])
def get_all(db: Session = Depends(get_db)):
    return use_case.get_all(db)


@router.get("/{item_id}", response_model=CommentRead)
def get_one(item_id: int, db: Session = Depends(get_db)):
    return use_case.get_one(db, item_id)


@router.post("/", response_model=CommentRead)
def create(item: CommentCreate, db: Session = Depends(get_db)):
    return use_case.create(db, item.dict())


@router.put("/{item_id}", response_model=CommentRead)
def update(item_id: int, item: CommentCreate, db: Session = Depends(get_db)):
    return use_case.update(db, item_id, item.dict())


@router.delete("/{item_id}")
def delete(item_id: int, db: Session = Depends(get_db)):
    use_case.delete(db, item_id)
    return {"ok": True}