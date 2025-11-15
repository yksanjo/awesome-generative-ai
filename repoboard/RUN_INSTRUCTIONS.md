# How to Run RepoBoard

## The Problem You Had

You got `ModuleNotFoundError: No module named 'sqlalchemy'` because you were running the API outside the virtual environment.

## Solution: Always Activate Virtual Environment First

### Method 1: Use the Helper Scripts (Easiest)

```bash
cd /Users/yoshikondo/awesome-generative-ai/repoboard

# Start API (Terminal 1)
./START_API.sh

# Start Bot (Terminal 2)
./START_BOT.sh
```

### Method 2: Manual Activation

```bash
cd /Users/yoshikondo/awesome-generative-ai/repoboard

# Activate virtual environment
source venv/bin/activate

# You should see (venv) in your prompt
# Now run API
cd api
uvicorn main:app --reload
```

## Step-by-Step: Running Everything

### Terminal 1: Start API

```bash
cd /Users/yoshikondo/awesome-generative-ai/repoboard
source venv/bin/activate
cd api
uvicorn main:app --reload
```

You should see:
```
INFO:     Uvicorn running on http://127.0.0.1:8000
INFO:     Application startup complete.
```

### Terminal 2: Start Telegram Bot

```bash
cd /Users/yoshikondo/awesome-generative-ai/repoboard
source venv/bin/activate

# Make sure .env has your bot token
# Then run:
cd telegram-bot
python bot.py
```

You should see:
```
RepoBoard Telegram Bot started!
```

### Terminal 3: (Optional) Ingest Repos

```bash
cd /Users/yoshikondo/awesome-generative-ai/repoboard
source venv/bin/activate

# Ingest trending repos
python jobs/ingest_trending.py

# Process them
python jobs/process_repos.py

# Generate boards
python jobs/generate_boards.py
```

## Quick Check: Is Venv Activated?

Look for `(venv)` in your terminal prompt:
```bash
(venv) user@computer repoboard %
```

If you don't see `(venv)`, activate it:
```bash
source venv/bin/activate
```

## Verify Dependencies

```bash
source venv/bin/activate
python -c "import sqlalchemy, fastapi, telegram; print('✅ All OK!')"
```

If you get an error, install:
```bash
pip install -r requirements.txt
pip install -r telegram-bot/requirements.txt
```

## Common Issues

### "ModuleNotFoundError"
- **Solution:** Activate venv first: `source venv/bin/activate`

### "Command not found: uvicorn"
- **Solution:** Activate venv and install: `pip install uvicorn`

### "TELEGRAM_BOT_TOKEN not set"
- **Solution:** Add to `.env` file: `TELEGRAM_BOT_TOKEN=your_token`

### API not responding
- **Check:** Is API running? Visit http://localhost:8000/docs
- **Check:** Are you in the right directory?

## Summary

**Always remember:**
1. `cd repoboard`
2. `source venv/bin/activate` ← **This is important!**
3. Then run your commands

Or use the helper scripts:
- `./START_API.sh` - Starts API
- `./START_BOT.sh` - Starts bot


