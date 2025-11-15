# 🚀 Quick Start: Ollama Setup

## Status Check

✅ **Ollama is installed!** (version 0.12.11)

## Next Steps

### Step 1: Start Ollama Server

Open a **new terminal** and run:

```bash
ollama serve
```

**Keep this terminal running!** This starts the Ollama server.

### Step 2: Pull a Model (In Another Terminal)

```bash
# Pull llama3 (recommended)
ollama pull llama3

# This will download ~4.7GB, takes a few minutes
```

**Alternative models:**
- `ollama pull llama2` - Smaller, faster
- `ollama pull mistral` - Very fast
- `ollama pull codellama` - Good for code

### Step 3: Verify Setup

```bash
# Check if model is available
ollama list

# Test it
ollama run llama3 "Hello, how are you?"
```

### Step 4: Update .env (Already Done!)

Your `.env` should now have:
```bash
LLM_PROVIDER=ollama
OLLAMA_BASE_URL=http://localhost:11434
```

### Step 5: Restart Your Bot

```bash
cd /Users/yoshikondo/awesome-generative-ai/repoboard
source venv/bin/activate
cd telegram-bot
python bot.py
```

## Quick Commands

```bash
# Terminal 1: Start Ollama
ollama serve

# Terminal 2: Pull model (one time)
ollama pull llama3

# Terminal 3: Restart bot
cd repoboard && source venv/bin/activate && cd telegram-bot && python bot.py
```

## Test It!

Once everything is running, try on Telegram:

```
"Hello!"
"Find Python libraries"
"Show me trending repos"
```

## Troubleshooting

**"Connection refused"**
- Make sure `ollama serve` is running
- Check: `curl http://localhost:11434/api/tags`

**"Model not found"**
- Pull the model: `ollama pull llama3`
- Check: `ollama list`

**Slow responses**
- First response is slower (model loading)
- Subsequent responses are faster
- Use smaller model if too slow

## That's It! 🎉

Once Ollama is running with a model, your bot will use it for free, local LLM processing!


