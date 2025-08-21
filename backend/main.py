"""
AskPostgres FastAPI Backend Application.

A professional backend service for querying PostgreSQL databases 
using natural language through OpenRouter LLM integration.
"""
import logging
import sys
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import structlog

from app.config import settings
from app.database import db_manager
from app.routes import router
from app.models import ErrorResponse


# Configure structured logging
structlog.configure(
    processors=[
        structlog.stdlib.filter_by_level,
        structlog.stdlib.add_logger_name,
        structlog.stdlib.add_log_level,
        structlog.stdlib.PositionalArgumentsFormatter(),
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.StackInfoRenderer(),
        structlog.processors.format_exc_info,
        structlog.processors.UnicodeDecoder(),
        structlog.processors.JSONRenderer()
    ],
    context_class=dict,
    logger_factory=structlog.stdlib.LoggerFactory(),
    wrapper_class=structlog.stdlib.BoundLogger,
    cache_logger_on_first_use=True,
)

# Set up logging
logging.basicConfig(
    format="%(message)s",
    stream=sys.stdout,
    level=getattr(logging, settings.log_level.upper())
)

logger = structlog.get_logger()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Application lifespan manager for startup and shutdown events.
    """
    # Startup
    logger.info("Starting AskPostgres backend application")
    
    try:
        # Initialize database connection
        await db_manager.initialize()
        logger.info("Database connection initialized")
        
        # Test database connection
        if await db_manager.test_connection():
            logger.info("Database connection test successful")
        else:
            logger.warning("Database connection test failed")
        
    except Exception as e:
        logger.error(f"Failed to initialize application: {e}")
        raise
    
    yield
    
    # Shutdown
    logger.info("Shutting down AskPostgres backend application")
    await db_manager.close()
    logger.info("Database connections closed")


# Create FastAPI application
app = FastAPI(
    title="AskPostgres API",
    description="Backend API for querying PostgreSQL databases using natural language",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins_list,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)


# Global exception handler
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """Handle unexpected exceptions."""
    logger.error(f"Unhandled exception: {exc}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content=ErrorResponse(
            error="Internal server error",
            details=["An unexpected error occurred. Please try again later."]
        ).dict()
    )


# Include API routes
app.include_router(router, prefix="/api/v1", tags=["api"])


# Root endpoint
@app.get("/")
async def root():
    """Root endpoint with basic API information."""
    return {
        "name": "AskPostgres API",
        "version": "1.0.0",
        "description": "Backend API for querying PostgreSQL databases using natural language",
        "docs": "/docs",
        "health": "/api/v1/health"
    }


# Additional middleware for request logging
@app.middleware("http")
async def log_requests(request: Request, call_next):
    """Log all incoming requests."""
    start_time = time.time()
    
    # Get client IP
    client_ip = request.headers.get("X-Forwarded-For", request.client.host if request.client else "unknown")
    
    logger.info(
        "Request started",
        method=request.method,
        url=str(request.url),
        client_ip=client_ip
    )
    
    response = await call_next(request)
    
    process_time = time.time() - start_time
    logger.info(
        "Request completed",
        method=request.method,
        url=str(request.url),
        status_code=response.status_code,
        process_time=round(process_time, 4)
    )
    
    return response


if __name__ == "__main__":
    import uvicorn
    import time
    
    uvicorn.run(
        "main:app",
        host=settings.api_host,
        port=settings.api_port,
        reload=True,
        log_level=settings.log_level.lower()
    )
