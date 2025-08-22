# Contributing to AskPostgres 🤝

Thank you for your interest in contributing to AskPostgres! We welcome contributions from the community and are grateful for your support.

## 🌟 Ways to Contribute

### 🐛 Bug Reports
- Found a bug? Please create an issue with detailed steps to reproduce
- Include your environment details (OS, Python version, PostgreSQL version)
- Attach screenshots if applicable

### 💡 Feature Requests
- Have an idea for a new feature? We'd love to hear it!
- Create an issue with the "enhancement" label
- Describe the use case and expected behavior

### 📝 Documentation
- Help improve our documentation
- Fix typos, add examples, or clarify instructions
- Update the README or create new guides

### 🧪 Testing
- Add unit tests for better coverage
- Test edge cases and error scenarios
- Improve integration tests

### 🎨 UI/UX Improvements
- Enhance the user interface
- Improve accessibility
- Add new themes or styling options

## 🚀 Getting Started

### Development Setup

1. **Fork the repository**
   ```bash
   git clone https://github.com/yourusername/AskPostgres.git
   cd AskPostgres
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   pip install -r requirements-dev.txt  # Development dependencies
   ```

4. **Set up environment**
   ```bash
   # Edit .env with your test database credentials
   # The file is already included with placeholder values
   ```

5. **Run tests**
   ```bash
   pytest
   ```

### Development Workflow

1. **Create a feature branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make your changes**
   - Follow the coding standards below
   - Add tests for new functionality
   - Update documentation as needed

3. **Run tests and linting**
   ```bash
   pytest
   black src/
   flake8 src/
   ```

4. **Commit your changes**
   ```bash
   git add .
   git commit -m "feat: add your feature description"
   ```

5. **Push and create a pull request**
   ```bash
   git push origin feature/your-feature-name
   ```

## 📋 Coding Standards

### Python Style Guide
- Follow PEP 8 guidelines
- Use Black for code formatting
- Maximum line length: 88 characters
- Use type hints where appropriate

### Code Organization
- Keep functions small and focused
- Use descriptive variable and function names
- Add docstrings for all public functions
- Group related functionality in modules

### Testing
- Write unit tests for all new features
- Aim for >80% code coverage
- Use pytest for testing framework
- Mock external dependencies

### Documentation
- Update README.md for new features
- Add inline comments for complex logic
- Include examples in docstrings

## 🔧 Project Structure

```
AskPostgres/
├── src/
│   ├── __init__.py
│   ├── config.py           # Configuration management
│   ├── database.py         # Database operations
│   ├── llm.py             # AI model integration
│   ├── security.py        # Security utilities
│   └── ui/
│       ├── __init__.py
│       └── components.py  # UI components
├── tests/
│   ├── __init__.py
│   ├── test_database.py
│   ├── test_llm.py
│   └── test_security.py
├── app.py                 # Main application
├── requirements.txt       # Production dependencies
├── requirements-dev.txt   # Development dependencies
└── pytest.ini           # Test configuration
```

## 🧪 Testing Guidelines

### Running Tests
```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src

# Run specific test file
pytest tests/test_database.py

# Run with verbose output
pytest -v
```

### Writing Tests
- Test both happy path and error cases
- Use descriptive test names
- Mock external dependencies (database, API calls)
- Test edge cases and boundary conditions

### Example Test
```python
def test_query_validation_rejects_non_select():
    """Test that non-SELECT queries are rejected."""
    validator = QueryValidator()
    
    with pytest.raises(SecurityError):
        validator.validate("DROP TABLE users;")
```

## 📝 Commit Message Guidelines

Use conventional commit format:

- `feat:` New feature
- `fix:` Bug fix
- `docs:` Documentation changes
- `style:` Code style changes
- `refactor:` Code refactoring
- `test:` Adding or updating tests
- `chore:` Maintenance tasks

Examples:
- `feat: add dark theme support`
- `fix: resolve database connection timeout`
- `docs: update installation instructions`

## 🔍 Code Review Process

1. **Automated Checks**
   - All tests must pass
   - Code coverage should not decrease
   - Linting checks must pass

2. **Manual Review**
   - Code follows project standards
   - Changes are well-documented
   - Security implications are considered

3. **Approval**
   - At least one maintainer approval required
   - All feedback addressed

## 🚨 Security Considerations

- Never commit sensitive data (API keys, passwords)
- Validate all user inputs
- Use parameterized queries for database operations
- Follow security best practices for web applications

## 📞 Getting Help

- **Questions**: Create a GitHub issue with the "question" label
- **Discussions**: Use GitHub Discussions for general topics
- **Chat**: Join our community Discord (link in README)



---

Thank you for contributing to AskPostgres! 🎉
