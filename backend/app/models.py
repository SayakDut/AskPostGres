"""
Pydantic models for API request/response schemas.
"""
from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field, validator


class QueryRequest(BaseModel):
    """Request model for natural language query."""
    query: str = Field(..., min_length=1, max_length=1000, description="Natural language query")
    
    @validator('query')
    def validate_query(cls, v):
        if not v or not v.strip():
            raise ValueError('Query cannot be empty')
        return v.strip()


class ColumnInfo(BaseModel):
    """Database column information."""
    column_name: str
    data_type: str
    is_nullable: str
    column_default: Optional[str]
    character_maximum_length: Optional[int]


class TableInfo(BaseModel):
    """Database table information."""
    table_name: str
    columns: List[ColumnInfo]


class SchemaResponse(BaseModel):
    """Response model for database schema."""
    success: bool = True
    data: Dict[str, Any] = Field(default_factory=dict)
    
    class Config:
        schema_extra = {
            "example": {
                "success": True,
                "data": {
                    "tables": [
                        {
                            "table_name": "users",
                            "columns": [
                                {
                                    "column_name": "id",
                                    "data_type": "integer",
                                    "is_nullable": "NO",
                                    "column_default": "nextval('users_id_seq'::regclass)",
                                    "character_maximum_length": None
                                }
                            ]
                        }
                    ],
                    "table_count": 1,
                    "total_columns": 1
                }
            }
        }


class QueryResponse(BaseModel):
    """Response model for query execution."""
    success: bool = True
    data: Optional[Dict[str, Any]] = None
    
    class Config:
        schema_extra = {
            "example": {
                "success": True,
                "data": {
                    "original_query": "Show me all users",
                    "generated_sql": "SELECT * FROM users LIMIT 100",
                    "explanation": "This query retrieves all users from the users table",
                    "confidence": 0.95,
                    "results": [
                        {"id": 1, "name": "John Doe", "email": "john@example.com"}
                    ],
                    "result_count": 1,
                    "warnings": []
                }
            }
        }


class ErrorResponse(BaseModel):
    """Response model for errors."""
    success: bool = False
    error: str
    details: Optional[List[str]] = None
    
    class Config:
        schema_extra = {
            "example": {
                "success": False,
                "error": "Query validation failed",
                "details": ["Only SELECT queries are allowed"]
            }
        }


class HealthResponse(BaseModel):
    """Response model for health check."""
    status: str
    timestamp: str
    services: Dict[str, str]
    
    class Config:
        schema_extra = {
            "example": {
                "status": "healthy",
                "timestamp": "2023-12-01T12:00:00Z",
                "services": {
                    "database": "connected",
                    "openrouter": "available"
                }
            }
        }
