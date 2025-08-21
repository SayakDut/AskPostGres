@echo off
REM AskPostgres Development Startup Script for Windows

echo 🐘💬 Starting AskPostgres Development Environment
echo ================================================

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python is required but not installed. Aborting.
    pause
    exit /b 1
)

REM Check if Node.js is installed
node --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Node.js is required but not installed. Aborting.
    pause
    exit /b 1
)

REM Setup backend
echo 🐍 Setting up Python backend...
cd backend

if not exist "venv" (
    echo 📦 Creating Python virtual environment...
    python -m venv venv
)

echo 🔧 Activating virtual environment...
call venv\Scripts\activate.bat

echo 📥 Installing Python dependencies...
pip install -r requirements.txt

if not exist ".env" (
    echo ⚙️ Creating backend .env file...
    copy .env.example .env
    echo ⚠️  Please edit backend\.env with your configuration before continuing
    pause
    exit /b 1
)

echo 🚀 Starting FastAPI backend on port 8000...
start "AskPostgres Backend" cmd /k "uvicorn main:app --reload --host 0.0.0.0 --port 8000"

cd ..

REM Setup frontend
echo ⚛️ Setting up Next.js frontend...
cd frontend

if not exist "node_modules" (
    echo 📦 Installing Node.js dependencies...
    npm install
)

if not exist ".env" (
    echo ⚙️ Creating frontend .env file...
    copy .env.example .env
)

echo 🚀 Starting Next.js frontend on port 3000...
start "AskPostgres Frontend" cmd /k "npm run dev"

cd ..

echo.
echo 🎉 AskPostgres is starting up!
echo ================================
echo 🔗 Frontend: http://localhost:3000
echo 🔗 Backend API: http://localhost:8000
echo 📚 API Docs: http://localhost:8000/docs
echo ❤️ Health Check: http://localhost:8000/api/v1/health
echo.
echo Press any key to exit...
pause >nul
