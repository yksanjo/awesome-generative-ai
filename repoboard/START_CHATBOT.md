# Start Chatbot (Telegram Bot) - Quick Commands

## Prerequisites

Make sure Docker Desktop is running first!

## Step 1: Start Database

```bash
cd /Users/yoshikondo/awesome-generative-ai/repoboard
./START_DATABASE.sh
```

Wait 5-10 seconds for PostgreSQL to start.

## Step 2: Start API (Terminal 1)

```bash
cd /Users/yoshikondo/awesome-generative-ai/repoboard
./START_API.sh
```

Keep this terminal open! You should see:
```
Starting RepoBoard API...
API will be available at: http://localhost:8000
INFO:     Uvicorn running on http://0.0.0.0:8000
```

## Step 3: Start Chatbot (Terminal 2)

Open a **new terminal window** and run:

```bash
cd /Users/yoshikondo/awesome-generative-ai/repoboard
./START_BOT_CLEAN.sh
```

You should see:
```
RepoBoard Telegram Bot started!
```

## All-in-One (Copy & Paste)

```bash
# Terminal 1: Database + API
cd /Users/yoshikondo/awesome-generative-ai/repoboard
./START_DATABASE.sh
sleep 5
./START_API.sh

# Terminal 2: Bot
cd /Users/yoshikondo/awesome-generative-ai/repoboard
./START_BOT_CLEAN.sh
```

## Test the Bot

On Telegram, send to your bot:
- `/start` - Welcome message
- `/search Python` - Search for Python repos
- `/boards` - List curated boards
- `/trending` - Show trending repos
- Or just type: "Find Python libraries" (conversational)

## Stop Everything

```bash
cd /Users/yoshikondo/awesome-generative-ai/repoboard
./STOP_ALL.sh
```

Or manually:
- Press `Ctrl+C` in each terminal
- Stop database: `docker-compose down` or `docker compose down`

## Troubleshooting

### "Docker not found"
- Start Docker Desktop app first!

### "Address already in use"
- API is already running, stop it first:
  ```bash
  pkill -f "uvicorn.*api"
  ```

### "Connection refused"
- Database not running, start it:
  ```bash
  ./START_DATABASE.sh
  ```

### Bot not responding
- Check API is running: `curl http://localhost:8000/`
- Restart bot: `./START_BOT_CLEAN.sh`


