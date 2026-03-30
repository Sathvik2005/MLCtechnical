import json
from typing import Any
from app.core.config import settings

try:
    import redis
except Exception:  # pragma: no cover
    redis = None


_memory_cache: dict[str, Any] = {}
_redis_client = redis.from_url(settings.redis_url) if (redis and settings.redis_url) else None


def get_cache(key: str) -> Any | None:
    if _redis_client:
        raw = _redis_client.get(key)
        return json.loads(raw) if raw else None
    return _memory_cache.get(key)


def set_cache(key: str, value: Any, ttl_seconds: int = 3600) -> None:
    if _redis_client:
        _redis_client.setex(key, ttl_seconds, json.dumps(value))
    else:
        _memory_cache[key] = value
