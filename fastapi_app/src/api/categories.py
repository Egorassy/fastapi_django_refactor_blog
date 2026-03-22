from fastapi import APIRouter, HTTPException
from datetime import datetime
from typing import List
from ..schemas.categories import CategoryCreate, CategoryRead

router = APIRouter(prefix="/categories")

db = []
counter = 1


def get_category_or_404(item_id: int):
    if item_id < 1 or item_id > len(db):
        raise HTTPException(status_code=404, detail="Category not found")
    return db[item_id - 1]


@router.get("/", response_model=List[CategoryRead])
def get_all():
    return db


@router.get("/{item_id}", response_model=CategoryRead)
def get_one(item_id: int):
    return get_category_or_404(item_id)


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
    existing = get_category_or_404(item_id)

    updated = {
        "id": item_id,
        "created_at": existing["created_at"],
        **item.dict()
    }

    db[item_id - 1] = updated
    return updated


@router.delete("/{item_id}")
def delete(item_id: int):
    get_category_or_404(item_id)

    db.pop(item_id - 1)
    return {"ok": True}