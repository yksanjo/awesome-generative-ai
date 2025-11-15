# 🗣️ Quick Start: Conversational Features

## What's New

Your bot now understands natural language! You can chat with it like a friend.

## Restart Your Bot

**Stop the current bot** (Ctrl+C in the terminal where it's running), then:

```bash
cd /Users/yoshikondo/awesome-generative-ai/repoboard
source venv/bin/activate
cd telegram-bot
python bot.py
```

## Try These on Telegram

Instead of commands, just talk naturally:

### Natural Language Examples

**Before (commands only):**
```
/search python
/trending
/boards
```

**Now (natural language):**
```
"Find Python libraries"
"Show me trending repos"
"What boards do you have?"
"Hello!"
"What can you do?"
```

### Example Conversations

```
You: "Hi there!"
Bot: "Hello! I'm RepoBoard Bot. I can help you discover GitHub repositories..."

You: "Find me some Python web frameworks"
Bot: [Searches and shows Python web frameworks]

You: "What's popular right now?"
Bot: [Shows trending repositories]

You: "Show me machine learning tools"
Bot: [Searches for ML tools]
```

## Web Chat Interface

### Start Web Frontend

```bash
cd /Users/yoshikondo/awesome-generative-ai/repoboard/web
npm install  # if not done yet
npm run dev
```

### Visit Chat Page

Go to: http://localhost:3000/chat

You'll see a beautiful chat interface where you can:
- Type naturally
- Get conversational responses
- See repository results inline

## How It Works

1. **You type:** "Find Python libraries"
2. **Bot understands:** Intent = search, Query = "Python libraries"
3. **Bot searches:** Finds matching repos
4. **Bot responds:** Shows results conversationally

## Features

✅ **Natural language understanding**
✅ **Intent recognition** (search, trending, boards)
✅ **Conversational responses**
✅ **Smart query extraction**
✅ **Web chat interface**
✅ **Telegram chat interface**

## Commands Still Work

All commands still work:
- `/search python` ✅
- `/trending` ✅
- `/boards` ✅

But now you can also just talk! 🎉

## Try It Now!

1. **Restart your bot** (see above)
2. **Send a natural message** on Telegram: "Find Python libraries"
3. **See the magic!** ✨

Enjoy your conversational RepoBoard bot!


