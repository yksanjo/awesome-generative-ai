#!/bin/bash
# Check status of all RepoBoard services

echo "📊 RepoBoard Services Status"
echo "============================"
echo ""

# Check API
if screen -list | grep -q "repoboard-api" || pgrep -f "uvicorn main:app" > /dev/null; then
    echo "✅ API: Running"
    curl -s http://localhost:8000/ > /dev/null 2>&1 && echo "   (API responding)" || echo "   (API not responding)"
else
    echo "❌ API: Not running"
fi

# Check Bot
if screen -list | grep -q "repoboard-bot" || pgrep -f "python bot.py" > /dev/null; then
    echo "✅ Bot: Running"
else
    echo "❌ Bot: Not running"
fi

# Check Ollama
if curl -s http://localhost:11434/api/tags > /dev/null 2>&1; then
    echo "✅ Ollama: Running"
    models=$(ollama list 2>/dev/null | tail -n +2 | wc -l | tr -d ' ')
    echo "   ($models models available)"
else
    echo "❌ Ollama: Not running"
fi

echo ""
echo "Screen sessions:"
screen -ls 2>/dev/null | grep -E "(repoboard|ollama)" || echo "  (none)"

echo ""
echo "To view logs:"
echo "  screen -r repoboard-api  # API logs"
echo "  screen -r repoboard-bot  # Bot logs"


