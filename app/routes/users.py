"""Compatibility import for the v1 users API router."""

from fastapi import APIRouter

from app.api.v1.users import router as users_router

router = APIRouter(prefix="/api/v1")
router.include_router(users_router)

__all__ = ["router"]
