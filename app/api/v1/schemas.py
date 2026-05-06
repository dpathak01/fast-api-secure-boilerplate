from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr, Field

from app.core.security import AuthToken
from app.modules.users.entities import User


class UserBase(BaseModel):
    """Base user schema."""

    email: EmailStr = Field(..., description="User email address")
    full_name: str = Field(..., min_length=1, max_length=100)
    is_active: bool = True


class UserCreate(UserBase):
    """Schema for creating a new user."""

    password: str = Field(..., min_length=8, description="Password")


class UserUpdateRequest(BaseModel):
    """Schema for updating user."""

    full_name: Optional[str] = Field(None, min_length=1, max_length=100)
    email: Optional[EmailStr] = None
    is_active: Optional[bool] = None


class UserResponse(UserBase):
    """Schema for user responses."""

    id: str
    created_at: datetime
    updated_at: datetime


class TokenResponse(BaseModel):
    """JWT token response."""

    access_token: str
    token_type: str = "bearer"
    expires_in: int


class LoginRequest(BaseModel):
    """Login credentials."""

    email: EmailStr
    password: str


def user_to_response(user: User) -> UserResponse:
    return UserResponse(
        id=user.id or "",
        email=user.email,
        full_name=user.full_name,
        is_active=user.is_active,
        created_at=user.created_at,
        updated_at=user.updated_at,
    )


def token_to_response(token: AuthToken) -> TokenResponse:
    return TokenResponse(
        access_token=token.access_token,
        token_type=token.token_type,
        expires_in=token.expires_in,
    )
