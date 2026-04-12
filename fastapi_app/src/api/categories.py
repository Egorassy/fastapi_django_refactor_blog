from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..schemas.categories import CategoryCreate, CategoryRead
from .dependencies import get_db

from use_case.categories import CategoryUseCase
from use_case.exceptions import EntityNotFoundError, EntityAlreadyExistsError

router = APIRouter(prefix="/categories")

use_case = CategoryUseCase()


@router.get("/", response_model=list[CategoryRead])
def get_all(db: Session = Depends(get_db)):
    return use_case.get_all(db)


@router.get("/{item_id}", response_model=CategoryRead)
def get_one(item_id: int, db: Session = Depends(get_db)):
    try:
        return use_case.get_one(db, item_id)
    except EntityNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.post("/", response_model=CategoryRead)
def create(item: CategoryCreate, db: Session = Depends(get_db)):
    try:
        return use_case.create(db, item.dict())
    except EntityAlreadyExistsError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.put("/{item_id}", response_model=CategoryRead)
def update(item_id: int, item: CategoryCreate, db: Session = Depends(get_db)):
    try:
        return use_case.update(db, item_id, item.dict())
    except EntityNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.delete("/{item_id}")
def delete(item_id: int, db: Session = Depends(get_db)):
    try:
        use_case.delete(db, item_id)
        return {"ok": True}
    except EntityNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))