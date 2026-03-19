from fastapi import APIRouter
from datetime import datetime
from typing import List
from ..schemas.categories import CategoryCreate, CategoryRead

router = APIRouter(prefix="/categories")

db = []
counter = 1


@router.get("/", response_model=List[CategoryRead])
def get_all():
    return db


@router.get("/{item_id}", response_model=CategoryRead)
def get_one(item_id: int):
    return db[item_id - 1]


@router.post("/", response_model=CategoryRead)
def create(item: CategoryCreate):
    global counter
    new_item = {
        "id": counter,
        "created_at": datetime.now(),
        **item.dict()
    }
    db.append(new_item)
    counter += 1
    return new_item


@router.put("/{item_id}", response_model=CategoryRead)
def update(item_id: int, item: CategoryCreate):
    updated = {
        "id": item_id,
        "created_at": db[item_id - 1]["created_at"],
        **item.dict()
    }
    db[item_id - 1] = updated
    return updated


@router.delete("/{item_id}")
def delete(item_id: int):
    db.pop(item_id - 1)
    return {"ok": True}