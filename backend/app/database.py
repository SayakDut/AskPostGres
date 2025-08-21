"""
Database connection and query execution utilities for PostgreSQL.
"""
import asyncio
import logging
from typing import List, Dict, Any, Optional
from contextlib import asynccontextmanager

import asyncpg
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import declarative_base
from sqlalchemy import text

from app.config import settings

logger = logging.getLogger(__name__)

# SQLAlchemy setup
engine = create_async_engine(
    settings.database_url,
    echo=False,
    pool_size=10,
    max_overflow=20,
    pool_pre_ping=True,
    pool_recycle=3600,
)

AsyncSessionLocal = async_sessionmaker(
    engine, 
    class_=AsyncSession, 
    expire_on_commit=False
)

Base = declarative_base()


class DatabaseManager:
    """Manages database connections and query execution."""
    
    def __init__(self):
        self._pool: Optional[asyncpg.Pool] = None
    
    async def initialize(self):
        """Initialize database connection pool."""
        try:
            self._pool = await asyncpg.create_pool(
                host=settings.postgres_host,
                port=settings.postgres_port,
                database=settings.postgres_db,
                user=settings.postgres_user,
                password=settings.postgres_password,
                min_size=5,
                max_size=20,
                command_timeout=30,
            )
            logger.info("Database connection pool initialized")
        except Exception as e:
            logger.error(f"Failed to initialize database pool: {e}")
            raise
    
    async def close(self):
        """Close database connection pool."""
        if self._pool:
            await self._pool.close()
            logger.info("Database connection pool closed")
    
    async def test_connection(self) -> bool:
        """Test database connectivity."""
        try:
            if not self._pool:
                await self.initialize()
            
            async with self._pool.acquire() as conn:
                await conn.fetchval("SELECT 1")
            return True
        except Exception as e:
            logger.error(f"Database connection test failed: {e}")
            return False
    
    async def execute_read_only_query(self, query: str) -> List[Dict[str, Any]]:
        """
        Execute a read-only SQL query safely.
        
        Args:
            query: SQL query string (must be SELECT only)
            
        Returns:
            List of dictionaries representing query results
            
        Raises:
            ValueError: If query is not read-only
            Exception: If query execution fails
        """
        if not self.is_read_only_query(query):
            raise ValueError("Only SELECT queries are allowed")
        
        # Add LIMIT if not present
        limited_query = self.add_limit_if_missing(query)
        
        try:
            if not self._pool:
                await self.initialize()
            
            async with self._pool.acquire() as conn:
                rows = await conn.fetch(limited_query)
                return [dict(row) for row in rows]
                
        except Exception as e:
            logger.error(f"Query execution failed: {e}")
            raise Exception(f"Database query failed: {str(e)}")
    
    @staticmethod
    def is_read_only_query(query: str) -> bool:
        """
        Validate that a query is read-only (SELECT only).
        
        Args:
            query: SQL query string
            
        Returns:
            True if query is read-only, False otherwise
        """
        normalized_query = query.strip().lower()
        
        # Check for dangerous keywords
        dangerous_keywords = [
            'insert', 'update', 'delete', 'drop', 'create', 'alter',
            'truncate', 'grant', 'revoke', 'commit', 'rollback',
            'begin', 'start transaction', 'set', 'call', 'exec',
            'merge', 'upsert', 'replace'
        ]
        
        for keyword in dangerous_keywords:
            if keyword in normalized_query:
                return False
        
        # Must start with SELECT
        return normalized_query.startswith('select')
    
    @staticmethod
    def add_limit_if_missing(query: str, default_limit: int = 100) -> str:
        """
        Add LIMIT clause if missing from query.
        
        Args:
            query: SQL query string
            default_limit: Default limit to apply
            
        Returns:
            Query with LIMIT clause
        """
        normalized_query = query.strip().lower()
        
        if 'limit' in normalized_query:
            return query
        
        # Handle ORDER BY clause
        if 'order by' in normalized_query:
            return f"{query.rstrip()} LIMIT {default_limit}"
        
        return f"{query.rstrip()} LIMIT {default_limit}"
    
    async def get_database_schema(self) -> List[Dict[str, Any]]:
        """
        Get database schema information (tables and columns).
        
        Returns:
            List of table information with columns
        """
        schema_query = """
        SELECT 
            t.table_name,
            c.column_name,
            c.data_type,
            c.is_nullable,
            c.column_default,
            c.character_maximum_length
        FROM information_schema.tables t
        JOIN information_schema.columns c ON t.table_name = c.table_name
        WHERE t.table_schema = 'public' 
        AND t.table_type = 'BASE TABLE'
        ORDER BY t.table_name, c.ordinal_position
        """
        
        try:
            if not self._pool:
                await self.initialize()
            
            async with self._pool.acquire() as conn:
                rows = await conn.fetch(schema_query)
                
                # Group columns by table
                tables = {}
                for row in rows:
                    table_name = row['table_name']
                    if table_name not in tables:
                        tables[table_name] = {
                            'table_name': table_name,
                            'columns': []
                        }
                    
                    tables[table_name]['columns'].append({
                        'column_name': row['column_name'],
                        'data_type': row['data_type'],
                        'is_nullable': row['is_nullable'],
                        'column_default': row['column_default'],
                        'character_maximum_length': row['character_maximum_length']
                    })
                
                return list(tables.values())
                
        except Exception as e:
            logger.error(f"Schema retrieval failed: {e}")
            raise Exception(f"Failed to retrieve database schema: {str(e)}")


# Global database manager instance
db_manager = DatabaseManager()
