# Fix: Bot Conflict Error

## The Error

```
Conflict: terminated by other getUpdates request; make sure that only one bot instance is running
```

## What This Means

You have **multiple bot instances running** at the same time. Telegram only allows one bot instance per token.

## Solution

### Step 1: Stop All Bot Instances

```bash
# Kill all running bot instances
pkill -f "python bot.py"

# Or find and kill manually
ps aux | grep "python bot.py"
kill <PID>
```

### Step 2: Check No Instances Running

```bash
ps aux | grep "python bot.py" | grep -v grep
```

Should return nothing.

### Step 3: Start Bot Again

```bash
cd /Users/yoshikondo/awesome-generative-ai/repoboard
source venv/bin/activate
cd telegram-bot
python bot.py
```

## Prevention

### Use Screen (Recommended)

```bash
# Check if bot is already running in screen
screen -ls | grep repoboard-bot

# If yes, attach to it instead of starting new one
screen -r repoboard-bot

# If no, start in screen
screen -S repoboard-bot
cd repoboard && source venv/bin/activate && cd telegram-bot && python bot.py
# Detach: Ctrl+A, D
```

### Use Helper Script

```bash
# This checks if already running
./START_BOT.sh
```

## Quick Fix Command

```bash
# Stop all, then start fresh
pkill -f "python bot.py"
sleep 2
cd /Users/yoshikondo/awesome-generative-ai/repoboard
source venv/bin/activate
cd telegram-bot
python bot.py
```

## That's It!

After stopping all instances and starting fresh, the error should be gone!


