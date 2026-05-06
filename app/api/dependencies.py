from functools import lru_cache

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from pymongo.database import Database

from app.core.security import InvalidTokenError
from app.modules.users import UserService
from app.providers.database import get_database
from app.providers.security import BcryptPasswordHasher, JwtTokenService
from app.providers.users import MongoUserRepository

security_scheme = HTTPBearer()


@lru_cache
def get_password_hasher() -> BcryptPasswordHasher:
    return BcryptPasswordHasher()


@lru_cache
def get_token_service() -> JwtTokenService:
    return JwtTokenService()


def get_user_repository(
    db: Database = Depends(get_database),
) -> MongoUserRepository:
    return MongoUserRepository(db)


def get_user_service(
    user_repository: MongoUserRepository = Depends(get_user_repository),
    password_hasher: BcryptPasswordHasher = Depends(get_password_hasher),
    token_service: JwtTokenService = Depends(get_token_service),
) -> UserService:
    return UserService(
        user_repository=user_repository,
        password_hasher=password_hasher,
        token_service=token_service,
    )


async def get_current_user_id(
    credentials: HTTPAuthorizationCredentials = Depends(security_scheme),
    token_service: JwtTokenService = Depends(get_token_service),
) -> str:
    try:
        return token_service.get_subject(credentials.credentials)
    except InvalidTokenError as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        ) from exc
