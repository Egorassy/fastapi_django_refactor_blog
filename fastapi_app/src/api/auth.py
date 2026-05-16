from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from .dependencies import get_db, oauth2_scheme
from ..schemas.auth import Token
from ..schemas.users import UserCreate
from ..core.security.token_blacklist import revoke_token
from ..use_case.auth import AuthUseCase

router = APIRouter(prefix="/auth", tags=["Auth"])
use_case = AuthUseCase()


@router.post("/login", response_model=Token)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(get_db),
):
    token = await use_case.login(db, form_data.username, form_data.password)
    return {"access_token": token, "token_type": "bearer"}


@router.post("/register")
async def register(
    data: UserCreate,
    db: AsyncSession = Depends(get_db),
):
    user = await use_case.register(db, data.model_dump())
    return user


@router.post("/logout")
async def logout(token: str = Depends(oauth2_scheme)):
    revoke_token(token)
    return {"ok": True, "message": "Logged out"}
