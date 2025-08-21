"""
API routes for AskPostgres backend.
"""
import logging
from datetime import datetime
from typing import Dict, Any

from fastapi import APIRouter, HTTPException, Request, Depends
from fastapi.responses import JSONResponse

from app.models import (
    QueryRequest, QueryResponse, SchemaResponse, 
    ErrorResponse, HealthResponse
)
from app.database import db_manager
from app.llm import openrouter_client
from app.security import rate_limiter, input_validator

logger = logging.getLogger(__name__)

# Create API router
router = APIRouter()


def get_client_ip(request: Request) -> str:
    """Extract client IP address from request."""
    forwarded = request.headers.get("X-Forwarded-For")
    if forwarded:
        return forwarded.split(",")[0].strip()
    return request.client.host if request.client else "unknown"


def check_rate_limit(request: Request):
    """Dependency to check rate limiting."""
    client_ip = get_client_ip(request)
    if not rate_limiter.is_allowed(client_ip):
        raise HTTPException(
            status_code=429,
            detail="Too many requests. Please wait before trying again."
        )
    return client_ip


@router.post("/query", response_model=QueryResponse)
async def execute_query(
    query_request: QueryRequest,
    client_ip: str = Depends(check_rate_limit)
):
    """
    Execute a natural language query against the database.
    
    Args:
        query_request: Natural language query request
        client_ip: Client IP address (from dependency)
        
    Returns:
        Query results with generated SQL and metadata
        
    Raises:
        HTTPException: If query validation or execution fails
    """
    try:
        # Validate and sanitize input
        validation = input_validator.validate_natural_language_query(query_request.query)
        if not validation.is_valid:
            raise HTTPException(
                status_code=400,
                detail={
                    "error": "Query validation failed",
                    "details": validation.errors
                }
            )
        
        sanitized_query = validation.sanitized_input
        logger.info(f"Processing query from {client_ip}: {sanitized_query[:100]}...")
        
        # Test database connection
        if not await db_manager.test_connection():
            raise HTTPException(
                status_code=500,
                detail="Database connection failed"
            )
        
        # Get database schema
        schema = await db_manager.get_database_schema()
        if not schema:
            raise HTTPException(
                status_code=404,
                detail="No tables found in database"
            )
        
        # Generate SQL from natural language
        llm_response = await openrouter_client.generate_sql_from_natural_language(
            sanitized_query, schema
        )
        
        # Validate generated SQL
        sql_validation = input_validator.validate_sql_query(llm_response.sql)
        if not sql_validation.is_valid:
            raise HTTPException(
                status_code=400,
                detail={
                    "error": "Generated SQL failed security validation",
                    "details": sql_validation.errors
                }
            )
        
        # Execute the query
        results = await db_manager.execute_read_only_query(llm_response.sql)
        
        # Prepare response
        response_data = {
            "original_query": sanitized_query,
            "generated_sql": llm_response.sql,
            "explanation": llm_response.explanation,
            "confidence": llm_response.confidence,
            "results": results,
            "result_count": len(results),
            "warnings": validation.warnings + sql_validation.warnings
        }
        
        logger.info(f"Query executed successfully. Returned {len(results)} rows.")
        return QueryResponse(success=True, data=response_data)
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Query execution failed: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Internal server error: {str(e)}"
        )


@router.get("/schema", response_model=SchemaResponse)
async def get_database_schema():
    """
    Get database schema information.
    
    Returns:
        Database schema with tables and columns
        
    Raises:
        HTTPException: If schema retrieval fails
    """
    try:
        # Test database connection
        if not await db_manager.test_connection():
            raise HTTPException(
                status_code=500,
                detail="Database connection failed"
            )
        
        # Get schema
        schema = await db_manager.get_database_schema()
        
        response_data = {
            "tables": schema,
            "table_count": len(schema),
            "total_columns": sum(len(table["columns"]) for table in schema)
        }
        
        return SchemaResponse(success=True, data=response_data)
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Schema retrieval failed: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to retrieve database schema: {str(e)}"
        )


@router.get("/health", response_model=HealthResponse)
async def health_check():
    """
    Health check endpoint.
    
    Returns:
        System health status
    """
    try:
        # Check database connection
        db_status = "connected" if await db_manager.test_connection() else "disconnected"
        
        # Check OpenRouter (basic check - we can't easily test without making a request)
        openrouter_status = "available"  # Assume available unless we have evidence otherwise
        
        status = "healthy" if db_status == "connected" else "degraded"
        
        return HealthResponse(
            status=status,
            timestamp=datetime.utcnow().isoformat() + "Z",
            services={
                "database": db_status,
                "openrouter": openrouter_status
            }
        )
        
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        return HealthResponse(
            status="unhealthy",
            timestamp=datetime.utcnow().isoformat() + "Z",
            services={
                "database": "error",
                "openrouter": "unknown"
            }
        )


# Error handlers
@router.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    """Handle HTTP exceptions."""
    return JSONResponse(
        status_code=exc.status_code,
        content=ErrorResponse(
            error=exc.detail if isinstance(exc.detail, str) else exc.detail.get("error", "Unknown error"),
            details=exc.detail.get("details") if isinstance(exc.detail, dict) else None
        ).dict()
    )
