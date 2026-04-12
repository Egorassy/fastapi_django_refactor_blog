from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError


async def validation_exception_handler(request: Request, exc: RequestValidationError):
    errors = exc.errors()

    for err in errors:
        if err.get("type") == "json_invalid":
            ctx = err.get("ctx", {})

            return JSONResponse(
                status_code=400,
                content={
                    "error": "INVALID_JSON",
                    "message": "Request body is not valid JSON",
                    "hint": "Check syntax: quotes, commas, boolean values (true/false)",
                    "location": {
                        "type": "body",
                        "position": err.get("loc", [None, None])[-1],
                    },
                    "debug": {
                        "parser_error": ctx.get("error")
                    }
                },
            )

    formatted = []

    for err in errors:
        formatted.append({
            "field": ".".join(map(str, err.get("loc", []))),
            "message": err.get("msg"),
            "type": err.get("type"),
            "input": err.get("input"),
        })

    return JSONResponse(
        status_code=422,
        content={
            "error": "VALIDATION_ERROR",
            "message": "Request validation failed",
            "details": formatted,
        },
    )

async def http_404_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=404,
        content={
            "error": "NOT_FOUND",
            "message": exc.detail or "Resource not found",
            "type": "HTTP_404_ERROR",
            "path": str(request.url),
            "method": request.method,
        },
    )