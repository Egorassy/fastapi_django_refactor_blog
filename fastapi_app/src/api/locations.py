from fastapi import APIRouter, HTTPException
from datetime import datetime
from typing import List
from ..schemas.locations import LocationCreate, LocationRead

router = APIRouter(prefix="/locations")

db = []
counter = 1


@router.get("/", response_model=List[LocationRead])
def get_all():
    return db


@router.get("/{item_id}", response_model=LocationRead)
def get_one(item_id: int):
    if item_id < 1 or item_id > len(db):
        raise HTTPException(status_code=404, detail="Location not found")
    return db[item_id - 1]


@router.post("/", response_model=LocationRead)
def create(item: LocationCreate):
    global counter
    new_item = {
        "id": counter,
        "created_at": datetime.now(),
        **item.dict()
    }
    db.append(new_item)
    counter += 1
    return new_item


@router.put("/{item_id}", response_model=LocationRead)
def update(item_id: int, item: LocationCreate):
    if item_id < 1 or item_id > len(db):
        raise HTTPException(status_code=404, detail="Location not found")

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
        raise HTTPException(status_code=404, detail="Location not found")

    db.pop(item_id - 1)
    return {"ok": True}