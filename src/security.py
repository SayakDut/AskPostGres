"""
Security utilities for input validation, sanitization, and rate limiting.
"""
import re
import time
import logging
import hashlib
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from collections import defaultdict
import streamlit as st

from src.config import get_settings

logger = logging.getLogger(__name__)
settings = get_settings()


@dataclass
class ValidationResult:
    """Result of input validation."""
    is_valid: bool
    errors: List[str]
    warnings: List[str]
    sanitized_input: Optional[str] = None


class RateLimiter:
    """Rate limiter for API requests using Streamlit session state."""

    def __init__(self, max_requests: int = None, window_seconds: int = 60):
        self.max_requests = max_requests or settings.max_requests_per_minute
        self.window_seconds = window_seconds

    def _ensure_session_state(self):
        """Ensure session state is initialized for rate limiting."""
        try:
            if 'rate_limit_requests' not in st.session_state:
                st.session_state.rate_limit_requests = defaultdict(list)
        except Exception:
            # If session state is not available, skip rate limiting
            pass
    
    def is_allowed(self, identifier: str = None) -> Tuple[bool, Optional[str]]:
        """
        Check if request is allowed based on rate limits.

        Args:
            identifier: Unique identifier (defaults to session-based)

        Returns:
            Tuple of (is_allowed, error_message)
        """
        try:
            self._ensure_session_state()

            if identifier is None:
                # Use session-based identifier for Streamlit
                identifier = self._get_session_identifier()

            now = time.time()
            window_start = now - self.window_seconds

            # Clean old requests
            st.session_state.rate_limit_requests[identifier] = [
                req_time for req_time in st.session_state.rate_limit_requests[identifier]
                if req_time > window_start
            ]

            # Check if under limit
            current_requests = len(st.session_state.rate_limit_requests[identifier])
            if current_requests >= self.max_requests:
                remaining_time = int(self.window_seconds - (now - min(st.session_state.rate_limit_requests[identifier])))
                return False, f"Rate limit exceeded. Try again in {remaining_time} seconds."

            # Add current request
            st.session_state.rate_limit_requests[identifier].append(now)
            return True, None

        except Exception:
            # If session state is not available, allow the request
            return True, None
    
    def _get_session_identifier(self) -> str:
        """Get a session-based identifier for rate limiting."""
        try:
            # Create a simple session identifier
            session_id = getattr(st.session_state, 'session_id', None)
            if session_id is None:
                # Generate a simple session ID based on current time and some randomness
                session_id = hashlib.md5(f"{time.time()}".encode()).hexdigest()[:16]
                st.session_state.session_id = session_id
            return session_id
        except Exception:
            # If session state is not available, return a default identifier
            return "default_session"


class InputValidator:
    """Validates and sanitizes user inputs."""
    
    # Dangerous SQL keywords and patterns
    DANGEROUS_KEYWORDS = [
        'insert', 'update', 'delete', 'drop', 'create', 'alter',
        'truncate', 'grant', 'revoke', 'commit', 'rollback',
        'begin', 'start transaction', 'set', 'call', 'exec',
        'merge', 'upsert', 'replace', 'sp_', 'xp_'
    ]
    
    DANGEROUS_PATTERNS = [
        r';\s*(drop|delete|update|insert|create|alter)',
        r'union\s+select',
        r'/\*.*\*/',  # Block comments
        r'--.*$',     # Line comments
        r"'[^']*'[^']*'",  # Potential string escape attempts
        r'\bxp_\w+',  # Extended stored procedures
        r'\bsp_\w+',  # System stored procedures
    ]
    
    @classmethod
    def validate_natural_language_query(cls, query: str) -> ValidationResult:
        """
        Validate and sanitize natural language query input.
        
        Args:
            query: User's natural language query
            
        Returns:
            ValidationResult with validation status and sanitized input
        """
        errors = []
        warnings = []
        
        # Basic validation
        if not query or not isinstance(query, str):
            errors.append("Query must be a non-empty string")
            return ValidationResult(False, errors, warnings)
        
        # Length validation
        if len(query) > 1000:
            errors.append("Query is too long (maximum 1000 characters)")
            return ValidationResult(False, errors, warnings)
        
        # Sanitize input
        sanitized = cls._sanitize_input(query)
        
        if not sanitized.strip():
            errors.append("Query contains no valid content after sanitization")
            return ValidationResult(False, errors, warnings)
        
        # Check for suspicious patterns (less strict for natural language)
        if cls._contains_suspicious_patterns(sanitized):
            warnings.append("Query contains patterns that might be interpreted as SQL")
        
        return ValidationResult(
            is_valid=len(errors) == 0,
            errors=errors,
            warnings=warnings,
            sanitized_input=sanitized
        )
    
    @classmethod
    def validate_sql_query(cls, query: str) -> ValidationResult:
        """
        Validate SQL query for security and safety.
        
        Args:
            query: SQL query string
            
        Returns:
            ValidationResult with validation status
        """
        errors = []
        warnings = []
        
        if not query or not isinstance(query, str):
            errors.append("SQL query cannot be empty")
            return ValidationResult(False, errors, warnings)
        
        normalized_query = query.lower().strip()
        
        # Must be SELECT query
        if not normalized_query.startswith('select'):
            errors.append("Only SELECT queries are allowed")
        
        # Check for dangerous keywords
        for keyword in cls.DANGEROUS_KEYWORDS:
            if keyword in normalized_query:
                errors.append(f"Dangerous keyword detected: {keyword.upper()}")
        
        # Check for dangerous patterns
        for pattern in cls.DANGEROUS_PATTERNS:
            if re.search(pattern, query, re.IGNORECASE):
                errors.append("Potentially dangerous SQL pattern detected")
        
        # Check for multiple statements
        if re.search(r';\s*\w', query):
            errors.append("Multiple SQL statements are not allowed")
        
        # Validate parentheses balance
        if query.count('(') != query.count(')'):
            errors.append("Unbalanced parentheses in query")
        
        # Check for LIMIT clause
        if 'limit' not in normalized_query:
            warnings.append("Query does not include LIMIT clause")
        
        return ValidationResult(
            is_valid=len(errors) == 0,
            errors=errors,
            warnings=warnings,
            sanitized_input=query if len(errors) == 0 else None
        )
    
    @classmethod
    def _sanitize_input(cls, input_str: str) -> str:
        """
        Sanitize user input by removing potentially dangerous characters.
        
        Args:
            input_str: Raw input string
            
        Returns:
            Sanitized input string
        """
        if not input_str:
            return ""
        
        # Remove null bytes and control characters
        sanitized = re.sub(r'[\x00-\x08\x0B\x0C\x0E-\x1F\x7F]', '', input_str)
        
        # Remove potential HTML/XML tags
        sanitized = re.sub(r'<[^>]*>', '', sanitized)
        
        # Limit length and strip whitespace
        return sanitized.strip()[:1000]
    
    @classmethod
    def _contains_suspicious_patterns(cls, text: str) -> bool:
        """
        Check if text contains suspicious SQL-like patterns.
        
        Args:
            text: Text to check
            
        Returns:
            True if suspicious patterns found
        """
        suspicious_patterns = [
            r'\bselect\b.*\bfrom\b',
            r'\binsert\b.*\binto\b',
            r'\bupdate\b.*\bset\b',
            r'\bdelete\b.*\bfrom\b',
            r'\bdrop\b.*\btable\b',
        ]
        
        for pattern in suspicious_patterns:
            if re.search(pattern, text, re.IGNORECASE):
                return True
        
        return False


class SecurityManager:
    """Central security manager for the application."""
    
    def __init__(self):
        self.rate_limiter = RateLimiter()
        self.input_validator = InputValidator()
    
    def check_request_allowed(self) -> Tuple[bool, Optional[str]]:
        """Check if the current request is allowed."""
        return self.rate_limiter.is_allowed()
    
    def validate_query_input(self, query: str) -> ValidationResult:
        """Validate natural language query input."""
        return self.input_validator.validate_natural_language_query(query)
    
    def validate_sql_query(self, query: str) -> ValidationResult:
        """Validate generated SQL query."""
        return self.input_validator.validate_sql_query(query)


# Global security manager instance
security_manager = SecurityManager()


def get_security_manager() -> SecurityManager:
    """Get the global security manager instance."""
    return security_manager
