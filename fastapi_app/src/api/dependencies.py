from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from ..infrastructure.module.db import SessionLocal
from ..core.security.jwt import decode_token
from ..core.exceptions.http import UnauthorizedError
from ..infrastructure.repositories.users import UserRepository


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):
    payload = decode_token(token)

    if not payload:
        raise UnauthorizedError("Invalid token")

    user_id = payload.get("sub")
    if not user_id:
        raise UnauthorizedError("Invalid token payload")

    repo = UserRepository()
    return repo.get_by_id(db, int(user_id))