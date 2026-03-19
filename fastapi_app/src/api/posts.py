from fastapi import APIRouter
from datetime import datetime
from typing import List
from ..schemas.posts import PostCreate, PostRead

router = APIRouter(prefix="/posts")

db = []
counter = 1


@router.get("/", response_model=List[PostRead])
def get_all():
    return db


@router.post("/", response_model=PostRead)
def create(item: PostCreate):
    global counter
    new_item = {
        "id": counter,
        "created_at": datetime.now(),
        **item.dict()
    }
    db.append(new_item)
    counter += 1
    return new_item