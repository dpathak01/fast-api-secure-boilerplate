class UserDomainError(Exception):
    """Base class for user domain errors."""


class UserAlreadyExistsError(UserDomainError):
    """Raised when a user email is already registered."""


class InvalidCredentialsError(UserDomainError):
    """Raised when login credentials do not match any active user."""


class UserDisabledError(UserDomainError):
    """Raised when a disabled user attempts an authenticated action."""


class UserNotFoundError(UserDomainError):
    """Raised when a user cannot be found."""


class UserPermissionDeniedError(UserDomainError):
    """Raised when a user tries to act on another user's account."""
