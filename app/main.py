from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from app.core.config import settings
from app.db.session import engine
from app.middleware.timing import TimingMiddleware
from app.middleware.requestid import RequestIDMiddleware
from app.core.exceptions import register_exception_handlers
from app.core.logging import setup_logging
from app.api.v1.router import api_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan: startup and shutdown events."""
    setup_logging()
    # Add startup logic here (e.g., warm up caches, verify DB connectivity)
    yield
    # Add shutdown logic here (e.g., close connections, flush queues)
    await engine.dispose()

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description=settings.DESCRIPTION,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    docs_url=f"{settings.API_V1_STR}/docs",
    redoc_url=f"{settings.API_V1_STR}/redoc",
    lifespan=lifespan,
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(GZipMiddleware, minimum_size=1000)
app.add_middleware(TimingMiddleware)
app.add_middleware(RequestIDMiddleware)
register_exception_handlers(app)

app.include_router(api_router, prefix=settings.API_V1_STR)