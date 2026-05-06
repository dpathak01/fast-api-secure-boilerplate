from datetime import datetime, timedelta
from typing import Optional

from jose import JWTError, jwt

from app.core.security import AuthToken, InvalidTokenError
from app.config import settings


class JwtTokenService:
    """JWT implementation of the token service port."""

    def create_access_token(
        self,
        subject: str,
        expires_delta: Optional[timedelta] = None,
    ) -> AuthToken:
        expires_delta = expires_delta or timedelta(
            hours=settings.JWT_EXPIRATION_HOURS
        )
        expire = datetime.utcnow() + expires_delta
        payload = {"sub": subject, "exp": expire}
        access_token = jwt.encode(
            payload,
            settings.JWT_SECRET_KEY,
            algorithm=settings.JWT_ALGORITHM,
        )
        return AuthToken(
            access_token=access_token,
            token_type="bearer",
            expires_in=int(expires_delta.total_seconds()),
        )

    def get_subject(self, token: str) -> str:
        try:
            payload = jwt.decode(
                token,
                settings.JWT_SECRET_KEY,
                algorithms=[settings.JWT_ALGORITHM],
            )
        except JWTError as exc:
            raise InvalidTokenError("Invalid authentication credentials") from exc

        subject = payload.get("sub")
        if not subject:
            raise InvalidTokenError("Invalid authentication credentials")

        return subject
