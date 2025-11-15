#!/bin/bash
# Start all RepoBoard services in background using screen

cd "$(dirname "$0")"

echo "🚀 Starting RepoBoard services in background..."

# Check if screen is installed
if ! command -v screen &> /dev/null; then
    echo "📦 Installing screen..."
    brew install screen
fi

# Start API in screen
if ! screen -list | grep -q "repoboard-api"; then
    echo "Starting API in screen session 'repoboard-api'..."
    screen -dmS repoboard-api bash -c "cd $(pwd) && source venv/bin/activate && cd api && uvicorn main:app --reload"
    sleep 2
    echo "✅ API started"
else
    echo "✅ API already running"
fi

# Start Bot in screen
if ! screen -list | grep -q "repoboard-bot"; then
    echo "Starting Bot in screen session 'repoboard-bot'..."
    screen -dmS repoboard-bot bash -c "cd $(pwd) && source venv/bin/activate && cd telegram-bot && python bot.py"
    sleep 2
    echo "✅ Bot started"
else
    echo "✅ Bot already running"
fi

# Check Ollama
if curl -s http://localhost:11434/api/tags > /dev/null 2>&1; then
    echo "✅ Ollama is running"
else
    echo "⚠️  Ollama is not running"
    echo "   Start it with: ollama serve"
    echo "   Or in screen: screen -dmS ollama ollama serve"
fi

echo ""
echo "✅ All services started!"
echo ""
echo "To view logs:"
echo "  screen -r repoboard-api  # View API"
echo "  screen -r repoboard-bot  # View Bot"
echo ""
echo "To stop:"
echo "  screen -r repoboard-api  # Then Ctrl+C"
echo "  screen -r repoboard-bot  # Then Ctrl+C"
echo ""
echo "Or kill all:"
echo "  pkill -f 'uvicorn'"
echo "  pkill -f 'bot.py'"


