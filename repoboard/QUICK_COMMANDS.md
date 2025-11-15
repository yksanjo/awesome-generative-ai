# Quick Commands for RepoBoard

## Important: Always Run from RepoBoard Directory!

First, navigate to the repoboard directory:
```bash
cd /Users/yoshikondo/awesome-generative-ai/repoboard
```

## Start Services

### Start API
```bash
cd /Users/yoshikondo/awesome-generative-ai/repoboard
./START_API.sh
```

### Start Telegram Bot
```bash
cd /Users/yoshikondo/awesome-generative-ai/repoboard
./START_BOT_CLEAN.sh
```

### Start Ollama (for local LLM)
```bash
cd /Users/yoshikondo/awesome-generative-ai/repoboard
./START_OLLAMA.sh
```

### Start Everything (Background)
```bash
cd /Users/yoshikondo/awesome-generative-ai/repoboard
./START_ALL_BACKGROUND.sh
```

## Stop Services

### Stop All Bots
```bash
cd /Users/yoshikondo/awesome-generative-ai/repoboard
./KILL_ALL_BOTS.sh
```

### Stop Everything
```bash
cd /Users/yoshikondo/awesome-generative-ai/repoboard
./STOP_ALL.sh
```

## Check Status

```bash
cd /Users/yoshikondo/awesome-generative-ai/repoboard
./STATUS.sh
```

## Quick Start (All in One)

```bash
# Navigate to directory
cd /Users/yoshikondo/awesome-generative-ai/repoboard

# Start API (in one terminal)
./START_API.sh

# Start Bot (in another terminal or background)
./START_BOT_CLEAN.sh
```

## Common Issue: Wrong Directory

If you get "no such file or directory", make sure you're in the right place:
```bash
pwd  # Should show: /Users/yoshikondo/awesome-generative-ai/repoboard
```

If not, run:
```bash
cd /Users/yoshikondo/awesome-generative-ai/repoboard
```


