#!/bin/bash
# Start bot with conflict checking

cd "$(dirname "$0")"

# Activate venv
source venv/bin/activate

# Stop any existing instances
echo "Checking for existing bot instances..."
EXISTING=$(ps aux | grep -E "python.*bot.py" | grep -v grep | wc -l | tr -d ' ')

if [ "$EXISTING" -gt 0 ]; then
    echo "⚠️  Found $EXISTING existing bot instance(s). Stopping..."
    pkill -f "python.*bot.py"
    sleep 2
fi

# Verify stopped
if ps aux | grep -E "python.*bot.py" | grep -v grep > /dev/null; then
    echo "❌ Could not stop existing instances. Please stop manually:"
    ps aux | grep -E "python.*bot.py" | grep -v grep
    exit 1
fi

echo "✅ Starting fresh bot instance..."
cd telegram-bot
python bot.py


