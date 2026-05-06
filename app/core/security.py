from dataclasses import dataclass
from datetime import timedelta
from typing import Optional, Protocol


@dataclass(frozen=True)
class AuthToken:
    """Bearer token returned by authentication use cases."""

    access_token: str
    token_type: str
    expires_in: int


class InvalidTokenError(Exception):
    """Raised when an access token cannot be decoded or trusted."""


class PasswordHasher(Protocol):
    """Password hashing port."""

    def hash(self, password: str) -> str:
        """Return a secure password hash."""

    def verify(self, plain_password: str, hashed_password: str) -> bool:
        """Return whether the plain password matches the stored hash."""


class TokenService(Protocol):
    """Token issuing and validation port."""

    def create_access_token(
        self,
        subject: str,
        expires_delta: Optional[timedelta] = None,
    ) -> AuthToken:
        """Create an access token for a subject."""

    def get_subject(self, token: str) -> str:
        """Decode a token and return its subject."""
