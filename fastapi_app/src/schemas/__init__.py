from fastapi import FastAPI

def create_app():
    app = FastAPI(title="FastAPI migration (minimal)")

    from .routers import categories, posts

    app.include_router(categories.router)
    app.include_router(posts.router)

    return app