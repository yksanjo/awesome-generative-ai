# Setting Up Ollama for RepoBoard

Ollama is a free, local LLM that runs on your computer. Perfect for personal use!

## Step 1: Install Ollama

```bash
brew install ollama
```

## Step 2: Start Ollama Server

In a **new terminal**, start Ollama:

```bash
ollama serve
```

**Keep this terminal running!** Ollama needs to be running for the bot to work.

## Step 3: Pull a Model

In **another terminal**, pull a model:

```bash
# Option 1: Llama 2 (7B, good balance)
ollama pull llama2

# Option 2: Llama 3 (newer, better)
ollama pull llama3

# Option 3: Mistral (fast, efficient)
ollama pull mistral
```

**Recommendation:** Start with `llama3` - it's newer and works well.

## Step 4: Configure RepoBoard

Edit your `.env` file:

```bash
cd /Users/yoshikondo/awesome-generative-ai/repoboard
nano .env
```

Set:
```bash
LLM_PROVIDER=ollama
OLLAMA_BASE_URL=http://localhost:11434
```

## Step 5: Test Ollama

```bash
# Test if Ollama is working
ollama run llama3 "Hello, how are you?"
```

You should get a response!

## Step 6: Restart Your Bot

```bash
cd /Users/yoshikondo/awesome-generative-ai/repoboard
source venv/bin/activate
cd telegram-bot
python bot.py
```

## Quick Setup Commands

```bash
# Terminal 1: Start Ollama
ollama serve

# Terminal 2: Pull model (one time)
ollama pull llama3

# Terminal 3: Update .env
echo "LLM_PROVIDER=ollama" >> .env
echo "OLLAMA_BASE_URL=http://localhost:11434" >> .env

# Terminal 4: Restart bot
cd repoboard
source venv/bin/activate
cd telegram-bot
python bot.py
```

## Model Recommendations

| Model | Size | Speed | Quality | Best For |
|-------|------|-------|---------|----------|
| **llama3** | 4.7GB | Fast | Good | Recommended |
| llama2 | 3.8GB | Fast | Good | Alternative |
| mistral | 4.1GB | Very Fast | Good | Fast responses |
| codellama | 3.8GB | Fast | Good | Code-focused |

## Troubleshooting

### "Connection refused"
- Make sure `ollama serve` is running
- Check: `curl http://localhost:11434/api/tags`

### "Model not found"
- Pull the model: `ollama pull llama3`
- Check available: `ollama list`

### Slow responses
- Use smaller model (llama2 instead of llama3)
- Or use mistral (faster)

## Benefits of Ollama

✅ **Free** - No API costs
✅ **Local** - Your data stays on your computer
✅ **Fast** - No network latency
✅ **Private** - No data sent to external services

## That's It!

Once Ollama is running and configured, your bot will use it for:
- Understanding natural language
- Generating conversational responses
- Processing repository summaries

Enjoy your free, local LLM! 🎉


