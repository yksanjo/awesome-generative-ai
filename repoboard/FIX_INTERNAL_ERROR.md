# Fix: Internal Server Error

## The Problem

The API is returning "Internal Server Error" for all requests. This is likely because:
1. API is using old database credentials
2. API process needs to be restarted to pick up new `.env` settings

## Solution: Restart API

```bash
cd /Users/yoshikondo/awesome-generative-ai/repoboard

# Stop API
pkill -9 -f "uvicorn"

# Start API with correct settings
./START_API_FIXED.sh
```

## Verify It's Fixed

After restarting, test:

```bash
# Test root endpoint
curl http://localhost:8000/

# Test search (should return empty array, not error)
curl "http://localhost:8000/search?q=test&limit=5"

# Test stats
curl http://localhost:8000/stats
```

## Expected Results

- Root: `{"message":"RepoBoard API","version":"1.0.0"}`
- Search: `[]` (empty array, not error)
- Stats: `{"total_repos":0,"total_boards":0,"total_categories":0}`

## If Still Getting Errors

1. **Check database is running:**
   ```bash
   docker ps | grep postgres
   ```

2. **Check .env file:**
   ```bash
   grep DATABASE_URL .env
   ```
   Should be: `DATABASE_URL=postgresql://repoboard:repoboard@localhost:5432/repoboard`

3. **Initialize database tables:**
   ```bash
   source venv/bin/activate
   python -c "from db.connection import init_db; init_db()"
   ```

4. **Check API logs** in the terminal where API is running for detailed error messages

## That's It! 🎉

After restarting the API, it should work correctly!


