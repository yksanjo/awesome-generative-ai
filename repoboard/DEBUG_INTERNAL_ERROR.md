# Debug: Internal Server Error

## Quick Checks

### 1. Check API Status
```bash
curl http://localhost:8000/
```

Should return: `{"message":"RepoBoard API","version":"1.0.0"}`

### 2. Check Database
```bash
docker ps | grep postgres
```

Should show PostgreSQL container running.

### 3. Check API Logs
Look at the terminal where API is running for error messages.

### 4. Check Bot Logs
Look at the terminal where bot is running for error messages.

## Common Causes

### Database Connection Error
**Symptom:** "connection refused" or "password authentication failed"

**Fix:**
```bash
# Check database is running
docker ps | grep postgres

# If not running, start it
./START_DATABASE.sh

# Restart API
pkill -f "uvicorn"
./START_API_FIXED.sh
```

### API Not Running
**Symptom:** Connection refused on port 8000

**Fix:**
```bash
./START_API_FIXED.sh
```

### Database Tables Missing
**Symptom:** "relation does not exist"

**Fix:**
```bash
source venv/bin/activate
python -c "from db.connection import init_db; init_db()"
```

### Wrong Database Credentials
**Symptom:** "password authentication failed"

**Fix:**
```bash
# Check .env file
grep DATABASE_URL .env

# Should be:
# DATABASE_URL=postgresql://repoboard:repoboard@localhost:5432/repoboard

# If wrong, fix it:
sed -i '' 's|DATABASE_URL=.*|DATABASE_URL=postgresql://repoboard:repoboard@localhost:5432/repoboard|' .env

# Restart API
pkill -f "uvicorn"
./START_API_FIXED.sh
```

## Full Restart

If nothing works, do a full restart:

```bash
cd /Users/yoshikondo/awesome-generative-ai/repoboard

# 1. Stop everything
pkill -f "uvicorn"
./KILL_ALL_BOTS.sh

# 2. Start database
./START_DATABASE.sh
sleep 5

# 3. Initialize database (if needed)
source venv/bin/activate
python -c "from db.connection import init_db; init_db()"

# 4. Start API
./START_API_FIXED.sh

# 5. Start bot (in another terminal)
./START_BOT_CLEAN.sh
```

## Get More Details

To see the actual error:

1. **API errors:** Check the terminal where API is running
2. **Bot errors:** Check the terminal where bot is running
3. **Database errors:** Check Docker logs:
   ```bash
   docker logs repoboard-postgres-1
   ```

## Still Having Issues?

Share:
- The exact error message
- Which service is failing (API or bot)
- What command you ran that caused the error


