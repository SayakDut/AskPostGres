"""
OpenRouter LLM integration for natural language to SQL conversion.
Uses the exact Python client code as specified in requirements.
"""
import json
import logging
import re
from typing import Dict, Any, List, Optional
from dataclasses import dataclass

from openai import OpenAI

from src.config import get_settings

logger = logging.getLogger(__name__)
settings = get_settings()


@dataclass
class LLMResponse:
    """Response from LLM containing SQL query and metadata."""
    sql: str
    explanation: str
    confidence: float
    warnings: List[str] = None
    
    def __post_init__(self):
        if self.warnings is None:
            self.warnings = []


class OpenRouterClient:
    """Client for interacting with OpenRouter API using exact specified code."""
    
    def __init__(self):
        # Using the exact OpenRouter client code as specified
        self.client = OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=settings.openrouter_api_key,
        )
    
    def generate_sql_from_natural_language(
        self, 
        natural_language_query: str, 
        schema: List[Dict[str, Any]]
    ) -> LLMResponse:
        """
        Convert natural language query to SQL using OpenRouter API.
        Uses the exact client code format specified in requirements.
        
        Args:
            natural_language_query: User's natural language query
            schema: Database schema information
            
        Returns:
            LLMResponse containing SQL query and metadata
            
        Raises:
            Exception: If LLM request fails or response is invalid
        """
        schema_description = self._generate_schema_description(schema)
        prompt = self._create_prompt(natural_language_query, schema_description)
        
        try:
            # Using the exact OpenRouter API call format as specified
            completion = self.client.chat.completions.create(
                extra_headers={
                    "HTTP-Referer": settings.site_url,
                    "X-Title": settings.site_name,
                },
                extra_body={},
                model="meta-llama/llama-3.2-3b-instruct:free",
                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.1,  # Low temperature for consistent SQL generation
            )
            
            # Extract response using the exact format
            sql_query = completion.choices[0].message.content
            
            if not sql_query:
                raise Exception("Empty response from LLM")
            
            return self._parse_llm_response(sql_query)
            
        except Exception as e:
            logger.error(f"OpenRouter API call failed: {e}")
            error_msg = str(e)

            # Provide helpful error messages for common issues
            if "401" in error_msg or "Unauthenticated" in error_msg or "User not found" in error_msg:
                raise Exception(
                    "❌ Invalid OpenRouter API Key!\n\n"
                    "Please:\n"
                    "1. Visit https://openrouter.ai/\n"
                    "2. Sign up/Login to get a valid API key\n"
                    "3. Update your .env file with: OPENROUTER_API_KEY=your_new_key\n"
                    "4. Restart the application\n\n"
                    f"Current error: {error_msg}"
                )
            elif "402" in error_msg or "insufficient balance" in error_msg:
                raise Exception(
                    "💳 Insufficient OpenRouter Credits!\n\n"
                    "Your OpenRouter account is out of credits. Please:\n"
                    "1. Visit https://openrouter.ai/\n"
                    "2. Login to your account\n"
                    "3. Add credits to your account\n"
                    "4. Or switch to a free model\n\n"
                    "Note: I've updated the app to use a free model. Try restarting the application.\n\n"
                    f"Current error: {error_msg}"
                )
            elif "429" in error_msg or "Rate limit exceeded" in error_msg:
                raise Exception(
                    "⏱️ Rate Limit Exceeded!\n\n"
                    "The free model allows only 1 request per minute.\n\n"
                    "Please:\n"
                    "1. Wait 60 seconds before asking another question\n"
                    "2. Or upgrade to a paid model for higher limits\n"
                    "3. Visit https://openrouter.ai/ to add credits\n\n"
                    "The application is working fine - just wait a moment before your next query!\n\n"
                    f"Current error: {error_msg}"
                )
            else:
                raise Exception(f"Failed to generate SQL query: {error_msg}")
    
    def _generate_schema_description(self, schema: List[Dict[str, Any]]) -> str:
        """
        Generate a human-readable schema description for the LLM.
        
        Args:
            schema: Database schema information
            
        Returns:
            Formatted schema description
        """
        if not schema:
            return "No database schema available."
        
        description = "Database Schema:\n\n"
        
        for table in schema:
            description += f"Table: {table['table_name']}\n"
            description += "Columns:\n"
            
            for column in table['columns']:
                # Handle different column formats safely
                column_name = column.get('column_name', column.get('name', 'unknown'))
                data_type = column.get('data_type', column.get('type', 'unknown'))

                # Handle nullable field safely
                is_nullable = column.get('is_nullable', 'UNKNOWN')
                nullable = "nullable" if is_nullable == 'YES' else "not null" if is_nullable == 'NO' else ""

                # Handle max length safely
                max_length = ""
                if column.get('character_maximum_length'):
                    max_length = f" (max length: {column['character_maximum_length']})"

                # Build description
                nullable_text = f" ({nullable})" if nullable else ""
                description += f"  - {column_name}: {data_type}{max_length}{nullable_text}\n"
            
            description += "\n"
        
        return description
    
    def _create_prompt(self, query: str, schema_description: str) -> str:
        """
        Create the prompt for the LLM.
        
        Args:
            query: Natural language query
            schema_description: Database schema description
            
        Returns:
            Formatted prompt for the LLM
        """
        return f"""You are a PostgreSQL expert. Convert the following natural language query into a safe, read-only SQL query.

{schema_description}

IMPORTANT RULES:
1. Only generate SELECT queries - no INSERT, UPDATE, DELETE, DROP, or other destructive operations
2. Always include a LIMIT clause (default: 100 rows unless user specifies otherwise)
3. Use proper PostgreSQL syntax
4. Be case-sensitive with table and column names as shown in the schema
5. If the query is ambiguous, make reasonable assumptions
6. If the query cannot be safely converted, explain why

Natural Language Query: "{query}"

Respond with a JSON object in this exact format:
{{
  "sql": "SELECT ... FROM ... WHERE ... LIMIT 100",
  "explanation": "Brief explanation of what the query does",
  "confidence": 0.95
}}

The confidence should be a number between 0 and 1 indicating how confident you are in the query."""
    
    def _parse_llm_response(self, response: str) -> LLMResponse:
        """
        Parse the LLM response into structured data.
        
        Args:
            response: Raw response from LLM
            
        Returns:
            Parsed LLMResponse object
            
        Raises:
            Exception: If response cannot be parsed
        """
        warnings = []
        
        try:
            # Try to parse as JSON first
            parsed = json.loads(response)
            
            if not all(key in parsed for key in ['sql', 'explanation', 'confidence']):
                raise ValueError("Missing required fields in LLM response")
            
            return LLMResponse(
                sql=parsed['sql'],
                explanation=parsed['explanation'],
                confidence=float(parsed['confidence']),
                warnings=warnings
            )
            
        except json.JSONDecodeError:
            # Try to extract SQL from non-JSON response
            sql_match = re.search(r'SELECT[\s\S]*?(?=\n\n|\n$|$)', response, re.IGNORECASE)
            if sql_match:
                warnings.append("LLM response was not in JSON format, extracted SQL manually")
                return LLMResponse(
                    sql=sql_match.group(0).strip(),
                    explanation="Generated SQL query from natural language",
                    confidence=0.7,
                    warnings=warnings
                )
            
            # Try to find any SQL-like content
            lines = response.split('\n')
            for line in lines:
                if line.strip().lower().startswith('select'):
                    warnings.append("Extracted SQL from unstructured response")
                    return LLMResponse(
                        sql=line.strip(),
                        explanation="Generated SQL query from natural language",
                        confidence=0.6,
                        warnings=warnings
                    )
            
            raise Exception("Could not parse LLM response or extract SQL")
        
        except Exception as e:
            logger.error(f"Failed to parse LLM response: {e}")
            raise Exception(f"Invalid response format from LLM: {str(e)}")


# Global OpenRouter client instance
openrouter_client = OpenRouterClient()


def get_openrouter_client() -> OpenRouterClient:
    """Get the global OpenRouter client instance."""
    return openrouter_client
