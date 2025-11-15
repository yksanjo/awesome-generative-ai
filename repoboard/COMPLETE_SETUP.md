# Complete Setup Guide

## Step 1: Install Docker (Required)

Docker is needed to run PostgreSQL database.

```bash
# Install Docker Desktop
brew install --cask docker
```

**After installation:**
1. Open **Docker Desktop** from Applications
2. Wait for Docker to start (whale icon in menu bar should be steady)
3. You'll see "Docker Desktop is running" when ready

## Step 2: Start Database

Once Docker is running:

```bash
cd /Users/yoshikondo/awesome-generative-ai/repoboard
./START_DATABASE.sh
```

Wait 5-10 seconds for PostgreSQL to fully start.

## Step 3: Start API

In **Terminal 1**:

```bash
cd /Users/yoshikondo/awesome-generative-ai/repoboard
./START_API.sh
```

You should see:
```
Starting RepoBoard API...
API will be available at: http://localhost:8000
INFO:     Uvicorn running on http://0.0.0.0:8000
```

**Keep this terminal open!**

## Step 4: Start Bot

In **Terminal 2** (new terminal window):

```bash
cd /Users/yoshikondo/awesome-generative-ai/repoboard
./START_BOT_CLEAN.sh
```

You should see:
```
RepoBoard Telegram Bot started!
```

**Keep this terminal open too!**

## Step 5: Test Everything

### Test API:
```bash
curl http://localhost:8000/
```

Should return: `{"message":"RepoBoard API","version":"1.0.0"}`

### Test Search:
```bash
curl "http://localhost:8000/search?q=Python&limit=5"
```

### Test Bot on Telegram:
- Send `/start` to your bot
- Send `/search Python`
- Send `/boards`

## Troubleshooting

### "Address already in use" (Port 8000)

Stop the existing API:
```bash
# Find and kill process on port 8000
lsof -ti:8000 | xargs kill -9

# Or kill all uvicorn processes
pkill -f "uvicorn.*api"
```

### "Docker not found"

Make sure Docker Desktop is:
1. Installed: `brew install --cask docker`
2. Running (check menu bar for whale icon)
3. Started (open Docker Desktop app)

### "Connection refused" (Database)

Database not running. Start it:
```bash
./START_DATABASE.sh
```

Wait 5-10 seconds, then try again.

### Bot not responding

1. Check bot is running: `ps aux | grep "bot.py" | grep -v grep`
2. Check API is running: `curl http://localhost:8000/`
3. Restart bot: `./START_BOT_CLEAN.sh`

## Quick Commands Reference

```bash
# Start database
./START_DATABASE.sh

# Start API
./START_API.sh

# Start bot
./START_BOT_CLEAN.sh

# Stop all
./STOP_ALL.sh

# Check status
./STATUS.sh
```

## That's It! 🎉

Once everything is running:
- API: http://localhost:8000
- API Docs: http://localhost:8000/docs
- Bot: Use on Telegram
