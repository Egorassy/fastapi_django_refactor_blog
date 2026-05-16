from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from ..schemas.locations import LocationCreate, LocationRead
from .dependencies import get_db, get_current_user
from ..use_case.locations import LocationUseCase

router = APIRouter(prefix="/locations", tags=["Locations"])
use_case = LocationUseCase()


@router.get("/", response_model=list[LocationRead])
async def get_all(db: AsyncSession = Depends(get_db)):
    return await use_case.get_all(db)


@router.get("/{item_id}", response_model=LocationRead)
async def get_one(item_id: int, db: AsyncSession = Depends(get_db)):
    return await use_case.get_one(db, item_id)


@router.post("/", response_model=LocationRead)
async def create(
    item: LocationCreate,
    db: AsyncSession = Depends(get_db),
    user=Depends(get_current_user),
):
    return await use_case.create(db, item.dict())


@router.put("/{item_id}", response_model=LocationRead)
async def update(
    item_id: int,
    item: LocationCreate,
    db: AsyncSession = Depends(get_db),
    user=Depends(get_current_user),
):
    return await use_case.update(db, item_id, item.dict())


@router.delete("/{item_id}")
async def delete(
    item_id: int,
    db: AsyncSession = Depends(get_db),
    user=Depends(get_current_user),
):
    await use_case.delete(db, item_id)
    return {"ok": True}