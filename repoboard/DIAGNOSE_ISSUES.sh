#!/bin/bash
# Diagnose what's not working

cd "$(dirname "$0")"

echo "🔍 Diagnosing RepoBoard issues..."
echo ""

# Check database
echo "1. Checking database..."
if docker ps | grep -q postgres; then
    echo "   ✅ PostgreSQL is running"
else
    echo "   ❌ PostgreSQL is NOT running"
    echo "   Fix: ./START_DATABASE.sh"
fi

# Check API
echo ""
echo "2. Checking API..."
if curl -s http://localhost:8000/ > /dev/null 2>&1; then
    echo "   ✅ API is responding"
    API_STATUS=$(curl -s http://localhost:8000/)
    echo "   Response: $API_STATUS"
else
    echo "   ❌ API is NOT responding"
    if lsof -ti:8000 > /dev/null 2>&1; then
        echo "   ⚠️  Port 8000 is in use but API not responding"
        echo "   Fix: ./FREE_PORT_8000.sh then ./START_API_FIXED.sh"
    else
        echo "   Fix: ./START_API_FIXED.sh"
    fi
fi

# Check bot
echo ""
echo "3. Checking bot..."
if ps aux | grep -q "python.*bot.py" | grep -v grep; then
    echo "   ✅ Bot is running"
else
    echo "   ❌ Bot is NOT running"
    echo "   Fix: ./START_BOT_CLEAN.sh"
fi

# Check .env
echo ""
echo "4. Checking configuration..."
if [ -f .env ]; then
    if grep -q "DATABASE_URL=postgresql://repoboard:repoboard" .env; then
        echo "   ✅ DATABASE_URL is correct"
    else
        echo "   ❌ DATABASE_URL is incorrect"
        echo "   Fix: Update .env file"
    fi
    
    if grep -q "TELEGRAM_BOT_TOKEN=" .env; then
        echo "   ✅ TELEGRAM_BOT_TOKEN is set"
    else
        echo "   ❌ TELEGRAM_BOT_TOKEN is NOT set"
        echo "   Fix: Add TELEGRAM_BOT_TOKEN to .env"
    fi
else
    echo "   ❌ .env file not found"
fi

# Check database tables
echo ""
echo "5. Checking database tables..."
if docker ps | grep -q postgres; then
    TABLE_COUNT=$(docker exec repoboard-postgres-1 psql -U repoboard -d repoboard -t -c "SELECT COUNT(*) FROM information_schema.tables WHERE table_schema = 'public';" 2>/dev/null | tr -d ' ')
    if [ "$TABLE_COUNT" -gt 0 ] 2>/dev/null; then
        echo "   ✅ Database tables exist ($TABLE_COUNT tables)"
    else
        echo "   ❌ Database tables do NOT exist"
        echo "   Fix: ./INIT_DATABASE.sh"
    fi
fi

echo ""
echo "📋 Summary:"
echo "   Run this script to see what needs to be fixed"
echo ""


