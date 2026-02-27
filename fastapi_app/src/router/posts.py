from fastapi import APIRouter, HTTPException
from typing import List
from schemas.schemas import PostCreate, PostRead
from datetime import datetime

router = APIRouter(prefix="/posts", tags=["posts"])

_posts: dict[int, dict] = {}
_next_post_id = 1


@router.get("/", response_model=List[PostRead])
def list_posts(skip: int = 0, limit: int = 100):
    items = list(_posts.values())[skip: skip + limit]
    return items


@router.post("/", response_model=PostRead, status_code=201)
def create_post(data: PostCreate):
    global _next_post_id
    now = datetime.utcnow()
    obj = data.dict()
    obj.update({"id": _next_post_id, "created_at": now})
    _posts[_next_post_id] = obj
    _next_post_id += 1
    return obj


@router.get("/{post_id}", response_model=PostRead)
def read_post(post_id: int):
    obj = _posts.get(post_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Post not found")
    return obj


@router.put("/{post_id}", response_model=PostRead)
def update_post(post_id: int, data: PostCreate):
    obj = _posts.get(post_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Post not found")
    updated = obj.copy()
    updated.update(data.dict())
    _posts[post_id] = updated
    return updated


@router.delete("/{post_id}")
def delete_post(post_id: int):
    if post_id not in _posts:
        raise HTTPException(status_code=404, detail="Post not found")
    del _posts[post_id]
    return {"deleted": True}