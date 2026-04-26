from sqlalchemy.orm import Session
from ..infrastructure.repositories.users import UserRepository
from ..core.security.password import hash_password
from ..core.exceptions.http import ConflictError


class UserUseCase:

    def __init__(self):
        self.repo = UserRepository()

    def create(self, db: Session, username: str, password: str):
        existing = self.repo.get_by_username(db, username)
        if existing:
            raise ConflictError("User already exists")

        return self.repo.create(db, {
            "username": username,
            "hashed_password": hash_password(password)
        })