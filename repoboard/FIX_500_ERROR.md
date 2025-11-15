# Fix: 500 Server Error - Database Not Running

## The Problem

You're getting a 500 error because **PostgreSQL database is not running**.

The error message shows:
```
connection to server at "localhost" port 5432 failed: Connection refused
```

## Solution: Start the Database

### Option 1: Using Docker Compose (Recommended)

```bash
cd /Users/yoshikondo/awesome-generative-ai/repoboard
docker-compose up -d postgres
```

This will start PostgreSQL in the background.

### Option 2: Start All Services

```bash
cd /Users/yoshikondo/awesome-generative-ai/repoboard
docker-compose up -d
```

This starts PostgreSQL, Qdrant (vector DB), and other services.

### Option 3: Check if PostgreSQL is Already Running

```bash
docker ps | grep postgres
```

If you see a postgres container, it's running. If not, start it with Option 1.

## Verify Database is Running

```bash
# Check Docker containers
docker ps

# Test database connection
docker exec -it repoboard-postgres-1 psql -U repoboard -d repoboard -c "SELECT 1;"
```

(Replace `repoboard-postgres-1` with your actual container name from `docker ps`)

## After Starting Database

1. **Restart the API** (if it's running):
   ```bash
   # Stop current API (Ctrl+C)
   # Then restart:
   cd /Users/yoshikondo/awesome-generative-ai/repoboard
   ./START_API.sh
   ```

2. **Test the search**:
   ```bash
   curl "http://localhost:8000/search?q=Python&limit=5"
   ```

3. **Test on Telegram**:
   - Send `/search Python` to your bot
   - Should work now!

## Quick Start (All Services)

```bash
cd /Users/yoshikondo/awesome-generative-ai/repoboard

# 1. Start database and services
docker-compose up -d

# 2. Start API (in one terminal)
./START_API.sh

# 3. Start Bot (in another terminal)
./START_BOT_CLEAN.sh
```

## That's It!

Once the database is running, the 500 error should be fixed! 🎉


