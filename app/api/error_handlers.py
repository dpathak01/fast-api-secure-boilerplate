from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse

from app.modules.users.errors import (
    InvalidCredentialsError,
    UserAlreadyExistsError,
    UserDisabledError,
    UserDomainError,
    UserNotFoundError,
    UserPermissionDeniedError,
)


def register_exception_handlers(app: FastAPI) -> None:
    """Register HTTP mappings for domain errors."""

    @app.exception_handler(UserDomainError)
    async def user_domain_exception_handler(
        request: Request,
        exc: UserDomainError,
    ) -> JSONResponse:
        return JSONResponse(
            status_code=_status_code_for(exc),
            content={"detail": str(exc)},
        )


def _status_code_for(exc: UserDomainError) -> int:
    if isinstance(exc, UserAlreadyExistsError):
        return status.HTTP_409_CONFLICT
    if isinstance(exc, InvalidCredentialsError):
        return status.HTTP_401_UNAUTHORIZED
    if isinstance(exc, (UserDisabledError, UserPermissionDeniedError)):
        return status.HTTP_403_FORBIDDEN
    if isinstance(exc, UserNotFoundError):
        return status.HTTP_404_NOT_FOUND
    return status.HTTP_400_BAD_REQUEST
