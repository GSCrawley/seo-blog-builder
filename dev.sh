#!/bin/bash
# Development script for the SEO Blog Builder application
# This script starts both the backend and frontend development servers

# Exit on error
set -e

# Set the directory to this script's directory
cd "$(dirname "$0")"

# Function to check if a command exists
command_exists() {
  command -v "$1" >/dev/null 2>&1
}

# Check prerequisites
if ! command_exists python; then
  echo "Python is not installed. Please install Python 3.11 or higher."
  exit 1
fi

if ! command_exists npm; then
  echo "npm is not installed. Please install Node.js and npm."
  exit 1
fi

if ! command_exists docker; then
  echo "Docker is not installed. Please install Docker and Docker Compose."
  echo "The application may not work correctly without Docker for Redis and PostgreSQL."
fi

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
  echo "Creating virtual environment..."
  python -m venv venv
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Install backend dependencies if requirements.txt exists
if [ -f "requirements.txt" ]; then
  echo "Installing backend dependencies..."
  pip install -r requirements.txt
fi

# Create .env file if it doesn't exist
if [ ! -f ".env" ]; then
  echo "Creating .env file from example..."
  cp .env.example .env
  echo "Please update the .env file with your API keys and credentials."
fi

# Start Docker Compose if it exists
if [ -f "docker-compose.yml" ]; then
  echo "Starting Docker services..."
  docker-compose up -d
fi

# Install frontend dependencies
echo "Installing frontend dependencies..."
cd frontend
npm install
cd ..

# Define log files
backend_log="logs/backend.log"
frontend_log="logs/frontend.log"

# Create logs directory if it doesn't exist
mkdir -p logs

# Start backend server
echo "Starting backend server..."
# Using nohup to run in background
nohup uvicorn app.main:app --reload --host 0.0.0.0 --port 8000 > "$backend_log" 2>&1 &
backend_pid=$!

# Start frontend server
echo "Starting frontend server..."
cd frontend
nohup npm start > "../$frontend_log" 2>&1 &
frontend_pid=$!
cd ..

# Print process IDs
echo "Backend server running with PID: $backend_pid"
echo "Frontend server running with PID: $frontend_pid"

# Save PIDs to a file
echo "$backend_pid $frontend_pid" > .dev_pids

echo "Development servers started!"
echo "Backend server: http://localhost:8000"
echo "Frontend server: http://localhost:3000"
echo "API Documentation: http://localhost:8000/docs"
echo "Backend logs: $backend_log"
echo "Frontend logs: $frontend_log"
echo ""
echo "To stop the servers, run: ./stop_dev.sh"

# Trap Ctrl+C to clean up
trap 'echo "Stopping servers..."; kill $backend_pid $frontend_pid 2>/dev/null; exit' INT

# Keep the script running
wait
