from fastapi import APIRouter, Depends, HTTPException, status
from pymongo.database import Database
from pymongo.errors import DuplicateKeyError
from bson.objectid import ObjectId
from datetime import datetime

from app.database import get_database
from app.models import UserCreate, UserResponse, UserUpdate, TokenResponse, LoginRequest
from app.security import security_utils, get_current_user_id

router = APIRouter(prefix="/api/v1/users", tags=["Users"])


@router.post("/register", response_model=TokenResponse, status_code=status.HTTP_201_CREATED)
async def register(user_data: UserCreate, db: Database = Depends(get_database)):
    """Register a new user."""
    users_collection = db["users"]

    # Check if user already exists
    if users_collection.find_one({"email": user_data.email}):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User with this email already exists",
        )

    # Hash password and prepare user document
    user_doc = {
        "email": user_data.email,
        "full_name": user_data.full_name,
        "hashed_password": security_utils.hash_password(user_data.password),
        "is_active": user_data.is_active,
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow(),
    }

    result = users_collection.insert_one(user_doc)
    user_id = str(result.inserted_id)

    # Create JWT token
    token, expires_in = security_utils.create_access_token(data={"sub": user_id})

    return TokenResponse(
        access_token=token,
        expires_in=expires_in,
    )


@router.post("/login", response_model=TokenResponse)
async def login(credentials: LoginRequest, db: Database = Depends(get_database)):
    """Login user and return JWT token."""
    users_collection = db["users"]

    user = users_collection.find_one({"email": credentials.email})
    if not user or not security_utils.verify_password(
        credentials.password, user["hashed_password"]
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
        )

    if not user.get("is_active", True):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User account is disabled",
        )

    user_id = str(user["_id"])
    token, expires_in = security_utils.create_access_token(data={"sub": user_id})

    return TokenResponse(
        access_token=token,
        expires_in=expires_in,
    )


@router.get("/me", response_model=UserResponse)
async def get_current_user(
    user_id: str = Depends(get_current_user_id),
    db: Database = Depends(get_database),
):
    """Get current authenticated user."""
    users_collection = db["users"]

    try:
        user = users_collection.find_one({"_id": ObjectId(user_id)})
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    return UserResponse(
        id=str(user["_id"]),
        email=user["email"],
        full_name=user["full_name"],
        is_active=user["is_active"],
        created_at=user["created_at"],
        updated_at=user["updated_at"],
    )


@router.get("/{user_id}", response_model=UserResponse)
async def get_user(
    user_id: str,
    db: Database = Depends(get_database),
):
    """Get user by ID."""
    users_collection = db["users"]

    try:
        user = users_collection.find_one({"_id": ObjectId(user_id)})
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    return UserResponse(
        id=str(user["_id"]),
        email=user["email"],
        full_name=user["full_name"],
        is_active=user["is_active"],
        created_at=user["created_at"],
        updated_at=user["updated_at"],
    )


@router.put("/{user_id}", response_model=UserResponse)
async def update_user(
    user_id: str,
    user_data: UserUpdate,
    current_user_id: str = Depends(get_current_user_id),
    db: Database = Depends(get_database),
):
    """Update user (only user can update their own profile)."""
    users_collection = db["users"]

    # Authorization check
    if user_id != current_user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to update this user",
        )

    try:
        user_obj_id = ObjectId(user_id)
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    # Check if email is already taken
    if user_data.email:
        existing_user = users_collection.find_one(
            {"email": user_data.email, "_id": {"$ne": user_obj_id}}
        )
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Email already in use",
            )

    # Prepare update data
    update_data = {k: v for k, v in user_data.dict().items() if v is not None}
    update_data["updated_at"] = datetime.utcnow()

    result = users_collection.find_one_and_update(
        {"_id": user_obj_id},
        {"$set": update_data},
        return_document=True,
    )

    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    return UserResponse(
        id=str(result["_id"]),
        email=result["email"],
        full_name=result["full_name"],
        is_active=result["is_active"],
        created_at=result["created_at"],
        updated_at=result["updated_at"],
    )


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(
    user_id: str,
    current_user_id: str = Depends(get_current_user_id),
    db: Database = Depends(get_database),
):
    """Delete user (only user can delete their own account)."""
    users_collection = db["users"]

    # Authorization check
    if user_id != current_user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to delete this user",
        )

    try:
        user_obj_id = ObjectId(user_id)
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    result = users_collection.delete_one({"_id": user_obj_id})

    if result.deleted_count == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
