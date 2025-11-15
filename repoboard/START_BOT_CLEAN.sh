#!/bin/bash
# Clean start - kill all bots first, then start fresh

cd "$(dirname "$0")"

echo "🧹 Cleaning up all bot instances..."
./KILL_ALL_BOTS.sh

echo ""
echo "⏳ Waiting 3 seconds for cleanup..."
sleep 3

echo ""
echo "🚀 Starting bot..."
source venv/bin/activate
cd telegram-bot
python bot.py


