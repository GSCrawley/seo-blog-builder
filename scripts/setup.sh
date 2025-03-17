#!/bin/bash

# Setup script for SEO Blog Builder

# Exit on error
set -e

echo "Setting up SEO Blog Builder development environment..."

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python -m venv venv
fi

# Activate virtual environment
source venv/bin/activate

# Install dependencies
echo "Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

# Create .env file if it doesn't exist
if [ ! -f ".env" ]; then
    echo "Creating .env file..."
    cp .env.example .env
    echo "Please update the .env file with your actual credentials."
fi

# Create necessary directories
echo "Creating necessary directories..."
mkdir -p logs
mkdir -p migrations/versions

# Initialize database
echo "Initializing database..."
# In a real setup, this would run database migrations
# alembic upgrade head

echo "Setup complete!"
echo ""
echo "Next steps:"
echo "1. Update the .env file with your API keys and credentials"
echo "2. Run the application: python -m app.main"
echo ""
echo "Development environment is ready!"
