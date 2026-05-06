"""Compatibility imports for security adapters.

New code should use app.providers.security and
app.api.dependencies directly.
"""

from datetime import timedelta
from typing import Optional

from app.providers.security import BcryptPasswordHasher, JwtTokenService
from app.api.dependencies import get_current_user_id


class SecurityUtils:
    """Legacy facade over the security infrastructure adapters."""

    def __init__(self) -> None:
        self._password_hasher = BcryptPasswordHasher()
        self._token_service = JwtTokenService()

    def hash_password(self, password: str) -> str:
        return self._password_hasher.hash(password)

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        return self._password_hasher.verify(plain_password, hashed_password)

    def create_access_token(
        self,
        data: dict,
        expires_delta: Optional[timedelta] = None,
    ) -> tuple[str, int]:
        token = self._token_service.create_access_token(
            subject=data["sub"],
            expires_delta=expires_delta,
        )
        return token.access_token, token.expires_in

    def decode_token(self, token: str) -> dict:
        return {"sub": self._token_service.get_subject(token)}


security_utils = SecurityUtils()

__all__ = ["SecurityUtils", "get_current_user_id", "security_utils"]
