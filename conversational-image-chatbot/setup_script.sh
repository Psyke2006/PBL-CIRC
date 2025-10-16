#!/bin/bash

# Conversational Image Recognition Chatbot Setup Script
# This script sets up the development environment

echo "=========================================="
echo "Conversational Image Recognition Chatbot"
echo "Setup Script"
echo "=========================================="
echo ""

# Check Python version
echo "Checking Python version..."
python3 --version

if [ $? -ne 0 ]; then
    echo "Error: Python 3 is not installed!"
    exit 1
fi

echo ""
echo "Creating project directories..."
mkdir -p uploads
mkdir -p static/css
mkdir -p static/js
mkdir -p templates
mkdir -p models
mkdir -p logs

echo "✓ Directories created"
echo ""

# Create virtual environment
echo "Creating virtual environment..."
python3 -m venv venv

if [ $? -ne 0 ]; then
    echo "Error: Failed to create virtual environment!"
    exit 1
fi

echo "✓ Virtual environment created"
echo ""

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

echo "✓ Virtual environment activated"
echo ""

# Upgrade pip
echo "Upgrading pip..."
pip install --upgrade pip

echo ""

# Install dependencies
echo "Installing dependencies from requirements.txt..."
pip install -r requirements.txt

if [ $? -ne 0 ]; then
    echo "Error: Failed to install dependencies!"
    exit 1
fi

echo "✓ Dependencies installed"
echo ""

# Create .gitkeep files
echo "Creating .gitkeep files for empty directories..."
touch uploads/.gitkeep
touch logs/.gitkeep
touch models/.gitkeep

echo "✓ .gitkeep files created"
echo ""

# Initialize database
echo "Initializing database..."
python3 -c "from database import db; print('Database initialized successfully')"

echo ""

# Run tests
echo "Running basic tests..."
python3 -c "from utils import create_required_directories; create_required_directories(); print('Utility test passed')"

echo ""

echo "=========================================="
echo "Setup Complete! 🎉"
echo "=========================================="
echo ""
echo "To start the application:"
echo "  1. Activate virtual environment: source venv/bin/activate"
echo "  2. Run the app: python app.py"
echo "  3. Open browser: http://localhost:5000"
echo ""
echo "To deactivate virtual environment: deactivate"
echo ""
echo "=========================================="
