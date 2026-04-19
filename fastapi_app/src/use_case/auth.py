from sqlalchemy.orm import Session

from ..infrastructure.repositories.users import UserRepository
from ..core.security.password import verify_password
from ..core.security.jwt import create_access_token
from ..core.exceptions.http import UnauthorizedError


class AuthUseCase:

    def __init__(self):
        self.repo = UserRepository()

    def login(self, db: Session, username: str, password: str):
        user = self.repo.get_by_username(db, username)

        if not user or not verify_password(password, user.hashed_password):
            raise UnauthorizedError("Invalid credentials")

        return create_access_token({"sub": str(user.id)})