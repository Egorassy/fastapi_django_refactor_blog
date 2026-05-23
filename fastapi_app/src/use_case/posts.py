from sqlalchemy.ext.asyncio import AsyncSession

from ..core.exceptions.http import ConflictError, ForbiddenError, NotFoundError
from ..infrastructure.module.exceptions import (
    IntegrityDatabaseError,
    NotFoundError as RepoNotFoundError,
)
from ..infrastructure.module.files import delete_post_image
from ..infrastructure.repositories.categories import CategoryRepository
from ..infrastructure.repositories.locations import LocationRepository
from ..infrastructure.repositories.posts import PostRepository


class PostUseCase:
    def __init__(self):
        self.repo = PostRepository()
        self.category_repo = CategoryRepository()
        self.location_repo = LocationRepository()

    async def get_all(self, db: AsyncSession):
        return await self.repo.get_all(db)

    async def get_one(self, db: AsyncSession, item_id: int):
        try:
            return await self.repo.get_by_id(db, item_id)
        except RepoNotFoundError:
            raise NotFoundError(f"Post {item_id} not found", code="post_not_found")

    async def create(self, db: AsyncSession, data: dict):
        await self._check_relations(db, data)

        try:
            return await self.repo.create(db, data)
        except IntegrityDatabaseError:
            raise ConflictError("Post already exists", code="post_conflict")

    async def update(self, db: AsyncSession, item_id: int, data: dict, user_id: int):
        await self._check_relations(db, data)

        try:
            post = await self.repo.get_by_id(db, item_id)
        except RepoNotFoundError:
            raise NotFoundError(f"Post {item_id} not found", code="post_not_found")

        if post.author_id != user_id:
            raise ForbiddenError("You are not the owner of this post")

        old_image = post.image
        updated_post = await self.repo.update(db, item_id, data)

        if old_image and old_image != updated_post.image:
            delete_post_image(old_image)

        return updated_post

    async def delete(self, db: AsyncSession, item_id: int, user_id: int):
        try:
            post = await self.repo.get_by_id(db, item_id)
        except RepoNotFoundError:
            raise NotFoundError(f"Post {item_id} not found", code="post_not_found")

        if post.author_id != user_id:
            raise ForbiddenError("You are not the owner of this post")

        await self.repo.delete(db, item_id)
        delete_post_image(post.image)

    async def _check_relations(self, db: AsyncSession, data: dict):
        location_id = data.get("location_id")
        if location_id is not None:
            try:
                await self.location_repo.get_by_id(db, location_id)
            except RepoNotFoundError:
                raise NotFoundError(
                    f"Location {location_id} not found",
                    code="location_not_found",
                )

        category_id = data.get("category_id")
        if category_id is not None:
            try:
                await self.category_repo.get_by_id(db, category_id)
            except RepoNotFoundError:
                raise NotFoundError(
                    f"Category {category_id} not found",
                    code="category_not_found",
                )
