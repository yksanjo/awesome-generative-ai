# Running RepoBoard in Background

## The Problem

If you close the terminal, the bot stops. Here are solutions to keep it running!

## Solution 1: Use `screen` (Easiest)

### Install screen (if needed)
```bash
# macOS
brew install screen

# Linux (usually pre-installed)
# No installation needed
```

### Run Bot in Screen

```bash
# Start a screen session
screen -S repoboard-bot

# Inside screen, start your bot
cd /Users/yoshikondo/awesome-generative-ai/repoboard
source venv/bin/activate
cd telegram-bot
python bot.py

# Detach from screen: Press Ctrl+A, then D
# Now you can close the terminal!
```

### Reattach Later

```bash
# See all screen sessions
screen -ls

# Reattach to bot
screen -r repoboard-bot

# To stop: Press Ctrl+C, then type: exit
```

## Solution 2: Use `tmux` (Alternative)

```bash
# Start tmux session
tmux new -s repoboard-bot

# Run bot
cd /Users/yoshikondo/awesome-generative-ai/repoboard
source venv/bin/activate
cd telegram-bot
python bot.py

# Detach: Press Ctrl+B, then D
# Reattach: tmux attach -t repoboard-bot
```

## Solution 3: Run in Background with `nohup`

```bash
cd /Users/yoshikondo/awesome-generative-ai/repoboard
source venv/bin/activate
cd telegram-bot

# Run in background
nohup python bot.py > bot.log 2>&1 &

# Check if running
ps aux | grep "python bot.py"

# Stop it
pkill -f "python bot.py"
```

## Solution 4: Use `launchd` (macOS - Runs on Startup)

Create `~/Library/LaunchAgents/com.repoboard.bot.plist`:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.repoboard.bot</string>
    <key>ProgramArguments</key>
    <array>
        <string>/Users/yoshikondo/awesome-generative-ai/repoboard/venv/bin/python</string>
        <string>/Users/yoshikondo/awesome-generative-ai/repoboard/telegram-bot/bot.py</string>
    </array>
    <key>WorkingDirectory</key>
    <string>/Users/yoshikondo/awesome-generative-ai/repoboard</string>
    <key>RunAtLoad</key>
    <true/>
    <key>KeepAlive</key>
    <true/>
    <key>StandardOutPath</key>
    <string>/Users/yoshikondo/awesome-generative-ai/repoboard/bot.log</string>
    <key>StandardErrorPath</key>
    <string>/Users/yoshikondo/awesome-generative-ai/repoboard/bot.error.log</string>
</dict>
</plist>
```

Then:
```bash
# Load service
launchctl load ~/Library/LaunchAgents/com.repoboard.bot.plist

# Start
launchctl start com.repoboard.bot

# Stop
launchctl stop com.repoboard.bot

# Unload
launchctl unload ~/Library/LaunchAgents/com.repoboard.bot.plist
```

## Solution 5: Docker (Best for Production)

Create `docker-compose.bot.yml`:

```yaml
version: '3.8'
services:
  bot:
    build: .
    command: python telegram-bot/bot.py
    environment:
      - TELEGRAM_BOT_TOKEN=${TELEGRAM_BOT_TOKEN}
      - REPOBOARD_API_URL=http://api:8000
    depends_on:
      - api
    restart: unless-stopped
```

## Recommended: Use Screen (Easiest)

**Quick setup:**

```bash
# Start screen
screen -S repoboard-bot

# Run bot
cd /Users/yoshikondo/awesome-generative-ai/repoboard
source venv/bin/activate
cd telegram-bot
python bot.py

# Detach: Ctrl+A, then D
# Close terminal - bot keeps running!

# Reattach later:
screen -r repoboard-bot
```

## For Multiple Services

You can run multiple things in separate screens:

```bash
# Terminal 1: API
screen -S repoboard-api
cd repoboard && source venv/bin/activate && cd api && uvicorn main:app --reload
# Detach: Ctrl+A, D

# Terminal 2: Bot
screen -S repoboard-bot
cd repoboard && source venv/bin/activate && cd telegram-bot && python bot.py
# Detach: Ctrl+A, D

# Terminal 3: Ollama
screen -S ollama
ollama serve
# Detach: Ctrl+A, D
```

## Check What's Running

```bash
# See all screen sessions
screen -ls

# See all processes
ps aux | grep -E "(bot.py|uvicorn|ollama)"
```

## Stop Services

```bash
# Stop bot (if in screen)
screen -r repoboard-bot
# Press Ctrl+C, then: exit

# Or kill by process
pkill -f "python bot.py"
pkill -f "uvicorn"
pkill -f "ollama serve"
```


