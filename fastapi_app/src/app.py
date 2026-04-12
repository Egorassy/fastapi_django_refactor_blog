from fastapi import FastAPI, HTTPException
from starlette.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError
from src.core.exceptions.handlers import validation_exception_handler, http_404_exception_handler


from .api.categories import router as categories_router
from .api.posts import router as posts_router
from .api.locations import router as locations_router
from .api.comments import router as comments_router


def create_app() -> FastAPI:
    app = FastAPI(title="FastAPI Blog", root_path="/api/v1")

    app.add_exception_handler(
        RequestValidationError,
        validation_exception_handler
    )

    app.add_exception_handler(
        HTTPException,
        http_404_exception_handler
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(categories_router)
    app.include_router(posts_router)
    app.include_router(locations_router)
    app.include_router(comments_router)

    return app

def setup_exception_handlers(app: FastAPI):
    app.add_exception_handler(RequestValidationError, validation_exception_handler)