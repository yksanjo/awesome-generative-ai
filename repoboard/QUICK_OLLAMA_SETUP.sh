#!/bin/bash
# Quick Ollama setup script for RepoBoard

echo "🔧 Setting up Ollama for RepoBoard..."

# Check if Ollama is installed
if ! command -v ollama &> /dev/null; then
    echo "📦 Installing Ollama..."
    brew install ollama
else
    echo "✅ Ollama is already installed"
fi

# Check if Ollama is running
if curl -s http://localhost:11434/api/tags > /dev/null 2>&1; then
    echo "✅ Ollama is running"
else
    echo "⚠️  Ollama is not running"
    echo "   Start it with: ollama serve"
fi

# Check if llama3 is available
if ollama list 2>/dev/null | grep -q llama3; then
    echo "✅ llama3 model is available"
else
    echo "📥 Pulling llama3 model (this may take a few minutes)..."
    ollama pull llama3
fi

# Update .env file
cd "$(dirname "$0")"
if [ -f .env ]; then
    # Check if already configured
    if grep -q "LLM_PROVIDER=ollama" .env; then
        echo "✅ .env already configured for Ollama"
    else
        echo "📝 Updating .env file..."
        echo "" >> .env
        echo "# Ollama Configuration" >> .env
        echo "LLM_PROVIDER=ollama" >> .env
        echo "OLLAMA_BASE_URL=http://localhost:11434" >> .env
        echo "✅ .env updated"
    fi
else
    echo "❌ .env file not found"
fi

echo ""
echo "✅ Setup complete!"
echo ""
echo "Next steps:"
echo "1. Make sure Ollama is running: ollama serve"
echo "2. Restart your bot"
echo "3. Test: Send 'Hello' to your bot on Telegram"


