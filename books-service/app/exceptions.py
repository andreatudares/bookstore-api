"""HTTP Exceptions."""

import json

from fastapi import HTTPException, Request, status
from fastapi.responses import JSONResponse

from app.database import exceptions as db_exceptions
from app.schemas import response as response_schemas


class NotFoundException(HTTPException):
    """Not Found Exception."""

    def __init__(self, detail: str) -> None:
        super().__init__(status_code=status.HTTP_404_NOT_FOUND, detail=detail)


class InternalServerErrorException(HTTPException):
    """Internal Server Exception."""

    def __init__(self, detail: str = "Internal Server Error.") -> None:
        super().__init__(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=detail,
        )


class CustomExceptionHandler:
    """Custom Exception Handler."""

    @staticmethod
    async def handle_exception(
        request: Request,  # noqa: ARG004
        exception: Exception,
    ) -> JSONResponse:
        response_exception: HTTPException
        if isinstance(exception, db_exceptions.DatabaseNotFoundException):
            response_exception = NotFoundException(detail=exception.message)
        else:
            response_exception = InternalServerErrorException()
        return JSONResponse(
            status_code=response_exception.status_code,
            content=json.loads(
                response_schemas.ResponseModel(
                    success=False,
                    message=response_exception.detail,
                    errors=[
                        response_schemas.ErrorDetailModel(
                            field="general",
                            issue=f"{response_exception.detail}",
                        )
                    ],
                ).model_dump_json()
            ),
        )
