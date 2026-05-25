from sqlalchemy import select
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from ..module.exceptions import DatabaseError, IntegrityDatabaseError, NotFoundError
from ..module.models.users import User


class UserRepository:
    async def get_all(self, db: AsyncSession):
        result = await db.execute(select(User))
        return result.scalars().all()

    async def get_by_username(self, db: AsyncSession, username: str):
        result = await db.execute(select(User).where(User.username == username))
        return result.scalar_one_or_none()

    async def get_by_id(self, db: AsyncSession, user_id: int):
        obj = await db.get(User, user_id)
        if not obj:
            raise NotFoundError("User", user_id)
        return obj

    async def create(self, db: AsyncSession, data: dict):
        try:
            obj = User(**data)
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

    async def update(self, db: AsyncSession, user_id: int, data: dict):
        obj = await self.get_by_id(db, user_id)

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
