from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from .dependencies import get_db
from ..schemas.users import UserRead
from ..use_case.users import UserUseCase

router = APIRouter(prefix="/users")
use_case = UserUseCase()


@router.get("/", response_model=list[UserRead])
def get_all(db: Session = Depends(get_db)):
    return use_case.get_all(db)


@router.get("/{user_id}", response_model=UserRead)
def get_one(user_id: int, db: Session = Depends(get_db)):
    return use_case.get_one(db, user_id)
