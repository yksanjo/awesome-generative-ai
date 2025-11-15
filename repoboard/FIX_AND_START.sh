#!/bin/bash
# Fix bot conflicts and start fresh

cd "$(dirname "$0")"

echo "🔧 Fixing bot conflicts..."

# Stop all bot instances
echo "1. Stopping all bot instances..."
pkill -f "python bot.py" 2>/dev/null
sleep 2

# Verify stopped
if ps aux | grep -E "python bot.py" | grep -v grep > /dev/null; then
    echo "   ⚠️  Some instances still running, force killing..."
    pkill -9 -f "python bot.py" 2>/dev/null
    sleep 1
fi

# Check if stopped
if ps aux | grep -E "python bot.py" | grep -v grep > /dev/null; then
    echo "   ❌ Failed to stop all instances"
    echo "   Manual kill required"
    exit 1
else
    echo "   ✅ All bot instances stopped"
fi

# Check environment
echo ""
echo "2. Checking environment..."
source venv/bin/activate

if [ -f .env ]; then
    if grep -q "TELEGRAM_BOT_TOKEN=" .env; then
        echo "   ✅ Telegram token found in .env"
    else
        echo "   ❌ TELEGRAM_BOT_TOKEN not in .env"
        exit 1
    fi
else
    echo "   ❌ .env file not found"
    exit 1
fi

# Check dependencies
echo ""
echo "3. Checking dependencies..."
python -c "import telegram" 2>/dev/null && echo "   ✅ python-telegram-bot installed" || {
    echo "   ❌ Installing python-telegram-bot..."
    pip install python-telegram-bot
}

# Test imports
echo ""
echo "4. Testing imports..."
cd telegram-bot
python -c "from conversation import ConversationHandler; print('   ✅ Conversation handler OK')" 2>&1 || {
    echo "   ⚠️  Conversation handler has issues (will use fallback)"
}

# Start bot
echo ""
echo "5. Starting bot..."
echo "   Bot will start now. Press Ctrl+C to stop."
echo ""

python bot.py


