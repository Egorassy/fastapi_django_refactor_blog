from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm

from .dependencies import get_db
from ..use_case.auth import AuthUseCase
from ..schemas.auth import Token

router = APIRouter(prefix="/auth")

use_case = AuthUseCase()


@router.post("/login", response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    token = use_case.login(db, form_data.username, form_data.password)
    return {"access_token": token}