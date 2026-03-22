from fastapi import APIRouter, HTTPException
from datetime import datetime
from typing import List
from ..schemas.posts import PostCreate, PostRead

router = APIRouter(prefix="/posts")

db = []
counter = 1


@router.get("/", response_model=List[PostRead])
def get_all():
    return db


@router.get("/{item_id}", response_model=PostRead)
def get_one(item_id: int):
    if item_id < 1 or item_id > len(db):
        raise HTTPException(status_code=404, detail="Post not found")
    return db[item_id - 1]


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


@router.put("/{item_id}", response_model=PostRead)
def update(item_id: int, item: PostCreate):
    if item_id < 1 or item_id > len(db):
        raise HTTPException(status_code=404, detail="Post not found")

    updated = {
        "id": item_id,
        "created_at": db[item_id - 1]["created_at"],
        **item.dict()
    }
    db[item_id - 1] = updated
    return updated


@router.delete("/{item_id}")
def delete(item_id: int):
    if item_id < 1 or item_id > len(db):
        raise HTTPException(status_code=404, detail="Post not found")

    db.pop(item_id - 1)
    return {"ok": True}