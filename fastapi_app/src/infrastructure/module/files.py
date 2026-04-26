from pathlib import Path
from uuid import uuid4
import shutil

from fastapi import UploadFile


MEDIA_ROOT = Path(__file__).resolve().parents[3] / "media"
POSTS_DIR = MEDIA_ROOT / "posts"


def save_post_image(image: UploadFile) -> str:
    POSTS_DIR.mkdir(parents=True, exist_ok=True)

    suffix = Path(image.filename or "").suffix
    filename = f"{uuid4().hex}{suffix}"
    file_path = POSTS_DIR / filename

    with file_path.open("wb") as buffer:
        shutil.copyfileobj(image.file, buffer)

    return f"posts/{filename}"
