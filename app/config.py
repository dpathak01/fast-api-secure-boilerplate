import os
from typing import Literal
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings with environment-based configuration."""

    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=True,
        extra="ignore",
    )

    # Environment
    ENV: Literal["dev", "qa", "prod"] = "dev"
    DEBUG: bool = False

    # Server
    APP_NAME: str = "FastAPI Secure Boilerplate"
    APP_VERSION: str = "1.0.0"
    HOST: str = "0.0.0.0"
    PORT: int = 8000

    # Database
    MONGODB_URL: str = "mongodb://localhost:27017"
    MONGODB_DB_NAME: str = "fastapi_db"

    # JWT
    JWT_SECRET_KEY: str = "your-secret-key-change-in-production"
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRATION_HOURS: int = 24

    # Security
    CORS_ORIGINS: list[str] = ["http://localhost:3000", "http://localhost:8000"]
    CORS_ALLOW_CREDENTIALS: bool = True
    CORS_ALLOW_METHODS: list[str] = ["*"]
    CORS_ALLOW_HEADERS: list[str] = ["*"]

    @property
    def is_production(self) -> bool:
        return self.ENV == "prod"

    @property
    def is_development(self) -> bool:
        return self.ENV == "dev"


def get_settings() -> Settings:
    """Load settings from environment."""
    app_env = os.getenv("APP_ENV")

    if app_env:
        env_file = f".env.{app_env}"
        if os.path.exists(env_file):
            return Settings(_env_file=env_file)

    if os.path.exists(".env"):
        return Settings(_env_file=".env")

    return Settings()


settings = get_settings()
