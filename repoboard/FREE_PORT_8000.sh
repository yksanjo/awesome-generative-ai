#!/bin/bash
# Free port 8000 and restart API

cd "$(dirname "$0")"

echo "🔧 Freeing port 8000..."

# Kill process on port 8000
lsof -ti:8000 | xargs kill -9 2>/dev/null

# Kill all uvicorn processes
pkill -9 -f "uvicorn" 2>/dev/null

sleep 2

# Verify port is free
if lsof -ti:8000 > /dev/null 2>&1; then
    echo "⚠️  Port 8000 still in use. Force killing..."
    lsof -ti:8000 | xargs kill -9 2>/dev/null
    sleep 1
fi

if lsof -ti:8000 > /dev/null 2>&1; then
    echo "❌ Could not free port 8000"
    echo "   Process using port 8000:"
    lsof -i:8000
    exit 1
else
    echo "✅ Port 8000 is now free"
    echo ""
    echo "Now start the API:"
    echo "  ./START_API_FIXED.sh"
fi


