"""
UI components for the Streamlit frontend.
"""
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from typing import List, Dict, Any, Optional
import time
import io

from src.config import get_settings

settings = get_settings()


class UIComponents:
    """Collection of reusable UI components."""
    
    @staticmethod
    def render_header():
        """Render the application header."""
        st.set_page_config(
            page_title="AskPostgres",
            page_icon="🐘",
            layout="wide",
            initial_sidebar_state="expanded"
        )

        # Get theme from session state
        theme = st.session_state.get('theme', 'Light')
        is_dark = theme == 'Dark'

        # Dynamic CSS based on theme
        css = f"""
        <style>
        /* Main theme variables */
        :root {{
            --bg-primary: {'#0E1117' if is_dark else '#FFFFFF'};
            --bg-secondary: {'#1E1E1E' if is_dark else '#F8FAFC'};
            --text-primary: {'#FFFFFF' if is_dark else '#1F2937'};
            --text-secondary: {'#CCCCCC' if is_dark else '#6B7280'};
            --border-color: {'#404040' if is_dark else '#E5E7EB'};
            --accent-color: {'#60A5FA' if is_dark else '#3B82F6'};
        }}

        /* Override Streamlit's default styling */
        .stApp {{
            background-color: var(--bg-primary) !important;
            color: var(--text-primary) !important;
        }}

        /* Fix the white header area */
        .main .block-container {{
            background-color: var(--bg-primary) !important;
            color: var(--text-primary) !important;
        }}

        /* Fix Streamlit's top header */
        header[data-testid="stHeader"] {{
            background-color: var(--bg-primary) !important;
            height: 0px !important;
        }}

        /* Fix the main content area */
        .main {{
            background-color: var(--bg-primary) !important;
        }}

        /* Fix any remaining white backgrounds */
        div[data-testid="stAppViewContainer"] {{
            background-color: var(--bg-primary) !important;
        }}

        section[data-testid="stSidebar"] {{
            background-color: var(--bg-secondary) !important;
        }}

        .main-header {{
            background: linear-gradient(90deg, {'#1E3A8A' if is_dark else '#3B82F6'} 0%, {'#1E40AF' if is_dark else '#1E40AF'} 100%);
            padding: 1rem;
            border-radius: 10px;
            margin-bottom: 2rem;
            color: white;
        }}

        .metric-card {{
            background: var(--bg-secondary);
            padding: 1rem;
            border-radius: 8px;
            border: 1px solid var(--border-color);
            box-shadow: 0 1px 3px rgba(0, 0, 0, {'0.3' if is_dark else '0.1'});
            color: var(--text-primary);
        }}

        .query-box {{
            border: 2px solid var(--accent-color);
            border-radius: 8px;
            padding: 1rem;
            background: var(--bg-secondary);
            color: var(--text-primary);
        }}

        .success-box {{
            border: 2px solid {'#059669' if is_dark else '#10B981'};
            border-radius: 8px;
            padding: 1rem;
            background: {'#064E3B' if is_dark else '#ECFDF5'};
            color: var(--text-primary);
        }}

        .error-box {{
            border: 2px solid {'#DC2626' if is_dark else '#EF4444'};
            border-radius: 8px;
            padding: 1rem;
            background: {'#7F1D1D' if is_dark else '#FEF2F2'};
            color: var(--text-primary);
        }}

        .warning-box {{
            border: 2px solid {'#D97706' if is_dark else '#F59E0B'};
            border-radius: 8px;
            padding: 1rem;
            background: {'#92400E' if is_dark else '#FFFBEB'};
            color: var(--text-primary);
        }}

        /* Left align all table columns - applies to both themes */
        .stDataFrame table th,
        .stDataFrame table td,
        div[data-testid="stDataFrame"] table th,
        div[data-testid="stDataFrame"] table td,
        .dataframe th,
        .dataframe td {{
            text-align: left !important;
        }}

        /* Dark theme specific overrides */
        {'/* Dark theme styles */' if is_dark else ''}
        {'''
        /* Text and input styling */
        .stSelectbox > div > div {
            background-color: var(--bg-secondary) !important;
            color: var(--text-primary) !important;
            border-color: var(--border-color) !important;
        }

        .stTextArea > div > div > textarea {
            background-color: var(--bg-secondary) !important;
            color: var(--text-primary) !important;
            border-color: var(--border-color) !important;
        }

        .stTextInput > div > div > input {
            background-color: var(--bg-secondary) !important;
            color: var(--text-primary) !important;
            border-color: var(--border-color) !important;
        }

        .stButton > button {
            background-color: var(--accent-color) !important;
            color: white !important;
            border: none !important;
        }

        .stSidebar {
            background-color: var(--bg-secondary) !important;
        }

        .stMarkdown {
            color: var(--text-primary) !important;
        }

        /* Fix metric cards */
        div[data-testid="metric-container"] {
            background-color: var(--bg-secondary) !important;
            color: var(--text-primary) !important;
            border: 1px solid var(--border-color) !important;
        }

        /* Fix success/error messages */
        .stSuccess {
            background-color: #064E3B !important;
            color: #FFFFFF !important;
        }

        .stError {
            background-color: #7F1D1D !important;
            color: #FFFFFF !important;
        }

        .stWarning {
            background-color: #92400E !important;
            color: #FFFFFF !important;
        }

        .stInfo {
            background-color: #1E3A8A !important;
            color: #FFFFFF !important;
        }

        /* Fix expander */
        .streamlit-expanderHeader {
            background-color: var(--bg-secondary) !important;
            color: var(--text-primary) !important;
        }

        .streamlit-expanderContent {
            background-color: var(--bg-secondary) !important;
            color: var(--text-primary) !important;
        }

        /* Fix dataframe */
        .stDataFrame {
            background-color: var(--bg-secondary) !important;
            color: var(--text-primary) !important;
        }

        /* Left align all dataframe columns */
        .stDataFrame table th,
        .stDataFrame table td {
            text-align: left !important;
        }

        /* Also target the specific dataframe elements */
        div[data-testid="stDataFrame"] table th,
        div[data-testid="stDataFrame"] table td {
            text-align: left !important;
        }

        /* Target any table cells in the app */
        .dataframe th,
        .dataframe td {
            text-align: left !important;
        }

        /* Fix plotly charts background */
        .js-plotly-plot {
            background-color: var(--bg-secondary) !important;
        }

        /* Fix any remaining text visibility issues */
        p, span, div, label {
            color: var(--text-primary) !important;
        }

        /* Fix sidebar text */
        .sidebar .stMarkdown {
            color: var(--text-primary) !important;
        }
        ''' if is_dark else ''}
        </style>
        """

        st.markdown(css, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="main-header">
            <h1>🐘💬 AskPostgres</h1>
            <p>Query your PostgreSQL database using natural language powered by AI</p>
        </div>
        """, unsafe_allow_html=True)
    
    @staticmethod
    def render_sidebar():
        """Render the sidebar with application info and settings."""
        with st.sidebar:
            st.markdown("### 📊 Application Info")
            st.info(f"**Version:** 1.0.0\n**Framework:** Streamlit + FastAPI\n**AI Model:** GPT-OSS-20B")
            
            st.markdown("### 🔧 Settings")
            
            # Theme selector
            current_theme = st.session_state.get('theme', 'Light')
            theme = st.selectbox(
                "Theme",
                ["Light", "Dark"],
                index=0 if current_theme == "Light" else 1,
                key="theme_selector"
            )

            # Update theme in session state and trigger rerun if changed
            if theme != st.session_state.get('theme', 'Light'):
                st.session_state.theme = theme
                st.rerun()
            
            # Query settings
            st.markdown("### ⚙️ Query Settings")
            default_limit = st.number_input(
                "Default LIMIT",
                min_value=10,
                max_value=1000,
                value=100,
                step=10,
                help="Default number of rows to return"
            )
            
            # Store in session state
            st.session_state.default_limit = default_limit
            
            st.markdown("### 📚 Example Queries")
            examples = [
                "Show me all users who registered this month",
                "What are the top 10 best-selling products?",
                "Find customers with orders over $1000",
                "Show me the average order value by month",
                "List all products that are out of stock"
            ]
            
            for i, example in enumerate(examples):
                if st.button(f"📝 {example[:30]}...", key=f"example_{i}"):
                    st.session_state.query_input = example
                    st.rerun()
    
    @staticmethod
    def render_query_input() -> Optional[str]:
        """
        Render the query input section.
        
        Returns:
            The submitted query string or None
        """
        st.markdown("### 🔍 Ask Your Question")
        
        # Initialize session state
        if 'query_input' not in st.session_state:
            st.session_state.query_input = ""
        
        # Query input
        query = st.text_area(
            "Enter your question in plain English:",
            value=st.session_state.query_input,
            height=100,
            placeholder="e.g., Show me all users who signed up last week",
            help="Ask questions about your data in natural language"
        )
        
        col1, col2, col3 = st.columns([1, 1, 2])
        
        with col1:
            submit_button = st.button("🚀 Execute Query", type="primary")
        
        with col2:
            clear_button = st.button("🗑️ Clear")
        
        if clear_button:
            st.session_state.query_input = ""
            st.rerun()
        
        if submit_button and query.strip():
            return query.strip()
        
        return None
    
    @staticmethod
    def render_loading_spinner(message: str = "Processing your query..."):
        """Render a loading spinner with message."""
        with st.spinner(message):
            # Add a progress bar for better UX
            progress_bar = st.progress(0)
            for i in range(100):
                time.sleep(0.01)
                progress_bar.progress(i + 1)
            progress_bar.empty()
    
    @staticmethod
    def render_error_message(error: str, details: List[str] = None):
        """Render an error message with optional details."""
        st.markdown(f"""
        <div class="error-box">
            <h4>❌ Error</h4>
            <p>{error}</p>
        </div>
        """, unsafe_allow_html=True)
        
        if details:
            with st.expander("🔍 Error Details"):
                for detail in details:
                    st.write(f"• {detail}")
    
    @staticmethod
    def render_warning_message(warning: str, details: List[str] = None):
        """Render a warning message with optional details."""
        st.markdown(f"""
        <div class="warning-box">
            <h4>⚠️ Warning</h4>
            <p>{warning}</p>
        </div>
        """, unsafe_allow_html=True)
        
        if details:
            with st.expander("🔍 Warning Details"):
                for detail in details:
                    st.write(f"• {detail}")
    
    @staticmethod
    def render_success_message(message: str, details: str = None):
        """Render a success message with optional details."""
        st.markdown(f"""
        <div class="success-box">
            <h4>✅ Success</h4>
            <p>{message}</p>
        </div>
        """, unsafe_allow_html=True)
        
        if details:
            st.write(details)
    
    @staticmethod
    def render_query_results(
        results_df: pd.DataFrame,
        original_query: str,
        generated_sql: str,
        explanation: str,
        confidence: float,
        warnings: List[str] = None
    ):
        """
        Render query results with metadata.
        
        Args:
            results_df: DataFrame with query results
            original_query: Original natural language query
            generated_sql: Generated SQL query
            explanation: LLM explanation
            confidence: Confidence score
            warnings: List of warnings
        """
        # Results summary
        st.markdown("### 📊 Query Results")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Rows Returned", len(results_df))
        
        with col2:
            st.metric("Columns", len(results_df.columns))
        
        with col3:
            st.metric("Confidence", f"{confidence:.1%}")
        
        with col4:
            # Export button
            csv_buffer = io.StringIO()
            results_df.to_csv(csv_buffer, index=False)
            st.download_button(
                "📥 Export CSV",
                csv_buffer.getvalue(),
                file_name="query_results.csv",
                mime="text/csv"
            )
        
        # Show warnings if any
        if warnings:
            UIComponents.render_warning_message(
                "Query executed with warnings",
                warnings
            )
        
        # Query metadata
        with st.expander("🔍 Query Details", expanded=False):
            st.markdown("**Original Query:**")
            st.code(original_query, language="text")
            
            st.markdown("**Generated SQL:**")
            st.code(generated_sql, language="sql")
            
            st.markdown("**Explanation:**")
            st.write(explanation)
        
        # Results table
        if not results_df.empty:
            st.markdown("**Results:**")
            st.dataframe(
                results_df,
                use_container_width=True,
                height=400
            )
            
            # Basic visualization if numeric columns exist
            numeric_columns = results_df.select_dtypes(include=['number']).columns
            if len(numeric_columns) > 0:
                with st.expander("📈 Quick Visualization", expanded=False):
                    viz_type = st.selectbox(
                        "Visualization Type",
                        ["Bar Chart", "Line Chart", "Histogram", "Box Plot"]
                    )
                    
                    if len(numeric_columns) >= 1:
                        y_column = st.selectbox("Y-axis", numeric_columns)
                        
                        if viz_type == "Bar Chart" and len(results_df.columns) > 1:
                            x_column = st.selectbox(
                                "X-axis", 
                                [col for col in results_df.columns if col != y_column]
                            )
                            fig = px.bar(results_df.head(20), x=x_column, y=y_column)
                            st.plotly_chart(fig, use_container_width=True)
                        
                        elif viz_type == "Line Chart" and len(results_df.columns) > 1:
                            x_column = st.selectbox(
                                "X-axis", 
                                [col for col in results_df.columns if col != y_column]
                            )
                            fig = px.line(results_df.head(50), x=x_column, y=y_column)
                            st.plotly_chart(fig, use_container_width=True)
                        
                        elif viz_type == "Histogram":
                            fig = px.histogram(results_df, x=y_column)
                            st.plotly_chart(fig, use_container_width=True)
                        
                        elif viz_type == "Box Plot":
                            fig = px.box(results_df, y=y_column)
                            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No results returned for this query.")
    
    @staticmethod
    def render_database_status(is_connected: bool, schema_info: Dict[str, Any] = None):
        """Render database connection status."""
        if is_connected:
            st.success("🟢 Database Connected")
            if schema_info:
                col1, col2 = st.columns(2)
                with col1:
                    st.metric("Tables", schema_info.get('table_count', 0))
                with col2:
                    st.metric("Total Columns", schema_info.get('total_columns', 0))
        else:
            st.error("🔴 Database Disconnected")
            st.warning("Please check your database configuration in the .env file")
