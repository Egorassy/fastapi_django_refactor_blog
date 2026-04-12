from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..schemas.locations import LocationCreate, LocationRead
from .dependencies import get_db

from ..use_case.locations import LocationUseCase
from src.core.exceptions.http import NotFoundError

router = APIRouter(prefix="/locations")

use_case = LocationUseCase()


@router.get("/", response_model=list[LocationRead])
def get_all(db: Session = Depends(get_db)):
    return use_case.get_all(db)


@router.get("/{item_id}", response_model=LocationRead)
def get_one(item_id: int, db: Session = Depends(get_db)):
    try:
        return use_case.get_one(db, item_id)
    except NotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.post("/", response_model=LocationRead)
def create(item: LocationCreate, db: Session = Depends(get_db)):
    return use_case.create(db, item.dict())


@router.put("/{item_id}", response_model=LocationRead)
def update(item_id: int, item: LocationCreate, db: Session = Depends(get_db)):
    try:
        return use_case.update(db, item_id, item.dict())
    except NotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.delete("/{item_id}")
def delete(item_id: int, db: Session = Depends(get_db)):
    try:
        use_case.delete(db, item_id)
        return {"ok": True}
    except NotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))