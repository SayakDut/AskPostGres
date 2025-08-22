#!/usr/bin/env python3
"""
AskPostgres Application Runner

Simple script to run the AskPostgres application with proper error handling.
"""
import os
import sys
import subprocess
from pathlib import Path


def check_virtual_environment():
    """Check if virtual environment exists and is activated."""
    venv_path = Path("venv")
    
    if not venv_path.exists():
        print("❌ Virtual environment not found. Please run setup.py first.")
        return False
    
    # Check if we're in a virtual environment
    if hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix):
        print("✅ Virtual environment is active")
        return True
    else:
        print("⚠️  Virtual environment not activated")
        print("💡 Please activate it first:")
        if os.name == "nt":
            print("   venv\\Scripts\\activate")
        else:
            print("   source venv/bin/activate")
        return False


def check_environment_file():
    """Check if .env file exists."""
    env_file = Path(".env")
    if not env_file.exists():
        print("❌ .env file not found. Please copy .env.example to .env and configure it.")
        return False
    
    print("✅ Environment file found")
    return True


def run_application():
    """Run the Streamlit application."""
    print("🚀 Starting AskPostgres application...")
    
    try:
        # Run streamlit
        subprocess.run([
            sys.executable, "-m", "streamlit", "run", "app.py",
            "--server.port", "8501",
            "--server.address", "0.0.0.0"
        ], check=True)
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to start application: {e}")
        return False
    except KeyboardInterrupt:
        print("\n🛑 Application stopped by user")
        return True
    
    return True


def main():
    """Main runner function."""
    print("🐘💬 AskPostgres Application Runner")
    print("=" * 40)
    
    # Check virtual environment
    if not check_virtual_environment():
        sys.exit(1)
    
    # Check environment file
    if not check_environment_file():
        sys.exit(1)
    
    # Run application
    if not run_application():
        sys.exit(1)


if __name__ == "__main__":
    main()
