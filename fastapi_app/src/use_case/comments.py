from sqlalchemy.ext.asyncio import AsyncSession

from ..infrastructure.repositories.comments import CommentRepository
from ..infrastructure.module.exceptions import NotFoundError as RepoNotFoundError
from ..core.exceptions.http import NotFoundError, ForbiddenError


class CommentUseCase:
    def __init__(self):
        self.repo = CommentRepository()

    async def get_all(self, db: AsyncSession):
        return await self.repo.get_all(db)

    async def get_one(self, db: AsyncSession, item_id: int):
        try:
            return await self.repo.get_by_id(db, item_id)
        except RepoNotFoundError:
            raise NotFoundError(f"Comment {item_id} not found", code="comment_not_found")

    async def create(self, db: AsyncSession, data: dict):
        return await self.repo.create(db, data)

    async def update(self, db: AsyncSession, item_id: int, data: dict, user_id: int):
        try:
            comment = await self.repo.get_by_id(db, item_id)
        except RepoNotFoundError:
            raise NotFoundError(f"Comment {item_id} not found", code="comment_not_found")

        if comment.author_id != user_id:
            raise ForbiddenError("You are not the owner of this comment")

        return await self.repo.update(db, item_id, data)

    async def delete(self, db: AsyncSession, item_id: int, user_id: int):
        try:
            comment = await self.repo.get_by_id(db, item_id)
        except RepoNotFoundError:
            raise NotFoundError(f"Comment {item_id} not found", code="comment_not_found")

        if comment.author_id != user_id:
            raise ForbiddenError("You are not the owner of this comment")

        await self.repo.delete(db, item_id)
