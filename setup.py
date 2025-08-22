#!/usr/bin/env python3
"""
AskPostgres Setup Script

This script sets up the development environment for AskPostgres.
"""
import os
import sys
import subprocess
import shutil
from pathlib import Path


def run_command(command, description):
    """Run a command and handle errors."""
    print(f"🔧 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed: {e.stderr}")
        return False


def check_python_version():
    """Check if Python version is compatible."""
    print("🐍 Checking Python version...")
    if sys.version_info < (3, 8):
        print("❌ Python 3.8 or higher is required")
        return False
    print(f"✅ Python {sys.version_info.major}.{sys.version_info.minor} detected")
    return True


def setup_virtual_environment():
    """Set up Python virtual environment."""
    venv_path = Path("venv")
    
    if venv_path.exists():
        print("📦 Virtual environment already exists")
        return True
    
    print("📦 Creating virtual environment...")
    if not run_command(f"{sys.executable} -m venv venv", "Virtual environment creation"):
        return False
    
    return True


def install_dependencies():
    """Install Python dependencies."""
    venv_python = "venv/Scripts/python" if os.name == "nt" else "venv/bin/python"
    venv_pip = "venv/Scripts/pip" if os.name == "nt" else "venv/bin/pip"
    
    if not run_command(f"{venv_pip} install --upgrade pip", "Pip upgrade"):
        return False
    
    if not run_command(f"{venv_pip} install -r requirements.txt", "Dependencies installation"):
        return False
    
    return True


def setup_environment_file():
    """Set up environment configuration file."""
    env_file = Path(".env")
    env_example = Path(".env.example")
    
    if env_file.exists():
        print("⚙️ Environment file already exists")
        return True
    
    if env_example.exists():
        print("⚙️ Creating .env file from template...")
        shutil.copy(env_example, env_file)
        print("📝 IMPORTANT: Edit .env file with your actual values:")
        print("   - POSTGRES_* (your database connection details)")
        print("   - OPENROUTER_API_KEY (get free key from https://openrouter.ai/)")
        print("   - Other settings as needed")
        return True
    else:
        print("❌ .env.example template file not found")
        return False


def main():
    """Main setup function."""
    print("🐘💬 AskPostgres Setup")
    print("=" * 30)
    
    # Check Python version
    if not check_python_version():
        sys.exit(1)
    
    # Setup virtual environment
    if not setup_virtual_environment():
        sys.exit(1)
    
    # Install dependencies
    if not install_dependencies():
        sys.exit(1)
    
    # Setup environment file
    if not setup_environment_file():
        sys.exit(1)
    
    print("\n🎉 Setup completed successfully!")
    print("\n📋 Next steps:")
    print("1. Edit .env file with your configuration")
    print("2. Activate virtual environment:")
    if os.name == "nt":
        print("   venv\\Scripts\\activate")
    else:
        print("   source venv/bin/activate")
    print("3. Run the application:")
    print("   python -m streamlit run app.py")
    print("\n🔗 Application will be available at: http://localhost:8501")


if __name__ == "__main__":
    main()
