from sqlalchemy.ext.asyncio import AsyncSession

from ..core.exceptions.http import ConflictError, UnauthorizedError
from ..core.security.jwt import create_access_token
from ..core.security.password import verify_password, hash_password
from ..infrastructure.repositories.users import UserRepository
from ..infrastructure.module.exceptions import IntegrityDatabaseError


class AuthUseCase:
    def __init__(self):
        self.repo = UserRepository()

    async def login(self, db: AsyncSession, username: str, password: str):
        user = await self.repo.get_by_username(db, username)

        if not user or not verify_password(password, user.hashed_password):
            raise UnauthorizedError("Invalid credentials", code="invalid_credentials")

        return create_access_token({"sub": str(user.id)})

    async def register(self, db: AsyncSession, data: dict):
        try:
            data = data.copy()
            password = data.pop("password")
            data["hashed_password"] = hash_password(password)

            return await self.repo.create(db, data)
        except IntegrityDatabaseError:
            raise ConflictError("User already exists", code="user_conflict")
