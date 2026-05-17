from fastapi.responses import JSONResponse
from pydantic import BaseModel
from fastapi import status, Request


class HttpExceptionResponse(BaseModel):
    loc: list[str]
    msg: str
    type: str


def handle_exception(_: Request, exception: Exception) -> JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "detail": str(exception),
        },
    )
