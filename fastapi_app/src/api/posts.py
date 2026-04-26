from datetime import datetime

from fastapi import APIRouter, Depends, File, Form, UploadFile
from sqlalchemy.orm import Session

from ..schemas.posts import PostRead
from .dependencies import get_db, get_current_user
from ..use_case.posts import PostUseCase
from ..infrastructure.module.files import save_post_image

router = APIRouter(prefix="/posts")
use_case = PostUseCase()


@router.get("/", response_model=list[PostRead])
def get_all(db: Session = Depends(get_db)):
    return use_case.get_all(db)


@router.get("/{item_id}", response_model=PostRead)
def get_one(item_id: int, db: Session = Depends(get_db)):
    return use_case.get_one(db, item_id)


@router.post("/", response_model=PostRead)
def create(
    title: str = Form(...),
    text: str = Form(...),
    pub_date: datetime = Form(...),
    location_id: int | None = Form(None),
    category_id: int | None = Form(None),
    image: UploadFile | None = File(None),
    db: Session = Depends(get_db),
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

    return use_case.create(db, data)


@router.put("/{item_id}", response_model=PostRead)
def update(
    item_id: int,
    title: str = Form(...),
    text: str = Form(...),
    pub_date: datetime = Form(...),
    location_id: int | None = Form(None),
    category_id: int | None = Form(None),
    image: UploadFile | None = File(None),
    db: Session = Depends(get_db),
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

    return use_case.update(db, item_id, data, user.id)


@router.delete("/{item_id}")
def delete(
    item_id: int,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    use_case.delete(db, item_id, user.id)
    return {"ok": True}