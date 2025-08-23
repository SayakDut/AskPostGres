# 🐘 AskPostgres

<div align="center">

![AskPostgres Logo](https://img.shields.io/badge/AskPostgres-AI%20Database%20Assistant-blue?style=for-the-badge&logo=postgresql&logoColor=white)

**Query your PostgreSQL database using natural language powered by AI**

[![Python](https://img.shields.io/badge/Python-3.8+-blue?style=flat-square&logo=python)](https://python.org)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.28+-red?style=flat-square&logo=streamlit)](https://streamlit.io)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-13+-blue?style=flat-square&logo=postgresql)](https://postgresql.org)
[![OpenRouter](https://img.shields.io/badge/OpenRouter-AI%20API-green?style=flat-square)](https://openrouter.ai)

[🚀 Quick Start](#-quick-start) • [✨ Features](#-features) • [🎯 Examples](#-example-queries) • [🤝 Contributing](#-contributing)

</div>

---

## 🌟 Overview

AskPostgres is a sophisticated AI-powered database assistant that transforms natural language questions into SQL queries. Built with modern technologies and featuring both light and dark themes, it provides an intuitive interface for database exploration and analysis.

## ✨ Features

### 🎯 **Core Capabilities**
- **Natural Language Processing**: Convert plain English to SQL queries
- **Real-time Query Execution**: Instant results with performance metrics
- **Smart Schema Analysis**: Automatic database structure understanding
- **Export Functionality**: Download results in multiple formats (CSV, JSON, Excel)
- **Query History**: Track and revisit previous queries

### 🎨 **User Experience**
- **Dual Theme Support**: Professional light and dark modes
- **Responsive Design**: Works seamlessly across devices
- **Interactive Results**: Sortable and filterable data tables
- **Performance Metrics**: Query execution time and confidence scores
- **Error Handling**: Intelligent error messages and suggestions

### 🔧 **Technical Features**
- **Multiple AI Models**: Support for various LLM providers via OpenRouter
- **Connection Pooling**: Efficient database connection management
- **Rate Limiting**: Built-in API usage optimization
- **Secure Configuration**: Environment-based secrets management
- **Comprehensive Logging**: Detailed application monitoring

## 📸 Screenshots

### 🌙 Dark Theme Interface

**Query Interface with Results**
![Dark Theme - Query Results]([https://github.com/user-attachments/assets/dark-theme-query-results.png](https://github.com/SayakDut/AskPostGres/blob/0d5c452c958e8ea63acfe45db452457377a7db38/screenshots/5.png))

**Database Overview Dashboard**
![Dark Theme - Database Overview]([https://github.com/user-attachments/assets/dark-theme-overview.png](https://github.com/SayakDut/AskPostGres/blob/0d5c452c958e8ea63acfe45db452457377a7db38/screenshots/4.png))

### ☀️ Light Theme Interface

**Clean Query Results Display**
![Light Theme - Query Results]([https://github.com/user-attachments/assets/light-theme-results.png](https://github.com/SayakDut/AskPostGres/blob/0d5c452c958e8ea63acfe45db452457377a7db38/screenshots/3.png))

**Intuitive Query Input**
![Light Theme - Query Input]([https://github.com/user-attachments/assets/light-theme-input.png](https://github.com/SayakDut/AskPostGres/blob/0d5c452c958e8ea63acfe45db452457377a7db38/screenshots/1.png))

**Advanced Features & Export**
![Light Theme - Advanced Features]([https://github.com/user-attachments/assets/light-theme-advanced.png](https://github.com/SayakDut/AskPostGres/blob/0d5c452c958e8ea63acfe45db452457377a7db38/screenshots/2.png))


## 🚀 Quick Start

### Prerequisites
- **Python 3.8+**
- **PostgreSQL database** (local or remote)
- **OpenRouter API key** ([Get free key](https://openrouter.ai/))

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/AskPostgres.git
   cd AskPostgres
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment**
   ```bash
   # Edit .env with your database and API credentials
   # The file is already included with placeholder values
   ```

5. **Run the application**
   ```bash
   streamlit run app.py
   ```

6. **Open your browser**
   Navigate to `http://localhost:8501`

## ⚙️ Configuration

### Environment Variables

Edit the included `.env` file with your actual values:

```env
# Database Configuration
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
POSTGRES_DB=your_database
POSTGRES_USER=your_username
POSTGRES_PASSWORD=your_password

# AI Configuration
OPENROUTER_API_KEY=your_api_key_here

# Application Settings
SITE_URL=http://localhost:8501
STREAMLIT_THEME=light
MAX_REQUESTS_PER_MINUTE=30
```

### Database Setup

Ensure your PostgreSQL database is accessible and contains the tables you want to query. The application will automatically analyze your schema and provide intelligent suggestions.

## 🎯 Example Queries

### 📊 Business Analytics
- *"Show me the top 5 customers by revenue this year"*
- *"What are the monthly sales trends for the last 6 months?"*
- *"Find products with low inventory levels"*

### 🔍 Data Exploration
- *"List all tables in the database"*
- *"Show me the structure of the users table"*
- *"Find duplicate records in the orders table"*

### ⚡ Performance Analysis
- *"Which queries are taking the longest to execute?"*
- *"Show database size and table statistics"*
- *"Find unused indexes in the database"*

## 🏗️ Architecture

```
AskPostgres/
├── src/
│   ├── database.py          # Database connection and operations
│   ├── llm.py              # AI model integration
│   ├── security.py         # Security and validation
│   ├── config.py           # Configuration management
│   └── ui/
│       └── components.py   # Streamlit interface components
├── app.py                 # Main application entry point
├── requirements.txt        # Python dependencies
├── .env                   # Environment configuration (edit with your values)
├── CONTRIBUTING.md        # Contribution guidelines
└── README.md              # This file
```

## 🔒 Security

- **🛡️ Environment Variables**: Sensitive data stored securely
- **🔑 API Key Management**: Secure OpenRouter integration
- **💉 SQL Injection Protection**: Parameterized queries and validation
- **⏱️ Rate Limiting**: Built-in request throttling
- **🚫 Read-Only Queries**: Only SELECT statements allowed
- **🧹 Error Sanitization**: Safe error message handling

## 🛠️ Development

### Local Development Setup

1. **Fork the repository**
2. **Create a feature branch**: `git checkout -b feature-name`
3. **Make your changes** and add tests
4. **Run the test suite**: `pytest`
5. **Submit a pull request**

### Key Components

- **`src/database.py`**: PostgreSQL connection and query execution
- **`src/llm.py`**: OpenRouter API integration and prompt engineering
- **`src/security.py`**: Input validation and SQL injection prevention
- **`src/ui/components.py`**: Streamlit UI components and theming

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guidelines](CONTRIBUTING.md) for details.

### Ways to Contribute
- 🐛 **Bug Reports**: Found an issue? Let us know!
- 💡 **Feature Requests**: Have an idea? We'd love to hear it!
- 📝 **Documentation**: Help improve our docs
- 🧪 **Testing**: Add tests for better coverage
- 🎨 **UI/UX**: Enhance the user interface



## 🙏 Acknowledgments

- **[Streamlit](https://streamlit.io/)** for the amazing web framework
- **[OpenRouter](https://openrouter.ai/)** for democratizing AI model access
- **[PostgreSQL](https://postgresql.org/)** for robust database capabilities
- **The Open Source Community** for inspiration and tools


