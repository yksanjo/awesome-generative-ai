# 🚀 Quick Start: Telegram Bot (5 Minutes)

## Step 1: Create Bot (2 minutes)

1. Open Telegram app
2. Search: `@BotFather`
3. Send: `/newbot`
4. Name: `RepoBoard Bot`
5. Username: `yourname_repoboard_bot` (must end with `bot`)
6. **Copy the token** (looks like: `123456789:ABC...`)

## Step 2: Configure (1 minute)

```bash
cd repoboard

# Edit .env file
nano .env
# Or: open .env in any editor
```

Add:
```bash
TELEGRAM_BOT_TOKEN=paste_your_token_here
REPOBOARD_API_URL=http://localhost:8000
```

## Step 3: Install & Run (2 minutes)

```bash
# Install dependencies
cd telegram-bot
pip install -r requirements.txt

# Make sure API is running (in another terminal)
cd ../api
uvicorn main:app --reload

# Start bot (in this terminal)
cd ../telegram-bot
python bot.py
```

You should see: `RepoBoard Telegram Bot started!`

## Step 4: Use on Phone

1. Open Telegram on your phone
2. Search: `@yourname_repoboard_bot` (your bot username)
3. Click "Start"
4. Send: `/start`

## Commands to Browse Repos

### List All Boards
```
/boards
```
Shows all curated boards with buttons to view them.

### Search Repositories
```
/search python
/search machine learning
/search web framework
```
Searches for repos matching your query.

### Get Trending
```
/trending
```
Shows trending repositories sorted by stars.

### View Specific Board
Click the buttons from `/boards` to view repos in that board.

## Example Conversation

```
You: /start

Bot: 🔍 Welcome to RepoBoard Bot!
     Discover curated GitHub repositories.
     Commands:
     /boards - List all boards
     /search <query> - Search repos
     /trending - Get trending repos
     /help - Show commands

You: /boards

Bot: 📊 Curated Boards:
     • Machine Learning Tools
       25 repositories
     [Click button to view]

You: [Clicks button]

Bot: Machine Learning Tools
     Curated collection of ML frameworks...
     25 repositories:
     1. scikit-learn/scikit-learn
        Machine learning library...
        ⭐ 58000 stars
        🔗 https://github.com/...

You: /search python

Bot: 🔍 Search Results for 'python':
     1. python/cpython
        Official Python language
        ⭐ 58000 stars
        🔗 https://github.com/...
```

## Troubleshooting

**Bot not responding?**
- Check if `python bot.py` is running
- Check if API is running (`uvicorn main:app --reload`)
- Check token in `.env` is correct

**No boards found?**
- Run ingestion first:
  ```bash
  python jobs/ingest_trending.py
  python jobs/process_repos.py
  python jobs/generate_boards.py
  ```

**Can't find bot?**
- Search with `@` symbol: `@your_bot_name`
- Make sure username ends with `bot`

## That's It! 🎉

You can now browse GitHub repos from Telegram on your phone!


