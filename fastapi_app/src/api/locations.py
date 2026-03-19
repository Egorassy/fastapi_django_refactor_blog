from fastapi import APIRouter
from datetime import datetime
from typing import List
from schemas.locations import LocationCreate, LocationRead

router = APIRouter(prefix="/locations")

db = []
counter = 1


@router.get("/", response_model=List[LocationRead])
def get_all():
    return db


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