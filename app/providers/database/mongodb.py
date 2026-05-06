from contextlib import contextmanager
from typing import Generator, Optional

from pymongo import MongoClient
from pymongo.database import Database

from app.config import settings


class MongoDBConnection:
    """Singleton MongoDB connection handler."""

    _instance: Optional["MongoDBConnection"] = None
    _client: Optional[MongoClient] = None
    _db: Optional[Database] = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def connect(self) -> Database:
        """Establish MongoDB connection."""
        if self._client is None:
            self._client = MongoClient(settings.MONGODB_URL)
            self._db = self._client[settings.MONGODB_DB_NAME]
            self._client.admin.command("ping")

        if self._db is None:
            raise RuntimeError("MongoDB database was not initialized")

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
            return self.connect()
        return self._db


db_connection = MongoDBConnection()


def get_database() -> Database:
    """FastAPI dependency for getting the active database."""
    return db_connection.get_db()


@contextmanager
def get_db_context() -> Generator[Database, None, None]:
    """Context manager for scripts and one-off database operations."""
    yield get_database()
