#!/bin/bash
# Fix all issues and start everything

cd "$(dirname "$0")"

echo "🔧 Fixing and starting RepoBoard..."
echo ""

# 1. Fix .env
echo "1. Checking .env file..."
if ! grep -q "^DATABASE_URL=postgresql://repoboard:repoboard" .env 2>/dev/null; then
    echo "   ⚠️  Fixing DATABASE_URL..."
    sed -i '' '/^DATABASE_URL=/d' .env 2>/dev/null || sed -i '/^DATABASE_URL=/d' .env 2>/dev/null
    echo "DATABASE_URL=postgresql://repoboard:repoboard@localhost:5432/repoboard" >> .env
    echo "   ✅ Fixed DATABASE_URL"
fi

# 2. Stop everything
echo ""
echo "2. Stopping existing processes..."
pkill -9 -f "uvicorn" 2>/dev/null
pkill -9 -f "python.*bot.py" 2>/dev/null
lsof -ti:8000 | xargs kill -9 2>/dev/null
sleep 2
echo "   ✅ Stopped all processes"

# 3. Check database
echo ""
echo "3. Checking database..."
if docker ps | grep -q postgres; then
    echo "   ✅ Database is running"
else
    echo "   ⚠️  Starting database..."
    ./START_DATABASE.sh
    sleep 5
fi

# 4. Initialize database if needed
echo ""
echo "4. Checking database tables..."
TABLE_COUNT=$(docker exec repoboard-postgres-1 psql -U repoboard -d repoboard -t -c "SELECT COUNT(*) FROM information_schema.tables WHERE table_schema = 'public';" 2>/dev/null | tr -d ' ' 2>/dev/null || echo "0")
if [ "$TABLE_COUNT" = "0" ] || [ -z "$TABLE_COUNT" ]; then
    echo "   ⚠️  Initializing database..."
    source venv/bin/activate
    python -c "from db.connection import init_db; init_db(); print('✅ Database initialized')" 2>&1
else
    echo "   ✅ Database tables exist"
fi

echo ""
echo "✅ Setup complete!"
echo ""
echo "Now start services:"
echo "  Terminal 1: ./START_API_FIXED.sh"
echo "  Terminal 2: ./START_BOT_CLEAN.sh"


