"""Compatibility imports for API schemas.

New code should import schemas from app.api.v1.schemas.
"""

from app.api.v1.schemas import (
    LoginRequest,
    TokenResponse,
    UserBase,
    UserCreate,
    UserResponse,
    UserUpdateRequest as UserUpdate,
)

__all__ = [
    "LoginRequest",
    "TokenResponse",
    "UserBase",
    "UserCreate",
    "UserResponse",
    "UserUpdate",
]
