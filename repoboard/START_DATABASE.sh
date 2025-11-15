#!/bin/bash
# Start PostgreSQL database

cd "$(dirname "$0")"

echo "🐘 Starting PostgreSQL database..."

# Try docker compose (newer syntax) first, then docker-compose
if command -v docker &> /dev/null; then
    if docker compose version &> /dev/null; then
        echo "Using: docker compose"
        docker compose up -d postgres
    elif docker-compose version &> /dev/null; then
        echo "Using: docker-compose"
        docker-compose up -d postgres
    else
        echo "❌ Docker Compose not found!"
        echo ""
        echo "Install Docker Desktop:"
        echo "  brew install --cask docker"
        echo ""
        echo "Or install docker-compose:"
        echo "  pip install docker-compose"
        exit 1
    fi
    
    echo ""
    echo "⏳ Waiting for PostgreSQL to start..."
    sleep 5
    
    # Check if it's running
    if docker ps | grep -q postgres; then
        echo "✅ PostgreSQL is running!"
        echo ""
        echo "You can now start the API:"
        echo "  ./START_API.sh"
    else
        echo "⚠️  PostgreSQL might still be starting..."
        echo "Check status with: docker ps"
    fi
else
    echo "❌ Docker not found!"
    echo ""
    echo "Install Docker Desktop:"
    echo "  brew install --cask docker"
    echo ""
    echo "Then start Docker Desktop and run this script again."
    exit 1
fi


