from sqlalchemy import select
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from ..module.exceptions import DatabaseError, IntegrityDatabaseError, NotFoundError
from ..module.models.categories import Category


class CategoryRepository:
    async def get_all(self, db: AsyncSession):
        result = await db.execute(select(Category))
        return result.scalars().all()

    async def get_by_id(self, db: AsyncSession, item_id: int):
        obj = await db.get(Category, item_id)
        if not obj:
            raise NotFoundError("Category", item_id)
        return obj

    async def create(self, db: AsyncSession, data: dict):
        try:
            obj = Category(**data)
            db.add(obj)
            await db.commit()
            await db.refresh(obj)
            return obj
        except IntegrityError:
            await db.rollback()
            raise IntegrityDatabaseError()
        except SQLAlchemyError:
            await db.rollback()
            raise DatabaseError()

    async def update(self, db: AsyncSession, item_id: int, data: dict):
        obj = await self.get_by_id(db, item_id)

        try:
            for key, value in data.items():
                setattr(obj, key, value)

            await db.commit()
            await db.refresh(obj)
            return obj
        except IntegrityError:
            await db.rollback()
            raise IntegrityDatabaseError()
        except SQLAlchemyError:
            await db.rollback()
            raise DatabaseError()

    async def delete(self, db: AsyncSession, item_id: int):
        obj = await self.get_by_id(db, item_id)

        try:
            await db.delete(obj)
            await db.commit()
        except IntegrityError:
            await db.rollback()
            raise IntegrityDatabaseError()
        except SQLAlchemyError:
            await db.rollback()
            raise DatabaseError()