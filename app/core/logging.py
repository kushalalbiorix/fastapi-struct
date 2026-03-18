import logging
import sys

from app.core.config import settings

def setup_logging() -> None:
    log_level = getattr(logging, settings.LOG_LEVEL.upper(), logging.INFO)
    
    if settings.LOG_FORMAT == "json":
        try:
            import structlog
 
            structlog.configure(
                processors=[
                    structlog.contextvars.merge_contextvars,
                    structlog.stdlib.add_log_level,
                    structlog.stdlib.add_logger_name,
                    structlog.processors.TimeStamper(fmt="iso"),
                    structlog.processors.StackInfoRenderer(),
                    structlog.processors.format_exc_info,
                    structlog.processors.JSONRenderer(),
                ],
                logger_factory=structlog.stdlib.LoggerFactory(),
                wrapper_class=structlog.stdlib.BoundLogger,
                cache_logger_on_first_use=True,
            )
        except ImportError:
            _setup_standard_logging(log_level)
    else:
        _setup_standard_logging(log_level)
        

def _setup_standard_logging(log_level: int) -> None:
    fmt = "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s"
    logging.basicConfig(
        level=log_level,
        format=fmt,
        handlers=[logging.StreamHandler(sys.stdout)],
    )
    # Silence noisy libraries
    logging.getLogger("uvicorn.access").setLevel(logging.WARNING)
    logging.getLogger("sqlalchemy.engine").setLevel(logging.WARNING)
    
    
def get_logger(name: str) -> logging.Logger:
    return logging.getLogger(name)