#!/bin/bash

# AskPostgres Development Startup Script

echo "🐘💬 Starting AskPostgres Development Environment"
echo "================================================"

# Check if required tools are installed
command -v python3 >/dev/null 2>&1 || { echo "❌ Python 3 is required but not installed. Aborting." >&2; exit 1; }
command -v node >/dev/null 2>&1 || { echo "❌ Node.js is required but not installed. Aborting." >&2; exit 1; }
command -v npm >/dev/null 2>&1 || { echo "❌ npm is required but not installed. Aborting." >&2; exit 1; }

# Function to check if port is in use
check_port() {
    if lsof -Pi :$1 -sTCP:LISTEN -t >/dev/null ; then
        echo "❌ Port $1 is already in use"
        return 1
    else
        echo "✅ Port $1 is available"
        return 0
    fi
}

# Check required ports
echo "🔍 Checking required ports..."
check_port 8000 || exit 1
check_port 3000 || exit 1

# Setup backend
echo "🐍 Setting up Python backend..."
cd backend

if [ ! -d "venv" ]; then
    echo "📦 Creating Python virtual environment..."
    python3 -m venv venv
fi

echo "🔧 Activating virtual environment..."
source venv/bin/activate

echo "📥 Installing Python dependencies..."
pip install -r requirements.txt

if [ ! -f ".env" ]; then
    echo "⚙️ Creating backend .env file..."
    cp .env.example .env
    echo "⚠️  Please edit backend/.env with your configuration before continuing"
    exit 1
fi

echo "🚀 Starting FastAPI backend on port 8000..."
uvicorn main:app --reload --host 0.0.0.0 --port 8000 &
BACKEND_PID=$!

cd ..

# Setup frontend
echo "⚛️ Setting up Next.js frontend..."
cd frontend

if [ ! -d "node_modules" ]; then
    echo "📦 Installing Node.js dependencies..."
    npm install
fi

if [ ! -f ".env" ]; then
    echo "⚙️ Creating frontend .env file..."
    cp .env.example .env
fi

echo "🚀 Starting Next.js frontend on port 3000..."
npm run dev &
FRONTEND_PID=$!

cd ..

echo ""
echo "🎉 AskPostgres is starting up!"
echo "================================"
echo "🔗 Frontend: http://localhost:3000"
echo "🔗 Backend API: http://localhost:8000"
echo "📚 API Docs: http://localhost:8000/docs"
echo "❤️ Health Check: http://localhost:8000/api/v1/health"
echo ""
echo "Press Ctrl+C to stop all services"

# Wait for interrupt
trap "echo '🛑 Stopping services...'; kill $BACKEND_PID $FRONTEND_PID; exit" INT
wait
