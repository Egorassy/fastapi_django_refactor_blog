from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from .dependencies import get_db, get_current_user
from ..schemas.users import UserEdit, UserEditRead, UserRead
from ..use_case.users import UserUseCase

router = APIRouter(prefix="/users", tags=["Users"])
use_case = UserUseCase()


@router.get("/", response_model=list[UserRead])
async def get_all(db: AsyncSession = Depends(get_db)):
    return await use_case.get_all(db)


@router.get("/{user_id}", response_model=UserRead)
async def get_one(user_id: int, db: AsyncSession = Depends(get_db)):
    return await use_case.get_one(db, user_id)


@router.post("/{user_id}/edit", response_model=UserEditRead)
async def edit_profile(
    user_id: int,
    data: UserEdit,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user),
):
    update_data = data.model_dump(exclude_unset=True)
    return await use_case.update_profile(
        db,
        user_id,
        current_user.id,
        update_data,
    )
