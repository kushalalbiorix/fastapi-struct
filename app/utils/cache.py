"""
Thin async Redis cache wrapper.
 
Usage:
    from app.utils.cache import cache
 
    await cache.set("key", {"data": 1}, ttl=300)
    value = await cache.get("key")
    await cache.delete("key")
"""


import json
import logging
from typing import Any,Optional

import redis.asyncio as aioredis
from app.core.config import settings

logger = logging.getLogger(__name__)

_redis: Optional[aioredis.Redis] = None


async def get_redis():
    global _redis
    
    if _redis is None:
        _redis = aioredis.from_url(
            settings.REDIS_URL,
            encoding = "utf-8",
            decode_response = True
            
        )
    
    return _redis


class Cache:
    
    async def get(self,key:str) -> Optional[Any]:
        try:
            r = await get_redis()
            raw = await r.get(key)
            return json.loads(raw) if raw is not None else None
        except Exception as exc:
            logger.warning("Cache GET failed for key=%s: %s", key, exc)
            return None
        
    
    async def set(self,key:str,value: Any,ttl:int=300):
        try:
            r = await get_redis()
            await r.set(key, json.dumps(value), ex=ttl)
            return True
        except Exception as exc:
            logger.warning("Cache SET failed for key=%s: %s", key, exc)
            return False
    
    async def delete(self, key: str) -> bool:
        try:
            r = await get_redis()
            await r.delete(key)
            return True
        except Exception as exc:
            logger.warning("Cache DELETE failed for key=%s: %s", key, exc)
            return False
    
    async def exists(self, key: str) -> bool:
        try:
            r = await get_redis()
            return bool(await r.exists(key))
        except Exception:
            return False
 
 
    async def incr(self, key: str, ttl: int = 60) -> int:
        """Atomic increment — useful for rate limiting."""
        r = await get_redis()
        pipe = r.pipeline()
        await pipe.incr(key)
        await pipe.expire(key, ttl)
        results = await pipe.execute()
        return results[0]


cache = Cache()
