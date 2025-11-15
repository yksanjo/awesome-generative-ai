# Telegram Bot Setup Guide - Step by Step

## Quick Setup (5 minutes)

### Step 1: Create Your Telegram Bot

1. **Open Telegram** on your phone or computer
2. **Search for** `@BotFather` (official Telegram bot creator)
3. **Start a chat** with BotFather
4. **Send command:** `/newbot`
5. **Choose a name:** `RepoBoard Bot` (or any name you like)
6. **Choose a username:** Must end with `bot`, e.g., `repoboard_bot` or `yourname_repoboard_bot`
7. **Copy the token** BotFather gives you (looks like: `123456789:ABCdefGHIjklMNOpqrsTUVwxyz`)

### Step 2: Configure Environment

```bash
cd repoboard
# Edit .env file
nano .env
# Or use any text editor
```

Add these lines:
```bash
TELEGRAM_BOT_TOKEN=your_token_here
REPOBOARD_API_URL=http://localhost:8000
```

**Important:** Replace `your_token_here` with the token from BotFather!

### Step 3: Install Dependencies

```bash
cd telegram-bot
pip install -r requirements.txt
```

### Step 4: Make Sure API is Running

The bot needs the RepoBoard API to be running. In one terminal:

```bash
cd api
uvicorn main:app --reload
```

Keep this running!

### Step 5: Start the Bot

In another terminal:

```bash
cd telegram-bot
python bot.py
```

You should see: `RepoBoard Telegram Bot started!`

### Step 6: Find Your Bot on Telegram

1. **Open Telegram** on your phone
2. **Search for** your bot username (e.g., `@repoboard_bot`)
3. **Click** on your bot
4. **Click** "Start" or send `/start`

### Step 7: Test Commands

Try these commands in Telegram:

- `/start` - Welcome message
- `/boards` - List all curated boards
- `/search machine learning` - Search for repos
- `/trending` - Get trending repos
- `/help` - Show all commands

## Commands Reference

### Basic Commands

- `/start` - Welcome message and instructions
- `/help` - Show all available commands
- `/boards` - List all curated boards (shows first 10)

### Browse Repos

- `/search <query>` - Search repositories
  - Example: `/search python`
  - Example: `/search machine learning`
  - Example: `/search web framework`

- `/trending` - Get trending repositories (sorted by stars)

- `/board <name>` - View specific board (click button from `/boards`)

### Interactive Buttons

When you send `/boards`, you'll see buttons. Click them to:
- View specific boards
- See repositories in that board
- Get links to repos

## Example Usage

### 1. Browse All Boards

```
You: /boards

Bot: 📊 Curated Boards:

• Machine Learning Tools
  Curated collection of ML frameworks and libraries
  25 repositories

• Web Development
  Modern web frameworks and tools
  18 repositories

[Click buttons to view boards]
```

### 2. Search for Repos

```
You: /search python

Bot: 🔍 Search Results for 'python':

1. python/cpython
   Official Python programming language
   ⭐ 58000 stars
   https://github.com/python/cpython

2. django/django
   Web framework for Python
   ⭐ 75000 stars
   https://github.com/django/django
...
```

### 3. Get Trending Repos

```
You: /trending

Bot: 🔥 Trending Repositories:

1. microsoft/vscode
   Visual Studio Code
   ⭐ 150000 stars

2. facebook/react
   React library
   ⭐ 220000 stars
...
```

## Troubleshooting

### Bot Not Responding?

1. **Check if bot is running:**
   ```bash
   # Should see: "RepoBoard Telegram Bot started!"
   ```

2. **Check if API is running:**
   ```bash
   # Visit: http://localhost:8000/docs
   # Should see API documentation
   ```

3. **Check token:**
   - Make sure token in `.env` is correct
   - No extra spaces
   - Token should start with numbers

### "Error fetching boards"

- Make sure API is running (`uvicorn main:app --reload`)
- Make sure you've ingested some repos first:
  ```bash
  python jobs/ingest_trending.py
  python jobs/process_repos.py
  python jobs/generate_boards.py
  ```

### Bot Not Found on Telegram

- Make sure you used the correct username
- Username must end with `bot`
- Try searching with `@` symbol: `@your_bot_name`

## Running in Background

### Option 1: Screen (Simple)

```bash
# Install screen if needed
# macOS: brew install screen
# Linux: sudo apt-get install screen

# Start screen session
screen -S repoboard-bot

# Run bot
cd telegram-bot
python bot.py

# Detach: Press Ctrl+A, then D
# Reattach: screen -r repoboard-bot
```

### Option 2: Systemd (Linux)

Create `/etc/systemd/system/repoboard-bot.service`:

```ini
[Unit]
Description=RepoBoard Telegram Bot
After=network.target

[Service]
Type=simple
User=your_username
WorkingDirectory=/path/to/repoboard/telegram-bot
ExecStart=/path/to/venv/bin/python bot.py
Restart=always

[Install]
WantedBy=multi-user.target
```

Then:
```bash
sudo systemctl enable repoboard-bot
sudo systemctl start repoboard-bot
```

### Option 3: Docker (Coming Soon)

## Next Steps

1. ✅ Bot is running
2. ✅ You can access it from phone
3. ✅ Test all commands
4. 🔄 Ingest some repos if you haven't:
   ```bash
   python jobs/ingest_trending.py
   python jobs/process_repos.py
   python jobs/generate_boards.py
   ```
5. 🎉 Start browsing repos!

## Tips

- **Use inline search:** Type `@your_bot_name python` in any chat to search
- **Share with friends:** Send them your bot username
- **Add to groups:** Add bot to Telegram groups to share repos
- **Bookmark:** Save your bot for quick access

Enjoy browsing GitHub repos from Telegram! 🚀


