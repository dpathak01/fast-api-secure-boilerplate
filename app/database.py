from pymongo import MongoClient
from pymongo.database import Database
from contextlib import contextmanager
from typing import Generator

from app.config import settings


class MongoDBConnection:
    """Singleton MongoDB connection handler."""

    _instance: "MongoDBConnection" = None
    _client: MongoClient = None
    _db: Database = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def connect(self) -> Database:
        """Establish MongoDB connection."""
        if self._client is None:
            self._client = MongoClient(settings.MONGODB_URL)
            self._db = self._client[settings.MONGODB_DB_NAME]
            # Verify connection
            self._client.admin.command("ping")
        return self._db

    def disconnect(self) -> None:
        """Close MongoDB connection."""
        if self._client:
            self._client.close()
            self._client = None
            self._db = None

    def get_db(self) -> Database:
        """Get database instance."""
        if self._db is None:
            self.connect()
        return self._db


# Global connection instance
db_connection = MongoDBConnection()


def get_database() -> Database:
    """Dependency for getting database instance."""
    return db_connection.get_db()


@contextmanager
def get_db_context() -> Generator[Database, None, None]:
    """Context manager for database operations."""
    try:
        db = get_database()
        yield db
    finally:
        pass
