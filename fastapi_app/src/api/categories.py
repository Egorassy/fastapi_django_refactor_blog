from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List

from infrastructure.module.db import SessionLocal
from use_case.categories import CategoryUseCase
from use_case.exceptions import EntityNotFoundError

from ..schemas.categories import CategoryCreate, CategoryRead

router = APIRouter(prefix="/categories")
use_case = CategoryUseCase()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/", response_model=List[CategoryRead])
def get_all(db: Session = Depends(get_db)):
    return use_case.get_all(db)


@router.get("/{item_id}", response_model=CategoryRead)
def get_one(item_id: int, db: Session = Depends(get_db)):
    try:
        return use_case.get_one(db, item_id)
    except EntityNotFoundError:
        raise HTTPException(status_code=404, detail="Category not found")


@router.post("/", response_model=CategoryRead)
def create(item: CategoryCreate, db: Session = Depends(get_db)):
    return use_case.create(db, item.dict())


@router.put("/{item_id}", response_model=CategoryRead)
def update(item_id: int, item: CategoryCreate, db: Session = Depends(get_db)):
    try:
        return use_case.update(db, item_id, item.dict())
    except EntityNotFoundError:
        raise HTTPException(status_code=404, detail="Category not found")


@router.delete("/{item_id}")
def delete(item_id: int, db: Session = Depends(get_db)):
    try:
        use_case.delete(db, item_id)
        return {"ok": True}
    except EntityNotFoundError:
        raise HTTPException(status_code=404, detail="Category not found")