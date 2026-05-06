from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError

from app.config import settings
from app.providers.database import db_connection
from app.middleware import setup_middleware
from app.api.error_handlers import register_exception_handlers
from app.api.v1 import api_router

# Initialize FastAPI app
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    debug=settings.DEBUG,
)

# Setup middleware (CORS, security headers, etc.)
setup_middleware(app)
register_exception_handlers(app)

# Include routers
app.include_router(api_router)


@app.on_event("startup")
async def startup_event():
    """Initialize database connection on startup."""
    try:
        db_connection.connect()
        print(f"✓ Connected to MongoDB: {settings.MONGODB_DB_NAME}")
    except Exception as e:
        print(f"✗ Failed to connect to MongoDB: {e}")
        raise


@app.on_event("shutdown")
async def shutdown_event():
    """Close database connection on shutdown."""
    db_connection.disconnect()
    print("✓ Disconnected from MongoDB")


@app.get("/health", tags=["Health"])
async def health_check():
    """Health check endpoint."""
    return {
        "status": "ok",
        "environment": settings.ENV,
        "app": settings.APP_NAME,
    }


@app.get("/", tags=["Root"])
async def root():
    """Root endpoint."""
    return {
        "message": f"Welcome to {settings.APP_NAME}",
        "version": settings.APP_VERSION,
        "docs": "/docs",
        "environment": settings.ENV,
    }


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    """Custom validation error handler."""
    return JSONResponse(
        status_code=422,
        content={
            "detail": exc.errors(),
            "body": exc.body,
        },
    )
