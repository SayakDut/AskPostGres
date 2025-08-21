# AskPostgres 🐘💬

A professional, production-ready web application that enables users to query PostgreSQL databases using natural language powered by AI. Built with a Python FastAPI backend and Next.js frontend, integrated with OpenRouter API.

![AskPostgres Demo](https://via.placeholder.com/800x400/3B82F6/FFFFFF?text=AskPostgres+Demo)

## 🏗️ Architecture

- **Backend**: Python FastAPI with async PostgreSQL support
- **Frontend**: Next.js 14 with React 18 and TypeScript
- **Database**: PostgreSQL with read-only query enforcement
- **AI Integration**: OpenRouter API with GPT-OSS-20B model
- **Communication**: RESTful API between frontend and backend

## ✨ Features

- **Natural Language Queries**: Ask questions in plain English and get SQL results
- **AI-Powered**: Uses OpenRouter API with GPT-OSS-20B model for SQL generation
- **Secure by Design**: Read-only queries only, comprehensive input validation
- **Interactive Results**: Sortable, filterable, paginated data tables with TanStack Table
- **Real-time Feedback**: Loading states, error handling, and toast notifications
- **Modern UI**: Built with Tailwind CSS and Framer Motion animations
- **Rate Limited**: Built-in API rate limiting (30 requests/minute)
- **Export Functionality**: Download results as CSV
- **Professional Logging**: Structured logging with request tracking
- **Health Monitoring**: Health check endpoints for system monitoring

## 🚀 Quick Start

### Prerequisites

- Python 3.8+ with pip
- Node.js 18+ and npm/yarn
- PostgreSQL database (local or remote)
- OpenRouter API key (free tier available)

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd askpostgres
   ```

2. **Backend Setup (Python FastAPI)**
   ```bash
   cd backend

   # Create virtual environment
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate

   # Install dependencies
   pip install -r requirements.txt

   # Set up environment variables
   cp .env.example .env
   ```

   Edit `backend/.env` with your configuration:
   ```env
   # PostgreSQL Database Configuration
   POSTGRES_HOST=localhost
   POSTGRES_PORT=5432
   POSTGRES_DB=your_database_name
   POSTGRES_USER=your_username
   POSTGRES_PASSWORD=your_password

   # OpenRouter API Configuration
   OPENROUTER_API_KEY=your_openrouter_api_key_here

   # Application Configuration
   SITE_URL=http://localhost:3000
   SITE_NAME=AskPostgres
   SECRET_KEY=your-secret-key-here
   ```

3. **Frontend Setup (Next.js)**
   ```bash
   cd frontend

   # Install dependencies
   npm install
   # or
   yarn install

   # Set up environment variables
   cp .env.example .env
   ```

   Edit `frontend/.env` with your configuration:
   ```env
   NEXT_PUBLIC_API_BASE_URL=http://localhost:8000/api/v1
   ```

4. **Start the applications**

   **Backend (Terminal 1):**
   ```bash
   cd backend
   uvicorn main:app --reload --host 0.0.0.0 --port 8000
   ```

   **Frontend (Terminal 2):**
   ```bash
   cd frontend
   npm run dev
   ```

5. **Open your browser**
   Navigate to [http://localhost:3000](http://localhost:3000)

## 🔧 Configuration

### Database Setup

Ensure your PostgreSQL database is running and accessible. The application requires:
- Read access to your database tables
- Connection to the `information_schema` for table introspection

### OpenRouter API Key

1. Sign up at [OpenRouter](https://openrouter.ai/)
2. Get your free API key
3. Add it to your `.env` file

The application uses the free `openai/gpt-oss-20b:free` model by default.

## 🛡️ Security Features

- **Read-Only Queries**: Only SELECT statements are allowed
- **SQL Injection Prevention**: Comprehensive input validation and sanitization
- **Rate Limiting**: 30 requests per minute per IP address
- **Query Validation**: Multi-layer security checks on generated SQL
- **Input Sanitization**: All user inputs are cleaned and validated
- **Environment Isolation**: All sensitive data in environment variables

## 📊 Usage Examples

### Example Queries

Try these natural language queries:

- "Show me all users who registered this month"
- "What are the top 10 best-selling products?"
- "Find customers with orders over $1000"
- "Show me the average order value by month"
- "List all products that are out of stock"

### API Endpoints

#### POST `/api/query`
Execute a natural language query

**Request:**
```json
{
  "query": "Show me all users who signed up last week"
}
```

**Response:**
```json
{
  "success": true,
  "data": {
    "originalQuery": "Show me all users who signed up last week",
    "generatedSQL": "SELECT * FROM users WHERE created_at >= NOW() - INTERVAL '7 days' LIMIT 100",
    "explanation": "This query retrieves all users who registered in the last 7 days",
    "confidence": 0.95,
    "results": [...],
    "resultCount": 42,
    "warnings": []
  }
}
```

#### GET `/api/schema`
Get database schema information

**Response:**
```json
{
  "success": true,
  "data": {
    "tables": [...],
    "tableCount": 5,
    "totalColumns": 23
  }
}
```

## 🏗️ Project Structure

```
askpostgres/
├── backend/                    # Python FastAPI Backend
│   ├── app/
│   │   ├── __init__.py
│   │   ├── config.py          # Configuration settings
│   │   ├── database.py        # PostgreSQL connection and queries
│   │   ├── llm.py            # OpenRouter API integration
│   │   ├── models.py         # Pydantic models for API
│   │   ├── routes.py         # API route handlers
│   │   └── security.py       # Security and validation utilities
│   ├── main.py               # FastAPI application entry point
│   ├── requirements.txt      # Python dependencies
│   └── .env.example         # Backend environment variables
├── frontend/                  # Next.js Frontend
│   ├── app/
│   │   ├── globals.css       # Global styles
│   │   ├── layout.tsx        # Root layout
│   │   └── page.tsx          # Main application page
│   ├── components/           # React components
│   │   ├── ErrorMessage.tsx
│   │   ├── LoadingSpinner.tsx
│   │   ├── QueryInput.tsx
│   │   ├── ResultsTable.tsx
│   │   └── Toast.tsx
│   ├── hooks/               # Custom React hooks
│   │   └── useToast.ts
│   ├── lib/                 # Frontend utilities
│   │   └── api.ts           # Backend API client
│   ├── package.json         # Frontend dependencies
│   └── .env.example        # Frontend environment variables
└── README.md               # This file
```

## 🔧 Development

### Backend Development (Python FastAPI)

**Available Scripts:**
```bash
cd backend

# Start development server
uvicorn main:app --reload

# Or use the run script
python run.py

# Run tests (if implemented)
pytest

# Format code
black .
isort .
```

**Adding New Features:**
1. **Database Functions**: Add to `app/database.py`
2. **API Endpoints**: Add to `app/routes.py`
3. **Security Rules**: Update `app/security.py`
4. **Data Models**: Add to `app/models.py`

### Frontend Development (Next.js)

**Available Scripts:**
```bash
cd frontend

# Start development server
npm run dev

# Build for production
npm run build

# Start production server
npm run start

# Run linting
npm run lint
```

**Adding New Features:**
1. **UI Components**: Create in `components/`
2. **API Integration**: Update `lib/api.ts`
3. **Custom Hooks**: Add to `hooks/`
4. **Styling**: Update Tailwind classes or `app/globals.css`

## 🚀 Deployment

### Docker Compose (Recommended for Development)

```bash
# Set your OpenRouter API key
export OPENROUTER_API_KEY=your_api_key_here

# Start all services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

### Production Deployment

**Backend (FastAPI):**
- Deploy to services like Railway, Render, or AWS ECS
- Use environment variables for configuration
- Set up proper logging and monitoring

**Frontend (Next.js):**
- Deploy to Vercel, Netlify, or similar platforms
- Configure `NEXT_PUBLIC_API_BASE_URL` to point to your backend

**Database:**
- Use managed PostgreSQL services like AWS RDS, Google Cloud SQL, or Supabase
- Ensure proper security groups and access controls

### Environment Variables

**Backend (.env):**
```env
POSTGRES_HOST=your_db_host
POSTGRES_PORT=5432
POSTGRES_DB=your_database
POSTGRES_USER=your_username
POSTGRES_PASSWORD=your_password
OPENROUTER_API_KEY=your_openrouter_key
SECRET_KEY=your_secret_key
ALLOWED_ORIGINS=https://your-frontend-domain.com
```

**Frontend (.env):**
```env
NEXT_PUBLIC_API_BASE_URL=https://your-backend-api.com/api/v1
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Troubleshooting

### Common Issues

**Database Connection Failed**
- Check your PostgreSQL server is running
- Verify connection credentials in `.env`
- Ensure database exists and user has access

**OpenRouter API Errors**
- Verify your API key is correct
- Check you haven't exceeded rate limits
- Ensure you have credits (if using paid models)

**Build Errors**
- Clear `.next` folder and rebuild
- Check all environment variables are set
- Verify Node.js version compatibility

### Getting Help

- Check the [Issues](https://github.com/your-repo/issues) page
- Review the troubleshooting section above
- Ensure all environment variables are properly configured
- Check backend logs: `docker-compose logs backend`
- Check frontend logs: `docker-compose logs frontend`

## 🧪 Testing

### Backend Testing
```bash
cd backend
pytest tests/
```

### Frontend Testing
```bash
cd frontend
npm test
```

### API Testing
Use the interactive API documentation at `http://localhost:8000/docs` when the backend is running.

## 🔒 Security Features

- **SQL Injection Prevention**: Multi-layer validation and sanitization
- **Read-Only Enforcement**: Only SELECT queries allowed
- **Rate Limiting**: 30 requests per minute per IP
- **Input Validation**: Comprehensive input sanitization
- **CORS Protection**: Configurable allowed origins
- **Environment Isolation**: All secrets in environment variables

## 🙏 Acknowledgments

- [FastAPI](https://fastapi.tiangolo.com/) - Modern Python web framework
- [Next.js](https://nextjs.org/) - React framework
- [OpenRouter](https://openrouter.ai/) - AI API platform
- [PostgreSQL](https://www.postgresql.org/) - Advanced open source database
- [TanStack Table](https://tanstack.com/table) - Data table library
- [Framer Motion](https://www.framer.com/motion/) - Animation library
- [Tailwind CSS](https://tailwindcss.com/) - CSS framework
- [asyncpg](https://github.com/MagicStack/asyncpg) - Fast PostgreSQL adapter
