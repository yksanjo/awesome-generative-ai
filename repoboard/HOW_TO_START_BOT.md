# How to Start the Telegram Bot

## Quick Start

```bash
cd /Users/yoshikondo/awesome-generative-ai/repoboard
./START_BOT_CLEAN.sh
```

## Prerequisites

Before starting the bot, make sure:

1. **Database is running:**
   ```bash
   ./START_DATABASE.sh
   ```

2. **API is running** (in another terminal):
   ```bash
   ./START_API_FIXED.sh
   ```

3. **Bot token is configured** in `.env`:
   ```
   TELEGRAM_BOT_TOKEN=your_token_here
   ```

## Step-by-Step

### Step 1: Start Database (if not running)

```bash
cd /Users/yoshikondo/awesome-generative-ai/repoboard
./START_DATABASE.sh
```

Wait 5-10 seconds for PostgreSQL to start.

### Step 2: Start API (Terminal 1)

```bash
cd /Users/yoshikondo/awesome-generative-ai/repoboard
./START_API_FIXED.sh
```

Keep this terminal open! You should see:
```
Starting RepoBoard API...
INFO:     Uvicorn running on http://0.0.0.0:8000
```

### Step 3: Start Bot (Terminal 2)

Open a **new terminal window** and run:

```bash
cd /Users/yoshikondo/awesome-generative-ai/repoboard
./START_BOT_CLEAN.sh
```

You should see:
```
RepoBoard Telegram Bot started!
```

## All-in-One Commands

**Terminal 1 (Database + API):**
```bash
cd /Users/yoshikondo/awesome-generative-ai/repoboard
./START_DATABASE.sh
sleep 5
./START_API_FIXED.sh
```

**Terminal 2 (Bot):**
```bash
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

## Troubleshooting

### "Docker not found"
- Start Docker Desktop app first!

### "Connection refused" (API)
- Make sure API is running: `curl http://localhost:8000/`
- Start API: `./START_API_FIXED.sh`

### "TELEGRAM_BOT_TOKEN not set"
- Add your bot token to `.env` file:
  ```
  TELEGRAM_BOT_TOKEN=your_token_here
  ```
- Get token from @BotFather on Telegram

### Bot not responding
1. Check bot is running: `ps aux | grep "bot.py" | grep -v grep`
2. Check API is running: `curl http://localhost:8000/`
3. Restart bot: `./START_BOT_CLEAN.sh`

## Stop the Bot

Press `Ctrl+C` in the terminal where the bot is running.

Or kill it:
```bash
pkill -f "python.*bot.py"
```

## That's It! 🎉

Your bot should now be running and responding on Telegram!


