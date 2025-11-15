#!/bin/bash
# Aggressively kill ALL bot instances

echo "🔍 Finding all bot instances..."

# Find all Python processes related to bot
BOT_PIDS=$(ps aux | grep -E "python.*bot\.py|bot\.py" | grep -v grep | awk '{print $2}')

if [ -z "$BOT_PIDS" ]; then
    echo "✅ No bot instances found"
else
    echo "Found bot instances: $BOT_PIDS"
    for PID in $BOT_PIDS; do
        echo "   Killing PID: $PID"
        kill -9 $PID 2>/dev/null
    done
    sleep 2
fi

# Also check for any Python processes in telegram-bot directory
TELEGRAM_PIDS=$(ps aux | grep -E "telegram-bot|telegram" | grep python | grep -v grep | awk '{print $2}')

if [ ! -z "$TELEGRAM_PIDS" ]; then
    echo "Found telegram-related processes: $TELEGRAM_PIDS"
    for PID in $TELEGRAM_PIDS; do
        echo "   Killing PID: $PID"
        kill -9 $PID 2>/dev/null
    done
    sleep 2
fi

# Final check
REMAINING=$(ps aux | grep -E "python.*bot\.py|bot\.py" | grep -v grep | wc -l | tr -d ' ')

if [ "$REMAINING" -eq 0 ]; then
    echo "✅ All bot instances stopped"
else
    echo "⚠️  Warning: $REMAINING instance(s) still running:"
    ps aux | grep -E "python.*bot\.py|bot\.py" | grep -v grep
    echo ""
    echo "Try manually:"
    echo "  pkill -9 -f 'bot.py'"
fi


