from pathlib import Path

from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi.staticfiles import StaticFiles
from starlette.middleware.cors import CORSMiddleware

from src.core.exceptions.handlers import (
    app_exception_handler,
    validation_exception_handler,
)
from src.core.exceptions.http import AppException
from src.core.logging import setup_logging
from src.core.middleware import setup_middlewares
from src.core.settings import settings

from .api.auth import router as auth_router
from .api.categories import router as categories_router
from .api.comments import router as comments_router
from .api.locations import router as locations_router
from .api.posts import router as posts_router
from .api.users import router as users_router


def create_app() -> FastAPI:
    setup_logging()
    tags_metadata = [
        {"name": "Auth", "description": "Login, register, logout"},
        {"name": "Users", "description": "User profiles"},
        {"name": "Posts", "description": "Blog posts"},
        {"name": "Categories", "description": "Post categories"},
        {"name": "Locations", "description": "Post locations"},
        {"name": "Comments", "description": "Post comments"},
    ]

    app = FastAPI(title=settings.app_name, openapi_tags=tags_metadata)

    app.add_exception_handler(RequestValidationError, validation_exception_handler)
    app.add_exception_handler(AppException, app_exception_handler)

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )



    setup_middlewares(app)

    media_dir = Path(settings.media_dir)
    media_dir.mkdir(parents=True, exist_ok=True)
    app.mount("/media", StaticFiles(directory=media_dir), name="media")

    app.include_router(auth_router)
    app.include_router(users_router)
    app.include_router(categories_router)
    app.include_router(posts_router)
    app.include_router(locations_router)
    app.include_router(comments_router)

    return app