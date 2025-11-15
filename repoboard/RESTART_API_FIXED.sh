#!/bin/bash
# Restart API with correct database settings

cd "$(dirname "$0")"

echo "🔄 Restarting API..."

# Stop any running API
pkill -f "uvicorn.*api" 2>/dev/null
pkill -f "python.*main:app" 2>/dev/null
sleep 2

# Check .env has correct DATABASE_URL
if ! grep -q "DATABASE_URL=postgresql://repoboard:repoboard" .env; then
    echo "⚠️  Fixing DATABASE_URL in .env..."
    sed -i '' 's|DATABASE_URL=.*|DATABASE_URL=postgresql://repoboard:repoboard@localhost:5432/repoboard|' .env
    echo "✅ Updated DATABASE_URL"
fi

# Activate venv and start API
source venv/bin/activate
cd api
echo "🚀 Starting API..."
uvicorn main:app --host 0.0.0.0 --port 8000 --reload


