# Fixed: 500 Error on Search

## What Was Wrong

1. **Database password mismatch** - `.env` had wrong credentials
2. **Database tables not initialized** - Tables didn't exist

## What I Fixed

1. ✅ Updated `.env` with correct DATABASE_URL:
   ```
   DATABASE_URL=postgresql://repoboard:repoboard@localhost:5432/repoboard
   ```

2. ✅ Initialized database tables:
   ```bash
   python -c "from db.connection import init_db; init_db()"
   ```

3. ✅ Improved search endpoint error handling

## Restart API

The API needs to be restarted to pick up the new `.env` settings:

```bash
# Stop current API (Ctrl+C or):
pkill -f "uvicorn.*api"

# Start API again:
cd /Users/yoshikondo/awesome-generative-ai/repoboard
./START_API.sh
```

## Test Search

```bash
curl "http://localhost:8000/search?q=Python&limit=5"
```

Should now return `[]` (empty array) if no repos, or results if repos exist.

## Next Steps

To get actual search results, you need to ingest some repos:

```bash
cd /Users/yoshikondo/awesome-generative-ai/repoboard
source venv/bin/activate

# Ingest trending repos
python jobs/ingest_trending.py

# Process repos (generate summaries)
python jobs/process_repos.py
```

Then search will return results!

## Quick Fix Commands

```bash
cd /Users/yoshikondo/awesome-generative-ai/repoboard

# 1. Fix .env (if needed)
sed -i '' 's|DATABASE_URL=.*|DATABASE_URL=postgresql://repoboard:repoboard@localhost:5432/repoboard|' .env

# 2. Initialize database
./INIT_DATABASE.sh

# 3. Restart API
pkill -f "uvicorn.*api"
./START_API.sh
```

That's it! 🎉


