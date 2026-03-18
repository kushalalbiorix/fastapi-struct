"""
Sliding-window rate limiter via Redis.
 
Usage in a router:
    from app.utils.rate_limit import rate_limit
 
    @router.get("/endpoint", dependencies=[Depends(rate_limit())])
    async def endpoint(): ...
 
    # Custom limit:
    @router.post("/login", dependencies=[Depends(rate_limit(max_calls=5, window_seconds=60))])
    async def login(): ...
"""
from fastapi import Depends, HTTPException, Request, status
 
from app.core.config import settings
from app.utils.cache import cache


def rate_limit(
    max_calls: int | None = None,
    window_seconds: int = 60,
):
    """
    Returns a FastAPI dependency that enforces a per-IP rate limit.
    Falls back gracefully if Redis is unavailable.
    """
    effective_max = max_calls or settings.RATE_LIMIT_PER_MINUTE
    async def _check(request: Request):
        client_ip = request.client.host if request.client else "unknown"
        key = f"rate_limit:{client_ip}:{request.url.path}"
 
        count = await cache.incr(key, ttl=window_seconds)
        if count > effective_max:
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail=f"Rate limit exceeded. Max {effective_max} requests per {window_seconds}s.",
                headers={"Retry-After": str(window_seconds)},
            )
            
    return _check