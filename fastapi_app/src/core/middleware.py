import logging
import time

from fastapi import FastAPI, Request

logger = logging.getLogger("app.requests")


def setup_middlewares(app: FastAPI) -> None:
    @app.middleware("http")
    async def log_requests(request: Request, call_next):
        start = time.perf_counter()
        user_id = getattr(request.state, "user_id", None)

        try:
            response = await call_next(request)
        except Exception:
            duration_ms = (time.perf_counter() - start) * 1000
            logger.exception(
                "method=%s path=%s status=%s user_id=%s duration_ms=%.2f",
                request.method,
                request.url.path,
                500,
                user_id if user_id is not None else "-",
                duration_ms,
            )
            raise

        duration_ms = (time.perf_counter() - start) * 1000

        logger.info(
            "method=%s path=%s status=%s user_id=%s duration_ms=%.2f",
            request.method,
            request.url.path,
            response.status_code,
            user_id if user_id is not None else "-",
            duration_ms,
        )

        return response
