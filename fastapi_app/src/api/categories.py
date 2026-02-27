from fastapi import APIRouter, HTTPException
from typing import List
from ..schemas.schemas import CategoryCreate, CategoryRead
from datetime import datetime

router = APIRouter(prefix="/categories", tags=["categories"])

_categories: dict[int, dict] = {}
_next_id = 1


@router.get("/", response_model=List[CategoryRead])
def list_categories(skip: int = 0, limit: int = 100):
    items = list(_categories.values())[skip: skip + limit]
    return items


@router.post("/", response_model=CategoryRead, status_code=201)
def create_category(data: CategoryCreate):
    global _next_id
    now = datetime.utcnow()
    obj = data.dict()
    obj.update({"id": _next_id, "created_at": now})
    _categories[_next_id] = obj
    _next_id += 1
    return obj


@router.get("/{category_id}", response_model=CategoryRead)
def read_category(category_id: int):
    obj = _categories.get(category_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Category not found")
    return obj


@router.put("/{category_id}", response_model=CategoryRead)
def update_category(category_id: int, data: CategoryCreate):
    obj = _categories.get(category_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Category not found")
    updated = obj.copy()
    updated.update(data.dict())
    _categories[category_id] = updated
    return updated


@router.delete("/{category_id}")
def delete_category(category_id: int):
    if category_id not in _categories:
        raise HTTPException(status_code=404, detail="Category not found")
    del _categories[category_id]
    return {"deleted": True}