from fastapi import APIRouter, Depends, status

from app.modules.users import (
    LoginUserCommand,
    RegisterUserCommand,
    UpdateUserCommand,
    UserService,
)
from app.api.dependencies import (
    get_current_user_id,
    get_user_service,
)
from app.api.v1.schemas import (
    LoginRequest,
    TokenResponse,
    UserCreate,
    UserResponse,
    UserUpdateRequest,
    token_to_response,
    user_to_response,
)

router = APIRouter(prefix="/users", tags=["Users"])


@router.post(
    "/register",
    response_model=TokenResponse,
    status_code=status.HTTP_201_CREATED,
)
async def register(
    user_data: UserCreate,
    user_service: UserService = Depends(get_user_service),
) -> TokenResponse:
    """Register a new user."""
    token = user_service.register_user(
        RegisterUserCommand(
            email=str(user_data.email),
            full_name=user_data.full_name,
            password=user_data.password,
            is_active=user_data.is_active,
        )
    )
    return token_to_response(token)


@router.post("/login", response_model=TokenResponse)
async def login(
    credentials: LoginRequest,
    user_service: UserService = Depends(get_user_service),
) -> TokenResponse:
    """Login user and return JWT token."""
    token = user_service.login_user(
        LoginUserCommand(
            email=str(credentials.email),
            password=credentials.password,
        )
    )
    return token_to_response(token)


@router.get("/me", response_model=UserResponse)
async def get_current_user(
    current_user_id: str = Depends(get_current_user_id),
    user_service: UserService = Depends(get_user_service),
) -> UserResponse:
    """Get current authenticated user."""
    return user_to_response(user_service.get_user(current_user_id))


@router.get("/{user_id}", response_model=UserResponse)
async def get_user(
    user_id: str,
    user_service: UserService = Depends(get_user_service),
) -> UserResponse:
    """Get user by ID."""
    return user_to_response(user_service.get_user(user_id))


@router.put("/{user_id}", response_model=UserResponse)
async def update_user(
    user_id: str,
    user_data: UserUpdateRequest,
    current_user_id: str = Depends(get_current_user_id),
    user_service: UserService = Depends(get_user_service),
) -> UserResponse:
    """Update user. Users can update only their own profile."""
    updated_user = user_service.update_user(
        user_id=user_id,
        current_user_id=current_user_id,
        command=UpdateUserCommand(
            full_name=user_data.full_name,
            email=str(user_data.email) if user_data.email else None,
            is_active=user_data.is_active,
        ),
    )
    return user_to_response(updated_user)


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(
    user_id: str,
    current_user_id: str = Depends(get_current_user_id),
    user_service: UserService = Depends(get_user_service),
) -> None:
    """Delete user. Users can delete only their own account."""
    user_service.delete_user(user_id=user_id, current_user_id=current_user_id)
