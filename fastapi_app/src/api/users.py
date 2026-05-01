from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from .dependencies import get_db
from ..schemas.users import UserRead
from ..use_case.users import UserUseCase

router = APIRouter(prefix="/users")
use_case = UserUseCase()


@router.get("/", response_model=list[UserRead])
async def get_all(db: AsyncSession = Depends(get_db)):
    return await use_case.get_all(db)


@router.get("/{user_id}", response_model=UserRead)
async def get_one(user_id: int, db: AsyncSession = Depends(get_db)):
    return await use_case.get_one(db, user_id)