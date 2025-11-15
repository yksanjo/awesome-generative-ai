# ✅ Everything is Ready! Start Now

## Step 1: Start the API (Terminal 1)

Keep your current terminal open, or open a new one:

```bash
cd /Users/yoshikondo/awesome-generative-ai/repoboard
source venv/bin/activate
cd api
uvicorn main:app --reload
```

**You should see:**
```
INFO:     Uvicorn running on http://127.0.0.1:8000
INFO:     Application startup complete.
```

**Keep this terminal running!** Don't close it.

## Step 2: Start the Bot (Terminal 2)

Open a **NEW terminal window** (keep Terminal 1 running):

```bash
cd /Users/yoshikondo/awesome-generative-ai/repoboard
source venv/bin/activate
cd telegram-bot
python bot.py
```

**You should see:**
```
RepoBoard Telegram Bot started!
```

**Keep this terminal running too!**

## Step 3: Test on Your Phone

1. **Open Telegram** on your phone
2. **Search for your bot** (the username you created with @BotFather)
3. **Click "Start"**
4. **Send:** `/start`

You should get a welcome message!

## Try These Commands

- `/start` - Welcome message
- `/help` - Show all commands
- `/boards` - List all boards (if you have any)
- `/search python` - Search for Python repos
- `/trending` - Get trending repos

## If You See "No boards found"

You need to ingest some repos first. Open **Terminal 3**:

```bash
cd /Users/yoshikondo/awesome-generative-ai/repoboard
source venv/bin/activate

# Ingest trending repos
python jobs/ingest_trending.py

# Process them (generate summaries)
python jobs/process_repos.py

# Generate boards
python jobs/generate_boards.py
```

This will take a few minutes. Then try `/boards` again in Telegram!

## Quick Reference

**Terminal 1 (API):**
```bash
cd /Users/yoshikondo/awesome-generative-ai/repoboard
source venv/bin/activate
cd api
uvicorn main:app --reload
```

**Terminal 2 (Bot):**
```bash
cd /Users/yoshikondo/awesome-generative-ai/repoboard
source venv/bin/activate
cd telegram-bot
python bot.py
```

**Terminal 3 (Optional - Ingest repos):**
```bash
cd /Users/yoshikondo/awesome-generative-ai/repoboard
source venv/bin/activate
python jobs/ingest_trending.py
python jobs/process_repos.py
python jobs/generate_boards.py
```

## That's It! 🎉

You're all set! The bot should work on your phone now.


