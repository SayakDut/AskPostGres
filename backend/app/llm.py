"""
OpenRouter LLM integration for natural language to SQL conversion.
"""
import logging
from typing import Dict, Any, List
from dataclasses import dataclass

from openai import OpenAI

from app.config import settings

logger = logging.getLogger(__name__)


@dataclass
class LLMResponse:
    """Response from LLM containing SQL query and metadata."""
    sql: str
    explanation: str
    confidence: float


class OpenRouterClient:
    """Client for interacting with OpenRouter API."""
    
    def __init__(self):
        self.client = OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=settings.openrouter_api_key,
        )
    
    async def generate_sql_from_natural_language(
        self, 
        natural_language_query: str, 
        schema: List[Dict[str, Any]]
    ) -> LLMResponse:
        """
        Convert natural language query to SQL using OpenRouter API.
        
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
            completion = self.client.chat.completions.create(
                extra_headers={
                    "HTTP-Referer": settings.site_url,
                    "X-Title": settings.site_name,
                },
                extra_body={},
                model="openai/gpt-oss-20b:free",
                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.1,  # Low temperature for consistent SQL generation
            )
            
            response_content = completion.choices[0].message.content
            if not response_content:
                raise Exception("Empty response from LLM")
            
            return self._parse_llm_response(response_content)
            
        except Exception as e:
            logger.error(f"OpenRouter API call failed: {e}")
            raise Exception(f"Failed to generate SQL query: {str(e)}")
    
    def _generate_schema_description(self, schema: List[Dict[str, Any]]) -> str:
        """
        Generate a human-readable schema description for the LLM.
        
        Args:
            schema: Database schema information
            
        Returns:
            Formatted schema description
        """
        description = "Database Schema:\n\n"
        
        for table in schema:
            description += f"Table: {table['table_name']}\n"
            description += "Columns:\n"
            
            for column in table['columns']:
                nullable = "nullable" if column['is_nullable'] == 'YES' else "not null"
                max_length = f" (max length: {column['character_maximum_length']})" \
                    if column['character_maximum_length'] else ""
                
                description += f"  - {column['column_name']}: {column['data_type']}{max_length} ({nullable})\n"
            
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
        try:
            import json
            parsed = json.loads(response)
            
            if not all(key in parsed for key in ['sql', 'explanation', 'confidence']):
                raise ValueError("Missing required fields in LLM response")
            
            return LLMResponse(
                sql=parsed['sql'],
                explanation=parsed['explanation'],
                confidence=float(parsed['confidence'])
            )
            
        except json.JSONDecodeError:
            # Try to extract SQL from non-JSON response
            import re
            sql_match = re.search(r'SELECT[\s\S]*?(?=\n\n|\n$|$)', response, re.IGNORECASE)
            if sql_match:
                return LLMResponse(
                    sql=sql_match.group(0).strip(),
                    explanation="Generated SQL query from natural language",
                    confidence=0.7
                )
            
            raise Exception("Could not parse LLM response")
        
        except Exception as e:
            logger.error(f"Failed to parse LLM response: {e}")
            raise Exception(f"Invalid response format from LLM: {str(e)}")


# Global OpenRouter client instance
openrouter_client = OpenRouterClient()
