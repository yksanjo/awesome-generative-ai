#!/bin/bash
# Start API with correct database configuration

cd "$(dirname "$0")"

echo "🔧 Checking configuration..."

# Ensure .env has correct DATABASE_URL
if ! grep -q "^DATABASE_URL=postgresql://repoboard:repoboard" .env 2>/dev/null; then
    echo "⚠️  Fixing DATABASE_URL in .env..."
    # Remove old DATABASE_URL lines
    sed -i '' '/^DATABASE_URL=/d' .env 2>/dev/null || sed -i '/^DATABASE_URL=/d' .env 2>/dev/null
    # Add correct one
    echo "DATABASE_URL=postgresql://repoboard:repoboard@localhost:5432/repoboard" >> .env
    echo "✅ Updated DATABASE_URL"
fi

# Stop any running API
echo "🛑 Stopping any running API..."
pkill -9 -f "uvicorn.*api" 2>/dev/null
pkill -9 -f "python.*main:app" 2>/dev/null
sleep 2

# Activate venv
source venv/bin/activate

# Verify database connection
echo "🔍 Verifying database connection..."
python -c "from shared.config import settings; print(f'Using: {settings.database_url[:30]}...')" 2>&1

# Start API
echo ""
echo "🚀 Starting RepoBoard API..."
echo "API will be available at: http://localhost:8000"
echo "API docs at: http://localhost:8000/docs"
echo ""

cd api
uvicorn main:app --host 0.0.0.0 --port 8000 --reload


