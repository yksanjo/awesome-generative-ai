#!/bin/bash
# Start Ollama server for RepoBoard

echo "🚀 Starting Ollama server..."
echo ""
echo "This will start Ollama in the background."
echo "To stop: pkill ollama"
echo ""

# Check if Ollama is installed
if ! command -v ollama &> /dev/null; then
    echo "❌ Ollama is not installed!"
    echo "   Install with: brew install ollama"
    exit 1
fi

# Check if already running
if curl -s http://localhost:11434/api/tags > /dev/null 2>&1; then
    echo "✅ Ollama is already running"
    ollama list
else
    echo "Starting Ollama server..."
    ollama serve &
    sleep 2
    
    if curl -s http://localhost:11434/api/tags > /dev/null 2>&1; then
        echo "✅ Ollama started successfully!"
    else
        echo "❌ Failed to start Ollama"
        exit 1
    fi
fi

echo ""
echo "Available models:"
ollama list

echo ""
echo "To pull a model:"
echo "  ollama pull llama3"
echo ""
echo "To test:"
echo "  ollama run llama3 'Hello'"


