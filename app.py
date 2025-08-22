"""
AskPostgres - Professional PostgreSQL Natural Language Query Interface

Query your PostgreSQL database using natural language powered by AI.
Built with Streamlit and OpenRouter API.
"""
import streamlit as st
import pandas as pd
import logging
import sys
from pathlib import Path
from typing import Optional, Dict, Any

# Add src to path for imports
sys.path.append(str(Path(__file__).parent / 'src'))

from src.config import get_settings
from src.database import db_manager
from src.llm import get_openrouter_client
from src.security import get_security_manager
from src.ui.components import UIComponents

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Get global instances
settings = get_settings()
security_manager = get_security_manager()
openrouter_client = get_openrouter_client()


class AskPostgresApp:
    """Main application class for AskPostgres."""
    
    def __init__(self):
        self.ui = UIComponents()
        self._initialize_session_state()
    
    def _initialize_session_state(self):
        """Initialize Streamlit session state variables."""
        if 'database_connected' not in st.session_state:
            st.session_state.database_connected = False
        
        if 'schema_info' not in st.session_state:
            st.session_state.schema_info = None
        
        if 'query_history' not in st.session_state:
            st.session_state.query_history = []
    
    def _validate_configuration(self) -> bool:
        """
        Validate application configuration.
        
        Returns:
            True if configuration is valid, False otherwise
        """
        errors = settings.validate_required_settings()
        if errors:
            st.error("❌ Configuration Error")
            st.write("Please check your .env file and ensure the following are set:")
            for error in errors:
                st.write(f"• {error}")
            
            st.info("💡 Copy .env.example to .env and fill in your configuration")
            return False
        
        return True
    
    def _test_database_connection(self) -> bool:
        """
        Test database connection and update session state.
        
        Returns:
            True if connection successful, False otherwise
        """
        try:
            # Test connection
            is_connected = db_manager.test_connection_sync()
            st.session_state.database_connected = is_connected
            
            if is_connected:
                # Get schema information
                try:
                    schema = db_manager.get_database_schema_sync()
                    st.session_state.schema_info = {
                        'tables': schema,
                        'table_count': len(schema),
                        'total_columns': sum(len(table['columns']) for table in schema)
                    }
                except Exception as e:
                    logger.warning(f"Could not retrieve schema: {e}")
                    st.session_state.schema_info = None
            
            return is_connected
            
        except Exception as e:
            logger.error(f"Database connection test failed: {e}")
            st.session_state.database_connected = False
            return False
    
    def _execute_query(self, query: str) -> Optional[Dict[str, Any]]:
        """
        Execute a natural language query.
        
        Args:
            query: Natural language query string
            
        Returns:
            Dictionary with query results or None if failed
        """
        try:
            # Check rate limiting
            is_allowed, error_msg = security_manager.check_request_allowed()
            if not is_allowed:
                self.ui.render_error_message("Rate Limit Exceeded", [error_msg])
                return None
            
            # Validate input
            validation = security_manager.validate_query_input(query)
            if not validation.is_valid:
                self.ui.render_error_message(
                    "Invalid Query Input",
                    validation.errors
                )
                return None
            
            # Show warnings if any
            if validation.warnings:
                self.ui.render_warning_message(
                    "Input Validation Warnings",
                    validation.warnings
                )
            
            # Get database schema
            if not st.session_state.schema_info:
                self.ui.render_error_message(
                    "Database Schema Not Available",
                    ["Please ensure database connection is working"]
                )
                return None
            
            # Generate SQL using LLM
            with st.spinner("🤖 Generating SQL query..."):
                llm_response = openrouter_client.generate_sql_from_natural_language(
                    validation.sanitized_input,
                    st.session_state.schema_info['tables']
                )
            
            # Validate generated SQL
            sql_validation = security_manager.validate_sql_query(llm_response.sql)
            if not sql_validation.is_valid:
                self.ui.render_error_message(
                    "Generated SQL Failed Security Validation",
                    sql_validation.errors
                )
                return None
            
            # Execute query
            with st.spinner("📊 Executing query..."):
                results_df = db_manager.execute_query_sync(llm_response.sql)
            
            # Prepare result data
            result_data = {
                'original_query': validation.sanitized_input,
                'generated_sql': llm_response.sql,
                'explanation': llm_response.explanation,
                'confidence': llm_response.confidence,
                'results_df': results_df,
                'warnings': validation.warnings + sql_validation.warnings + llm_response.warnings
            }
            
            # Add to query history
            st.session_state.query_history.append({
                'timestamp': pd.Timestamp.now(),
                'query': validation.sanitized_input,
                'sql': llm_response.sql,
                'row_count': len(results_df)
            })
            
            return result_data
            
        except Exception as e:
            logger.error(f"Query execution failed: {e}")
            self.ui.render_error_message(
                "Query Execution Failed",
                [str(e)]
            )
            return None
    
    def _render_query_history(self):
        """Render query history in sidebar."""
        if st.session_state.query_history:
            st.sidebar.markdown("### 📝 Query History")
            
            # Show last 5 queries
            recent_queries = st.session_state.query_history[-5:]
            for i, query_info in enumerate(reversed(recent_queries)):
                with st.sidebar.expander(f"Query {len(recent_queries) - i}"):
                    st.write(f"**Query:** {query_info['query'][:50]}...")
                    st.write(f"**Rows:** {query_info['row_count']}")
                    st.write(f"**Time:** {query_info['timestamp'].strftime('%H:%M:%S')}")
                    
                    if st.button(f"Rerun", key=f"rerun_{i}"):
                        st.session_state.query_input = query_info['query']
                        st.rerun()
    
    def run(self):
        """Run the main application."""
        # Render header
        self.ui.render_header()
        
        # Validate configuration
        if not self._validate_configuration():
            return
        
        # Test database connection
        db_connected = self._test_database_connection()
        
        # Render sidebar
        self.ui.render_sidebar()
        self._render_query_history()
        
        # Show database status
        self.ui.render_database_status(db_connected, st.session_state.schema_info)
        
        if not db_connected:
            st.stop()
        
        # Main query interface
        query = self.ui.render_query_input()
        
        if query:
            # Execute query
            result = self._execute_query(query)
            
            if result:
                # Render results
                self.ui.render_query_results(
                    results_df=result['results_df'],
                    original_query=result['original_query'],
                    generated_sql=result['generated_sql'],
                    explanation=result['explanation'],
                    confidence=result['confidence'],
                    warnings=result['warnings']
                )
        
        # Footer
        st.markdown("---")
        st.markdown("""
        <div style="text-align: center; color: #666;">
            <p>🐘💬 AskPostgres v1.0.0 | Built with Streamlit & FastAPI | 
            Powered by OpenRouter AI</p>
        </div>
        """, unsafe_allow_html=True)


def main():
    """Main entry point for the application."""
    try:
        app = AskPostgresApp()
        app.run()
    except Exception as e:
        logger.error(f"Application error: {e}")
        st.error(f"Application Error: {e}")
        st.info("Please check your configuration and try again.")


if __name__ == "__main__":
    main()
