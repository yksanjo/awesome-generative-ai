# RepoBoard Telegram Bot

Telegram bot for accessing RepoBoard curated boards directly from Telegram.

## Features

- 📊 Browse curated boards
- 🔍 Search repositories
- 🔥 Get trending repos
- 📱 Inline search in any chat
- 🔔 Subscribe to board updates (coming soon)

## Setup

### 1. Create Telegram Bot

1. Message [@BotFather](https://t.me/BotFather) on Telegram
2. Send `/newbot`
3. Choose a name: `RepoBoard Bot`
4. Choose a username: `repoboard_bot` (must end in `_bot`)
5. Copy the token you receive

### 2. Configure Environment

Add to your `.env` file:
```bash
TELEGRAM_BOT_TOKEN=your_bot_token_here
REPOBOARD_API_URL=http://localhost:8000  # Or your deployed API URL
```

### 3. Install Dependencies

```bash
cd telegram-bot
pip install -r requirements.txt
```

### 4. Run the Bot

```bash
python bot.py
```

## Commands

- `/start` - Welcome message
- `/boards` - List all curated boards
- `/search <query>` - Search repositories
- `/trending` - Get trending repos
- `/help` - Show all commands

## Inline Search

Type `@repoboard_bot <query>` in any Telegram chat to get instant results!

## Deployment

### Railway

```bash
railway init
railway up
```

Set environment variables:
- `TELEGRAM_BOT_TOKEN`
- `REPOBOARD_API_URL`

### Docker

```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["python", "bot.py"]
```

## Resource Requirements

- **RAM**: 256-512MB
- **CPU**: Minimal (mostly I/O bound)
- **Cost**: ~$5-10/month (VPS or Railway)

## Future Features

- [ ] Subscribe/unsubscribe to boards
- [ ] Daily/weekly digests
- [ ] Channel integration
- [ ] Inline search improvements
- [ ] Notifications for new repos

