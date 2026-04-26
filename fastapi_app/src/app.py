from pathlib import Path

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from starlette.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError

from src.core.exceptions.handlers import (
    validation_exception_handler,
    app_exception_handler,
)
from src.core.exceptions.http import AppException

from .api.categories import router as categories_router
from .api.posts import router as posts_router
from .api.locations import router as locations_router
from .api.comments import router as comments_router
from .api.auth import router as auth_router


def create_app() -> FastAPI:
    app = FastAPI(title="FastAPI Blog", root_path="/api/v1")

    app.add_exception_handler(RequestValidationError, validation_exception_handler)
    app.add_exception_handler(AppException, app_exception_handler)

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    media_dir = Path(__file__).resolve().parent.parent / "media"
    media_dir.mkdir(parents=True, exist_ok=True)
    app.mount("/media", StaticFiles(directory=media_dir), name="media")

    app.include_router(categories_router)
    app.include_router(posts_router)
    app.include_router(locations_router)
    app.include_router(comments_router)
    app.include_router(auth_router)

    return app