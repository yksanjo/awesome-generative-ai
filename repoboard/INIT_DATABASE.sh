#!/bin/bash
# Initialize database tables

cd "$(dirname "$0")"

echo "🗄️  Initializing database tables..."

# Activate virtual environment
source venv/bin/activate

# Initialize database
python -c "from db.connection import init_db; init_db(); print('✅ Database tables created!')"

echo ""
echo "✅ Database initialized!"
echo ""
echo "You can now:"
echo "  1. Ingest repos: python jobs/ingest_trending.py"
echo "  2. Process repos: python jobs/process_repos.py"
echo "  3. Generate boards: python jobs/generate_boards.py"


