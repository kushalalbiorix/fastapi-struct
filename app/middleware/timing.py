import time

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses  import Response
from fastapi import HTTPException

class TimingMiddleware(BaseHTTPMiddleware):
    
    """Adds X-Process-Time header to every response."""
     
    async def dispatch(self, request: Request, call_next) -> Response:
        
        start = time.perf_counter()
        response = await call_next(request)
        duration = time.perf_counter() - start
        response.headers["X-Process-Time"] = f"{duration:.4f}s"
        return response
    

            
        
        
        