from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class User:
    """User aggregate root."""

    id: Optional[str]
    email: str
    full_name: str
    hashed_password: str
    is_active: bool
    created_at: datetime
    updated_at: datetime


@dataclass
class UserUpdate:
    """Mutable user fields accepted by the domain use cases."""

    full_name: Optional[str] = None
    email: Optional[str] = None
    is_active: Optional[bool] = None

    def has_changes(self) -> bool:
        return any(
            value is not None
            for value in (self.full_name, self.email, self.is_active)
        )
