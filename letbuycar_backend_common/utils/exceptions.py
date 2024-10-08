from fastapi import Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

async def validation_exception_handler(request: Request, exc: RequestValidationError):
    errors = exc.errors()
    formatted_errors = {}
    for error in errors:
        loc = error.get("loc")
        field = loc[-1] if loc else "unknown"
        formatted_errors[field] = {
            "msg": error.get("msg"),
            "type": error.get("type")
        }
    return JSONResponse(
        status_code=422,
        content={"errors": formatted_errors}
    )