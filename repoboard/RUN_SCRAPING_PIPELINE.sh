#!/bin/bash
# Script to run the GitHub scraping, labeling, and sorting pipeline

set -e  # Exit on error

echo "=========================================="
echo "RepoBoard: Scraping, Labeling & Sorting"
echo "=========================================="
echo ""

# Get the script directory
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR"

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "❌ Virtual environment not found!"
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "✓ Activating virtual environment..."
source venv/bin/activate

# Check if dependencies are installed
if ! python -c "import requests" 2>/dev/null; then
    echo "❌ Dependencies not installed!"
    echo "Installing dependencies..."
    pip install -r requirements.txt
fi

# Check if .env file exists
if [ ! -f ".env" ]; then
    echo "❌ .env file not found!"
    if [ -f ".env.example" ]; then
        echo "Copying .env.example to .env..."
        cp .env.example .env
        echo "⚠️  Please edit .env file with your API keys before continuing!"
        echo "   At minimum, you need:"
        echo "   - DATABASE_URL (or use SQLite for testing)"
        echo "   - LLM_PROVIDER and API key (OpenAI/Anthropic/Ollama)"
        echo "   - GITHUB_TOKEN (optional but recommended)"
        exit 1
    else
        echo "⚠️  No .env.example found. Creating basic .env..."
        cat > .env << EOF
DATABASE_URL=postgresql://user:password@localhost:5432/repoboard
LLM_PROVIDER=openai
OPENAI_API_KEY=your_key_here
GITHUB_TOKEN=your_token_here
EOF
        echo "⚠️  Please edit .env file with your API keys!"
        exit 1
    fi
fi

# Check database connection (optional check)
echo ""
echo "Checking setup..."
echo ""

# Step 1: Initialize database
echo "[1/4] Initializing database..."
python -c "from db.connection import init_db; init_db()" 2>&1 || {
    echo "⚠️  Database initialization failed. This might be okay if tables already exist."
}

# Step 2: Scrape repositories
echo ""
echo "[2/4] Scraping trending repositories from GitHub..."
echo "This may take a few minutes..."
python jobs/ingest_trending.py || {
    echo "❌ Ingestion failed!"
    echo "Common issues:"
    echo "  - GitHub API rate limit (add GITHUB_TOKEN to .env)"
    echo "  - Database connection error (check DATABASE_URL in .env)"
    exit 1
}

# Step 3: Process repositories (label with AI)
echo ""
echo "[3/4] Processing repositories (generating summaries and labels with AI)..."
echo "This may take a while and may cost money if using OpenAI..."
python jobs/process_repos.py || {
    echo "❌ Processing failed!"
    echo "Common issues:"
    echo "  - LLM API key not set or invalid"
    echo "  - API rate limits"
    echo "  - Database connection error"
    exit 1
}

# Step 4: Generate boards (sort & cluster)
echo ""
echo "[4/4] Generating boards (sorting and clustering repositories)..."
python jobs/generate_boards.py || {
    echo "❌ Board generation failed!"
    echo "Common issues:"
    echo "  - Not enough repositories processed"
    echo "  - Database connection error"
    exit 1
}

echo ""
echo "=========================================="
echo "✅ Pipeline completed successfully!"
echo "=========================================="
echo ""
echo "Next steps:"
echo "  1. Start the API: cd api && uvicorn main:app --reload"
echo "  2. Start the frontend: cd web && npm install && npm run dev"
echo "  3. Visit http://localhost:3000 to browse repositories"
echo ""


