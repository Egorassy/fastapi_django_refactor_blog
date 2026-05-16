from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from ..schemas.comments import CommentCreate, CommentRead
from .dependencies import get_db, get_current_user
from ..use_case.comments import CommentUseCase

router = APIRouter(prefix="/comments", tags=["Comments"])
use_case = CommentUseCase()


@router.get("/", response_model=list[CommentRead])
async def get_all(db: AsyncSession = Depends(get_db)):
    return await use_case.get_all(db)


@router.get("/{item_id}", response_model=CommentRead)
async def get_one(item_id: int, db: AsyncSession = Depends(get_db)):
    return await use_case.get_one(db, item_id)


@router.post("/", response_model=CommentRead)
async def create(
    item: CommentCreate,
    db: AsyncSession = Depends(get_db),
    user=Depends(get_current_user),
):
    data = item.dict()
    data["author_id"] = user.id
    return await use_case.create(db, data)


@router.put("/{item_id}", response_model=CommentRead)
async def update(
    item_id: int,
    item: CommentCreate,
    db: AsyncSession = Depends(get_db),
    user=Depends(get_current_user),
):
    return await use_case.update(db, item_id, item.dict(), user.id)


@router.delete("/{item_id}")
async def delete(
    item_id: int,
    db: AsyncSession = Depends(get_db),
    user=Depends(get_current_user),
):
    await use_case.delete(db, item_id, user.id)
    return {"ok": True}