from datetime import datetime
from typing import Optional

from bson.objectid import ObjectId
from pymongo import ReturnDocument
from pymongo.database import Database

from app.modules.users.entities import User, UserUpdate


class MongoUserRepository:
    """MongoDB implementation of the user repository port."""

    def __init__(self, database: Database) -> None:
        self._collection = database["users"]

    def find_by_email(self, email: str) -> Optional[User]:
        document = self._collection.find_one({"email": email})
        return self._to_user(document) if document else None

    def find_by_id(self, user_id: str) -> Optional[User]:
        object_id = self._to_object_id(user_id)
        if object_id is None:
            return None

        document = self._collection.find_one({"_id": object_id})
        return self._to_user(document) if document else None

    def email_exists_for_other_user(self, email: str, user_id: str) -> bool:
        object_id = self._to_object_id(user_id)
        if object_id is None:
            return False

        return bool(
            self._collection.find_one(
                {
                    "email": email,
                    "_id": {"$ne": object_id},
                }
            )
        )

    def create(self, user: User) -> User:
        document = self._to_document(user)
        result = self._collection.insert_one(document)
        return User(
            id=str(result.inserted_id),
            email=user.email,
            full_name=user.full_name,
            hashed_password=user.hashed_password,
            is_active=user.is_active,
            created_at=user.created_at,
            updated_at=user.updated_at,
        )

    def update(self, user_id: str, update: UserUpdate) -> Optional[User]:
        object_id = self._to_object_id(user_id)
        if object_id is None:
            return None

        update_data = {
            key: value
            for key, value in {
                "full_name": update.full_name,
                "email": update.email,
                "is_active": update.is_active,
            }.items()
            if value is not None
        }
        update_data["updated_at"] = datetime.utcnow()

        document = self._collection.find_one_and_update(
            {"_id": object_id},
            {"$set": update_data},
            return_document=ReturnDocument.AFTER,
        )
        return self._to_user(document) if document else None

    def delete(self, user_id: str) -> bool:
        object_id = self._to_object_id(user_id)
        if object_id is None:
            return False

        result = self._collection.delete_one({"_id": object_id})
        return result.deleted_count > 0

    @staticmethod
    def _to_object_id(user_id: str) -> Optional[ObjectId]:
        try:
            return ObjectId(user_id)
        except Exception:
            return None

    @staticmethod
    def _to_document(user: User) -> dict:
        return {
            "email": user.email,
            "full_name": user.full_name,
            "hashed_password": user.hashed_password,
            "is_active": user.is_active,
            "created_at": user.created_at,
            "updated_at": user.updated_at,
        }

    @staticmethod
    def _to_user(document: dict) -> User:
        return User(
            id=str(document["_id"]),
            email=document["email"],
            full_name=document["full_name"],
            hashed_password=document["hashed_password"],
            is_active=document.get("is_active", True),
            created_at=document["created_at"],
            updated_at=document["updated_at"],
        )
