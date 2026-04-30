from collections.abc import AsyncGenerator

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession

from ..infrastructure.module.db import AsyncSessionLocal
from ..core.security.jwt import decode_token
from ..core.exceptions.http import UnauthorizedError
from ..infrastructure.repositories.users import UserRepository

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        yield session

async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: AsyncSession = Depends(get_db),
):
    payload = decode_token(token)
    if not payload:
        raise UnauthorizedError("Invalid token")

    user_id = payload.get("sub")
    if not user_id:
        raise UnauthorizedError("Invalid token payload")

    repo = UserRepository()
    return await repo.get_by_id(db, int(user_id))