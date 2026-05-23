from datetime import datetime

from fastapi import APIRouter, Depends, File, Form, Request, UploadFile
from sqlalchemy.ext.asyncio import AsyncSession

from ..infrastructure.module.files import save_post_image
from ..schemas.posts import PostRead
from ..use_case.posts import PostUseCase
from .dependencies import get_current_user, get_db

router = APIRouter(prefix="/posts", tags=["Posts"])
use_case = PostUseCase()


def serialize_post(post, request: Request) -> dict:
    return {
        "id": post.id,
        "title": post.title,
        "text": post.text,
        "pub_date": post.pub_date,
        "author_id": post.author_id,
        "location_id": post.location_id,
        "category_id": post.category_id,
        "image": str(request.url_for("media", path=post.image)) if post.image else None,
        "is_published": post.is_published,
        "created_at": post.created_at,
    }


@router.get("/", response_model=list[PostRead])
async def get_all(request: Request, db: AsyncSession = Depends(get_db)):
    posts = await use_case.get_all(db)
    return [serialize_post(post, request) for post in posts]


@router.get("/{item_id}", response_model=PostRead)
async def get_one(item_id: int, request: Request, db: AsyncSession = Depends(get_db)):
    post = await use_case.get_one(db, item_id)
    return serialize_post(post, request)


@router.post("/", response_model=PostRead)
async def create(
    request: Request,
    title: str = Form(...),
    text: str = Form(...),
    pub_date: datetime = Form(...),
    location_id: int | None = Form(None),
    category_id: int | None = Form(None),
    image: UploadFile | None = File(None),
    db: AsyncSession = Depends(get_db),
    user=Depends(get_current_user),
):
    data = {
        "title": title,
        "text": text,
        "pub_date": pub_date,
        "author_id": user.id,
        "location_id": location_id,
        "category_id": category_id,
        "is_published": True,
    }

    if image is not None:
        data["image"] = save_post_image(image)

    post = await use_case.create(db, data)
    return serialize_post(post, request)


@router.put("/{item_id}", response_model=PostRead)
async def update(
    item_id: int,
    request: Request,
    title: str = Form(...),
    text: str = Form(...),
    pub_date: datetime = Form(...),
    location_id: int | None = Form(None),
    category_id: int | None = Form(None),
    image: UploadFile | None = File(None),
    db: AsyncSession = Depends(get_db),
    user=Depends(get_current_user),
):
    data = {
        "title": title,
        "text": text,
        "pub_date": pub_date,
        "location_id": location_id,
        "category_id": category_id,
        "is_published": True,
    }

    if image is not None:
        data["image"] = save_post_image(image)

    post = await use_case.update(db, item_id, data, user.id)
    return serialize_post(post, request)


@router.post("/{item_id}/image", response_model=PostRead)
async def upload_image(
    item_id: int,
    request: Request,
    image: UploadFile = File(...),
    db: AsyncSession = Depends(get_db),
    user=Depends(get_current_user),
):
    post = await use_case.update(
        db,
        item_id,
        {"image": save_post_image(image)},
        user.id,
    )
    return serialize_post(post, request)


@router.delete("/{item_id}")
async def delete(
    item_id: int,
    db: AsyncSession = Depends(get_db),
    user=Depends(get_current_user),
):
    await use_case.delete(db, item_id, user.id)
    return {"ok": True}
