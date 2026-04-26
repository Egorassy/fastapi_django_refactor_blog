from sqlalchemy.orm import Session

from ..core.exceptions.http import UnauthorizedError, ConflictError
from ..core.security.password import verify_password, hash_password
from ..core.security.jwt import create_access_token
from ..infrastructure.repositories.users import UserRepository


class AuthUseCase:
    def __init__(self):
        self.repo = UserRepository()

    def login(self, db: Session, username: str, password: str):
        user = self.repo.get_by_username(db, username)

        if not user or not verify_password(password, user.hashed_password):
            raise UnauthorizedError("Invalid credentials", code="invalid_credentials")

        return create_access_token({"sub": str(user.id)})

    def register(self, db: Session, username: str, password: str):
        existing = self.repo.get_by_username(db, username)
        if existing:
            raise ConflictError("User already exists", code="user_conflict")

        return self.repo.create(
            db,
            {
                "username": username,
                "hashed_password": hash_password(password),
                "is_active": True,
            },
        )