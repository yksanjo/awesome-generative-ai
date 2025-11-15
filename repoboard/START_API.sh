#!/bin/bash
# Script to start RepoBoard API with proper environment

cd "$(dirname "$0")"

# Activate virtual environment
source venv/bin/activate

# Check if dependencies are installed
python -c "import sqlalchemy, fastapi" 2>/dev/null || {
    echo "Installing dependencies..."
    pip install -r requirements.txt
}

# Start API
echo "Starting RepoBoard API..."
echo "API will be available at: http://localhost:8000"
echo "API docs at: http://localhost:8000/docs"
echo ""
cd api
uvicorn main:app --reload


