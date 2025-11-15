#!/bin/bash
# Script to start RepoBoard Telegram Bot with proper environment

cd "$(dirname "$0")"

# Activate virtual environment
source venv/bin/activate

# Check if dependencies are installed
python -c "import telegram" 2>/dev/null || {
    echo "Installing Telegram bot dependencies..."
    pip install -r telegram-bot/requirements.txt
}

# Check for bot token
if [ -z "$TELEGRAM_BOT_TOKEN" ]; then
    if [ -f .env ]; then
        export $(grep -v '^#' .env | xargs)
    else
        echo "Error: TELEGRAM_BOT_TOKEN not set!"
        echo "Add it to .env file: TELEGRAM_BOT_TOKEN=your_token"
        exit 1
    fi
fi

# Stop any existing instances first
echo "Checking for existing bot instances..."
EXISTING=$(ps aux | grep -E "python.*bot\.py|bot\.py" | grep -v grep | wc -l | tr -d ' ')

if [ "$EXISTING" -gt 0 ]; then
    echo "⚠️  Found $EXISTING existing bot instance(s). Stopping..."
    # More aggressive kill
    pkill -9 -f "bot\.py" 2>/dev/null
    pkill -9 -f "python.*bot" 2>/dev/null
    sleep 3
    
    # Verify stopped
    REMAINING=$(ps aux | grep -E "python.*bot\.py|bot\.py" | grep -v grep | wc -l | tr -d ' ')
    if [ "$REMAINING" -gt 0 ]; then
        echo "❌ Could not stop all instances. Run ./KILL_ALL_BOTS.sh"
        ps aux | grep -E "python.*bot\.py|bot\.py" | grep -v grep
        exit 1
    fi
    echo "✅ Stopped existing instances"
fi

# Start bot
echo "🚀 Starting RepoBoard Telegram Bot..."
cd telegram-bot
python bot.py

