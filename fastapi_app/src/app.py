from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from .api.categories import router as categories_router
from .api.posts import router as posts_router
from .api.locations import router as locations_router
from .api.comments import router as comments_router


def create_app() -> FastAPI:
    app = FastAPI(title="FastAPI Blog", root_path="/api/v1")

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