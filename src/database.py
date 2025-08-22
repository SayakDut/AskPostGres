"""
Database connection and query execution utilities for PostgreSQL.
"""
import asyncio
import logging
from typing import List, Dict, Any, Optional, Tuple
from contextlib import asynccontextmanager
import pandas as pd

import asyncpg
import psycopg2
from psycopg2.extras import RealDictCursor
from sqlalchemy import create_engine, text
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker

from src.config import get_settings

logger = logging.getLogger(__name__)
settings = get_settings()


class DatabaseManager:
    """Manages database connections and query execution."""
    
    def __init__(self):
        self._async_pool: Optional[asyncpg.Pool] = None
        self._sync_engine = None
        self._async_engine = None
        self._initialized = False
    
    async def initialize_async(self):
        """Initialize async database connection pool."""
        if self._initialized:
            return
            
        try:
            self._async_pool = await asyncpg.create_pool(
                host=settings.postgres_host,
                port=settings.postgres_port,
                database=settings.postgres_db,
                user=settings.postgres_user,
                password=settings.postgres_password,
                min_size=5,
                max_size=20,
                command_timeout=30,
            )
            
            self._async_engine = create_async_engine(
                settings.database_url,
                echo=False,
                pool_size=10,
                max_overflow=20,
                pool_pre_ping=True,
                pool_recycle=3600,
            )
            
            self._initialized = True
            logger.info("Async database connection pool initialized")
        except Exception as e:
            logger.error(f"Failed to initialize async database pool: {e}")
            raise
    
    def initialize_sync(self):
        """Initialize synchronous database engine."""
        try:
            self._sync_engine = create_engine(
                settings.sync_database_url,
                echo=False,
                pool_size=10,
                max_overflow=20,
                pool_pre_ping=True,
                pool_recycle=3600,
            )
            logger.info("Sync database engine initialized")
        except Exception as e:
            logger.error(f"Failed to initialize sync database engine: {e}")
            raise
    
    async def close_async(self):
        """Close async database connection pool."""
        if self._async_pool:
            await self._async_pool.close()
            logger.info("Async database connection pool closed")
    
    def test_connection_sync(self) -> bool:
        """Test database connectivity synchronously."""
        try:
            if not self._sync_engine:
                self.initialize_sync()
            
            with self._sync_engine.connect() as conn:
                conn.execute(text("SELECT 1"))
            return True
        except Exception as e:
            logger.error(f"Sync database connection test failed: {e}")
            return False
    
    async def test_connection_async(self) -> bool:
        """Test database connectivity asynchronously."""
        try:
            if not self._initialized:
                await self.initialize_async()
            
            async with self._async_pool.acquire() as conn:
                await conn.fetchval("SELECT 1")
            return True
        except Exception as e:
            logger.error(f"Async database connection test failed: {e}")
            return False
    
    def execute_query_sync(self, query: str) -> pd.DataFrame:
        """
        Execute a query synchronously and return results as DataFrame.
        
        Args:
            query: SQL query string (must be SELECT only)
            
        Returns:
            pandas DataFrame with query results
            
        Raises:
            ValueError: If query is not read-only
            Exception: If query execution fails
        """
        if not self.is_read_only_query(query):
            raise ValueError("Only SELECT queries are allowed")
        
        # Add LIMIT if not present
        limited_query = self.add_limit_if_missing(query)
        
        try:
            if not self._sync_engine:
                self.initialize_sync()
            
            with self._sync_engine.connect() as conn:
                result = conn.execute(text(limited_query))
                columns = result.keys()
                rows = result.fetchall()
                
                # Convert to DataFrame
                df = pd.DataFrame(rows, columns=columns)
                return df
                
        except Exception as e:
            logger.error(f"Sync query execution failed: {e}")
            raise Exception(f"Database query failed: {str(e)}")
    
    async def execute_query_async(self, query: str) -> List[Dict[str, Any]]:
        """
        Execute a query asynchronously and return results as list of dicts.
        
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
            if not self._initialized:
                await self.initialize_async()
            
            async with self._async_pool.acquire() as conn:
                rows = await conn.fetch(limited_query)
                return [dict(row) for row in rows]
                
        except Exception as e:
            logger.error(f"Async query execution failed: {e}")
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
            'merge', 'upsert', 'replace', 'sp_', 'xp_'
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

        # Remove trailing semicolon if present
        clean_query = query.rstrip().rstrip(';')

        # Add LIMIT clause
        return f"{clean_query} LIMIT {default_limit}"
    
    def get_database_schema_sync(self) -> List[Dict[str, Any]]:
        """
        Get database schema information synchronously.
        
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
            df = self.execute_query_sync(schema_query)
            
            # Group columns by table
            tables = {}
            for _, row in df.iterrows():
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
