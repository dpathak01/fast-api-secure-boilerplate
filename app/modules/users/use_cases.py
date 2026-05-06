from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from app.core.security import AuthToken, PasswordHasher, TokenService
from app.modules.users.entities import User, UserUpdate
from app.modules.users.errors import (
    InvalidCredentialsError,
    UserAlreadyExistsError,
    UserDisabledError,
    UserNotFoundError,
    UserPermissionDeniedError,
)
from app.modules.users.contracts import UserRepository


@dataclass(frozen=True)
class RegisterUserCommand:
    email: str
    full_name: str
    password: str
    is_active: bool = True


@dataclass(frozen=True)
class LoginUserCommand:
    email: str
    password: str


@dataclass(frozen=True)
class UpdateUserCommand:
    full_name: Optional[str] = None
    email: Optional[str] = None
    is_active: Optional[bool] = None


class UserService:
    """Application service for user use cases."""

    def __init__(
        self,
        user_repository: UserRepository,
        password_hasher: PasswordHasher,
        token_service: TokenService,
    ) -> None:
        self._user_repository = user_repository
        self._password_hasher = password_hasher
        self._token_service = token_service

    def register_user(self, command: RegisterUserCommand) -> AuthToken:
        if self._user_repository.find_by_email(command.email):
            raise UserAlreadyExistsError("User with this email already exists")

        now = datetime.utcnow()
        user = User(
            id=None,
            email=command.email,
            full_name=command.full_name,
            hashed_password=self._password_hasher.hash(command.password),
            is_active=command.is_active,
            created_at=now,
            updated_at=now,
        )
        created_user = self._user_repository.create(user)
        if not created_user.id:
            raise UserNotFoundError("User was not persisted correctly")

        return self._token_service.create_access_token(subject=created_user.id)

    def login_user(self, command: LoginUserCommand) -> AuthToken:
        user = self._user_repository.find_by_email(command.email)
        if not user or not self._password_hasher.verify(
            command.password,
            user.hashed_password,
        ):
            raise InvalidCredentialsError("Invalid email or password")

        if not user.is_active:
            raise UserDisabledError("User account is disabled")

        if not user.id:
            raise UserNotFoundError("User not found")

        return self._token_service.create_access_token(subject=user.id)

    def get_user(self, user_id: str) -> User:
        user = self._user_repository.find_by_id(user_id)
        if not user:
            raise UserNotFoundError("User not found")
        return user

    def update_user(
        self,
        user_id: str,
        current_user_id: str,
        command: UpdateUserCommand,
    ) -> User:
        if user_id != current_user_id:
            raise UserPermissionDeniedError("Not authorized to update this user")

        update = UserUpdate(
            full_name=command.full_name,
            email=command.email,
            is_active=command.is_active,
        )

        if update.email and self._user_repository.email_exists_for_other_user(
            update.email,
            user_id,
        ):
            raise UserAlreadyExistsError("Email already in use")

        updated_user = self._user_repository.update(user_id, update)
        if not updated_user:
            raise UserNotFoundError("User not found")

        return updated_user

    def delete_user(self, user_id: str, current_user_id: str) -> None:
        if user_id != current_user_id:
            raise UserPermissionDeniedError("Not authorized to delete this user")

        deleted = self._user_repository.delete(user_id)
        if not deleted:
            raise UserNotFoundError("User not found")
