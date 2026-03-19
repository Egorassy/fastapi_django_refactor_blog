from fastapi import APIRouter
from datetime import datetime
from typing import List
from schemas.comments import CommentCreate, CommentRead

router = APIRouter(prefix="/comments")

db = []
counter = 1


@router.get("/", response_model=List[CommentRead])
def get_all():
    return db


@router.post("/", response_model=CommentRead)
def create(item: CommentCreate):
    global counter
    new_item = {
        "id": counter,
        "created_at": datetime.now(),
        **item.dict()
    }
    db.append(new_item)
    counter += 1
    return new_item