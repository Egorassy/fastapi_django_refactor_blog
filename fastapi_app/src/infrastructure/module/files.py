from pathlib import Path
from uuid import uuid4
import shutil

from fastapi import UploadFile

from ...core.exceptions.http import BadRequestError


MEDIA_ROOT = Path(__file__).resolve().parents[3] / "media"
POSTS_DIR = MEDIA_ROOT / "posts"

ALLOWED_IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".gif", ".webp"}
ALLOWED_IMAGE_CONTENT_TYPES = {
    "image/jpeg",
    "image/png",
    "image/gif",
    "image/webp",
}


def validate_post_image(image: UploadFile) -> None:
    suffix = Path(image.filename or "").suffix.lower()
    content_type = (image.content_type or "").lower()

    if suffix not in ALLOWED_IMAGE_EXTENSIONS:
        raise BadRequestError(
            "Unsupported image extension",
            code="invalid_image_type",
        )

    if content_type not in ALLOWED_IMAGE_CONTENT_TYPES:
        raise BadRequestError(
            "Unsupported image content type",
            code="invalid_image_type",
        )


def save_post_image(image: UploadFile) -> str:
    validate_post_image(image)

    POSTS_DIR.mkdir(parents=True, exist_ok=True)

    suffix = Path(image.filename or "").suffix.lower()
    filename = f"{uuid4().hex}{suffix}"
    file_path = POSTS_DIR / filename

    image.file.seek(0)

    with file_path.open("wb") as buffer:
        shutil.copyfileobj(image.file, buffer)

    return f"posts/{filename}"


def delete_post_image(image_path: str | None) -> None:
    if not image_path:
        return

    file_path = (MEDIA_ROOT / image_path).resolve()
    media_root = MEDIA_ROOT.resolve()

    if not file_path.is_relative_to(media_root):
        return

    if file_path.exists():
        file_path.unlink()

    parent = file_path.parent
    if parent.exists() and not any(parent.iterdir()):
        parent.rmdir()
