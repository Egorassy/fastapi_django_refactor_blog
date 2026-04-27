from sqlalchemy.orm import Session
from ..infrastructure.repositories.users import UserRepository
from ..core.security.password import hash_password
from ..core.exceptions.http import ConflictError, NotFoundError
from ..infrastructure.module.exceptions import NotFoundError as RepoNotFoundError


class UserUseCase:

    def __init__(self):
        self.repo = UserRepository()

    def get_all(self, db: Session):
        return self.repo.get_all(db)

    def get_one(self, db: Session, user_id: int):
        try:
            return self.repo.get_by_id(db, user_id)
        except RepoNotFoundError:
            raise NotFoundError(f"User {user_id} not found", code="user_not_found")

    def create(self, db: Session, username: str, password: str):
        existing = self.repo.get_by_username(db, username)
        if existing:
            raise ConflictError("User already exists", code="user_conflict")

        return self.repo.create(db, {
            "username": username,
            "hashed_password": hash_password(password)
        })