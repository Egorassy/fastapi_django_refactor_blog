from sqlalchemy.ext.asyncio import AsyncSession

from ..core.exceptions.http import ConflictError, ForbiddenError, NotFoundError
from ..core.security.password import hash_password
from ..infrastructure.module.exceptions import NotFoundError as RepoNotFoundError, IntegrityDatabaseError
from ..infrastructure.repositories.users import UserRepository


class UserUseCase:
    def __init__(self):
        self.repo = UserRepository()

    async def get_all(self, db: AsyncSession):
        return await self.repo.get_all(db)

    async def get_one(self, db: AsyncSession, user_id: int):
        try:
            return await self.repo.get_by_id(db, user_id)
        except RepoNotFoundError:
            raise NotFoundError(f"User {user_id} not found", code="user_not_found")

    async def create(self, db: AsyncSession, data: dict):
        try:
            data = data.copy()
            data["hashed_password"] = hash_password(data.pop("password"))
            return await self.repo.create(db, data)
        except IntegrityDatabaseError:
            raise ConflictError("User already exists", code="user_conflict")

    async def update_profile(self, db: AsyncSession, user_id: int, current_user_id: int, data: dict):
        if user_id != current_user_id:
            raise ForbiddenError("You are not the owner of this profile")

        try:
            return await self.repo.update(db, user_id, data)
        except RepoNotFoundError:
            raise NotFoundError(f"User {user_id} not found", code="user_not_found")
        except IntegrityDatabaseError:
            raise ConflictError("User profile already exists", code="user_conflict")