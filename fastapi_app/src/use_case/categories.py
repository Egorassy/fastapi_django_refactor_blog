from sqlalchemy.ext.asyncio import AsyncSession

from ..infrastructure.repositories.categories import CategoryRepository
from ..infrastructure.module.exceptions import (
    NotFoundError as RepoNotFoundError,
    IntegrityDatabaseError,
)
from ..core.exceptions.http import NotFoundError, ConflictError


class CategoryUseCase:
    def __init__(self):
        self.repo = CategoryRepository()

    async def get_all(self, db: AsyncSession):
        return await self.repo.get_all(db)

    async def get_one(self, db: AsyncSession, item_id: int):
        try:
            return await self.repo.get_by_id(db, item_id)
        except RepoNotFoundError:
            raise NotFoundError(f"Category {item_id} not found", code="category_not_found")

    async def create(self, db: AsyncSession, data: dict):
        try:
            return await self.repo.create(db, data)
        except IntegrityDatabaseError:
            raise ConflictError("Category already exists", code="category_conflict")

    async def update(self, db: AsyncSession, item_id: int, data: dict):
        try:
            return await self.repo.update(db, item_id, data)
        except RepoNotFoundError:
            raise NotFoundError(f"Category {item_id} not found", code="category_not_found")

    async def delete(self, db: AsyncSession, item_id: int):
        try:
            await self.repo.delete(db, item_id)
        except RepoNotFoundError:
            raise NotFoundError(f"Category {item_id} not found", code="category_not_found")
