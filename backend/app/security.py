"""
Security utilities for input validation, sanitization, and rate limiting.
"""
import re
import time
import logging
from typing import Dict, List, Optional
from dataclasses import dataclass
from collections import defaultdict

logger = logging.getLogger(__name__)


@dataclass
class ValidationResult:
    """Result of input validation."""
    is_valid: bool
    errors: List[str]
    warnings: List[str]
    sanitized_input: Optional[str] = None


class RateLimiter:
    """In-memory rate limiter for API requests."""
    
    def __init__(self, max_requests: int = 30, window_seconds: int = 60):
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        self.requests: Dict[str, List[float]] = defaultdict(list)
    
    def is_allowed(self, identifier: str) -> bool:
        """
        Check if request is allowed based on rate limits.
        
        Args:
            identifier: Unique identifier (e.g., IP address)
            
        Returns:
            True if request is allowed, False otherwise
        """
        now = time.time()
        window_start = now - self.window_seconds
        
        # Clean old requests
        self.requests[identifier] = [
            req_time for req_time in self.requests[identifier]
            if req_time > window_start
        ]
        
        # Check if under limit
        if len(self.requests[identifier]) >= self.max_requests:
            return False
        
        # Add current request
        self.requests[identifier].append(now)
        return True


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


# Global instances
rate_limiter = RateLimiter()
input_validator = InputValidator()
