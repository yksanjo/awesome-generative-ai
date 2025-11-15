# Running RepoBoard in Background

## Quick Answer

**Yes, closing the terminal stops the bot.** But you can run it in the background!

## Easiest Solution: Use Screen

### Start Bot in Background

```bash
# Start screen session
screen -S repoboard-bot

# Run bot
cd /Users/yoshikondo/awesome-generative-ai/repoboard
source venv/bin/activate
cd telegram-bot
python bot.py

# Detach: Press Ctrl+A, then D
# Now close terminal - bot keeps running!
```

### Reattach Later

```bash
# See all sessions
screen -ls

# Reattach
screen -r repoboard-bot

# Stop: Press Ctrl+C, then type: exit
```

## Even Easier: Use Helper Scripts

I created helper scripts for you!

### Start Everything in Background

```bash
cd /Users/yoshikondo/awesome-generative-ai/repoboard
./START_ALL_BACKGROUND.sh
```

This starts:
- ✅ API in background
- ✅ Bot in background
- ✅ Checks Ollama

### Check Status

```bash
./STATUS.sh
```

Shows what's running.

### Stop Everything

```bash
./STOP_ALL.sh
```

## Manual Screen Setup

### For API:

```bash
screen -S repoboard-api
cd repoboard && source venv/bin/activate && cd api && uvicorn main:app --reload
# Detach: Ctrl+A, D
```

### For Bot:

```bash
screen -S repoboard-bot
cd repoboard && source venv/bin/activate && cd telegram-bot && python bot.py
# Detach: Ctrl+A, D
```

### For Ollama:

```bash
screen -S ollama
ollama serve
# Detach: Ctrl+A, D
```

## Screen Commands

- `screen -ls` - List all sessions
- `screen -r <name>` - Reattach to session
- `screen -S <name>` - Create new session
- `Ctrl+A, D` - Detach (keeps running)
- `Ctrl+A, K` - Kill current session
- `exit` - Exit and stop session

## Alternative: nohup

```bash
cd repoboard
source venv/bin/activate
cd telegram-bot
nohup python bot.py > bot.log 2>&1 &

# Check if running
ps aux | grep "python bot.py"

# Stop
pkill -f "python bot.py"
```

## Check What's Running

```bash
# See screen sessions
screen -ls

# See processes
ps aux | grep -E "(bot|uvicorn|ollama)"
```

## Recommended Setup

**Use the helper script:**

```bash
./START_ALL_BACKGROUND.sh
```

This starts everything in background screens. You can close all terminals and everything keeps running!

## That's It!

Now your bot will keep running even when you close the terminal! 🎉


