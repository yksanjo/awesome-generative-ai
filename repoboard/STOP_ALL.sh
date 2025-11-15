#!/bin/bash
# Stop all RepoBoard services

echo "🛑 Stopping RepoBoard services..."

# Stop screen sessions
screen -S repoboard-api -X quit 2>/dev/null && echo "✅ Stopped API"
screen -S repoboard-bot -X quit 2>/dev/null && echo "✅ Stopped Bot"
screen -S ollama -X quit 2>/dev/null && echo "✅ Stopped Ollama"

# Kill processes (fallback)
pkill -f "uvicorn main:app" 2>/dev/null && echo "✅ Killed API process"
pkill -f "python bot.py" 2>/dev/null && echo "✅ Killed Bot process"
pkill -f "ollama serve" 2>/dev/null && echo "✅ Killed Ollama process"

echo ""
echo "✅ All services stopped!"


