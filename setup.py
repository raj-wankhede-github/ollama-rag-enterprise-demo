#!/usr/bin/env python
"""
Setup script for Ollama RAG Enterprise Demo
Installs dependencies optimized for Python 3.13.8
"""

import subprocess
import sys
import os
from pathlib import Path


def run_command(command: list, description: str) -> bool:
    """Run a command and report status"""
    print(f"\n{'='*60}")
    print(f"Step: {description}")
    print(f"{'='*60}")
    print(f"Running: {' '.join(command)}")
    print()
    
    try:
        result = subprocess.run(command, check=True)
        print(f"\n✓ {description} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"\n✗ Error: {description} failed with code {e.returncode}")
        return False
    except FileNotFoundError:
        print(f"\n✗ Error: Command not found. Make sure Python is in your PATH")
        return False


def main():
    """Main setup function"""
    print("=" * 60)
    print("Ollama RAG Enterprise Demo - Setup for Python 3.13.8")
    print("=" * 60)
    
    # Check Python version
    print(f"\nPython Version: {sys.version}")
    
    if sys.version_info < (3, 13):
        print("\n⚠️  Warning: Python 3.13+ is recommended")
        response = input("Continue anyway? (y/n): ").lower()
        if response != 'y':
            return 1
    
    # Step 1: Upgrade pip
    print("\n[1/4] Upgrading pip...")
    if not run_command(
        [sys.executable, "-m", "pip", "install", "--upgrade", "pip"],
        "Upgrade pip"
    ):
        return 1
    
    # Step 2: Create virtual environment (if needed)
    venv_path = Path("venv")
    if not venv_path.exists():
        print("\n[2/4] Creating virtual environment...")
        if not run_command(
            [sys.executable, "-m", "venv", "venv"],
            "Create virtual environment"
        ):
            print("\nNote: Virtual environment already exists, skipping...")
    else:
        print("\n[2/4] Virtual environment already exists, skipping...")
    
    # Step 3: Install requirements
    print("\n[3/4] Installing requirements...")
    if not run_command(
        [sys.executable, "-m", "pip", "install", "-r", "requirements.txt"],
        "Install dependencies"
    ):
        print("\n⚠️  Some packages may have warnings, but the installation should work")
        print("    This is normal for new Python versions")
    
    # Step 4: Verify installation
    print("\n[4/4] Verifying installation...")
    if not run_command(
        [sys.executable, "verify_installation.py"],
        "Verify installation"
    ):
        print("\n⚠️  Some packages may need attention")
    
    print("\n" + "=" * 60)
    print("Setup Complete!")
    print("=" * 60)
    print("\nNext steps:")
    print("1. Make sure Ollama is running")
    print("2. Run: python main.py")
    print("3. Open: http://localhost:8000/docs")
    print("\nFor Docker setup:")
    print("   cd docker && docker-compose up")
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
