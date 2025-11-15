# Quick Start Guide (Fixed)

## Step 1: Start Database

```bash
cd /Users/yoshikondo/awesome-generative-ai/repoboard
./START_DATABASE.sh
```

Or manually:
```bash
# Try new syntax first
docker compose up -d postgres

# Or old syntax
docker-compose up -d postgres
```

## Step 2: Wait for Database

Wait 5-10 seconds for PostgreSQL to fully start.

## Step 3: Start API

```bash
cd /Users/yoshikondo/awesome-generative-ai/repoboard
./START_API.sh
```

## Step 4: Start Bot

```bash
cd /Users/yoshikondo/awesome-generative-ai/repoboard
./START_BOT_CLEAN.sh
```

## Troubleshooting

### "docker-compose: command not found"

**Solution 1:** Use new syntax:
```bash
docker compose up -d postgres  # Note: no hyphen
```

**Solution 2:** Install Docker Desktop:
```bash
brew install --cask docker
```

Then start Docker Desktop app and try again.

### "Address already in use"

The API is already running. Stop it first:
```bash
# Find and kill API process
ps aux | grep uvicorn | grep -v grep | awk '{print $2}' | xargs kill
```

Or use:
```bash
pkill -f "uvicorn.*api"
```

### "Connection refused" (Database)

PostgreSQL is not running. Start it:
```bash
./START_DATABASE.sh
```

## All-in-One Start

```bash
cd /Users/yoshikondo/awesome-generative-ai/repoboard

# 1. Start database
./START_DATABASE.sh

# 2. Wait 5 seconds, then start API (in one terminal)
./START_API.sh

# 3. Start bot (in another terminal)
./START_BOT_CLEAN.sh
```

## Verify Everything is Running

```bash
# Check database
docker ps | grep postgres

# Check API
curl http://localhost:8000/

# Check bot
ps aux | grep "bot.py" | grep -v grep
```

That's it! 🎉


