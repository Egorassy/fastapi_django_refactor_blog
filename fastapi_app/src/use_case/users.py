from sqlalchemy.ext.asyncio import AsyncSession

from ..infrastructure.repositories.users import UserRepository
from ..core.security.password import hash_password
from ..core.exceptions.http import ConflictError, NotFoundError
from ..infrastructure.module.exceptions import NotFoundError as RepoNotFoundError


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

    async def create(self, db: AsyncSession, username: str, password: str):
        existing = await self.repo.get_by_username(db, username)
        if existing:
            raise ConflictError("User already exists", code="user_conflict")

        return await self.repo.create(
            db,
            {
                "username": username,
                "hashed_password": hash_password(password),
            },
        )