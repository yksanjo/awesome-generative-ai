# Test Conversational Features

## Quick Test

After restarting your bot, try these on Telegram:

1. **Natural search:**
   ```
   "Find Python libraries"
   ```

2. **Trending:**
   ```
   "Show me trending repos"
   ```

3. **Boards:**
   ```
   "What boards do you have?"
   ```

4. **Chat:**
   ```
   "Hello!"
   "What can you do?"
   ```

## If It Doesn't Work

The conversation feature requires:
1. ✅ LLM API key set (OpenAI, Anthropic, or Ollama)
2. ✅ Bot restarted with new code
3. ✅ API running

If you get errors, check:
- Is your LLM API key set in `.env`?
- Did you restart the bot?
- Is the API running?

## Fallback

If LLM isn't working, the bot will still work with commands:
- `/search python` ✅
- `/trending` ✅
- `/boards` ✅

But natural language won't work without LLM.


