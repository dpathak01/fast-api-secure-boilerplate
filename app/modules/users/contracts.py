from typing import Optional, Protocol

from app.modules.users.entities import User, UserUpdate


class UserRepository(Protocol):
    """Persistence contract needed by the user application service."""

    def find_by_email(self, email: str) -> Optional[User]:
        """Return a user by email, if one exists."""

    def find_by_id(self, user_id: str) -> Optional[User]:
        """Return a user by ID, if one exists."""

    def email_exists_for_other_user(self, email: str, user_id: str) -> bool:
        """Return whether an email belongs to a different user."""

    def create(self, user: User) -> User:
        """Persist a new user and return it with its assigned ID."""

    def update(self, user_id: str, update: UserUpdate) -> Optional[User]:
        """Apply a partial update and return the updated user."""

    def delete(self, user_id: str) -> bool:
        """Delete a user by ID."""
