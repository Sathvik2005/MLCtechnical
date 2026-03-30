from pymongo import MongoClient
from pymongo.database import Database
from app.core.config import settings


_client: MongoClient | None = None


def get_db() -> Database:
    global _client
    if _client is None:
        if not settings.mongo_uri:
            raise RuntimeError("MONGO_URI is required")
        _client = MongoClient(settings.mongo_uri)
    return _client[settings.database_name]
