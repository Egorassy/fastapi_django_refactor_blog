from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from .dependencies import get_db
from ..schemas.auth import Token, UserCreate
from ..use_case.auth import AuthUseCase

router = APIRouter(prefix="/auth")
use_case = AuthUseCase()


@router.post("/login", response_model=Token)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    token = use_case.login(db, form_data.username, form_data.password)
    return {"access_token": token, "token_type": "bearer"}


@router.post("/register")
def register(
    data: UserCreate,
    db: Session = Depends(get_db),
):
    user = use_case.register(db, data.username, data.password)
    return {
        "id": user.id,
        "username": user.username,
        "is_active": user.is_active,
    }