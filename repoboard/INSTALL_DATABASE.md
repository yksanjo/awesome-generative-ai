# Install Database - Choose One Option

## Option 1: Install Docker (Recommended - Easiest)

### Install Docker Desktop

```bash
# Install via Homebrew
brew install --cask docker
```

### Start Docker Desktop

1. Open **Docker Desktop** app (from Applications)
2. Wait for it to start (whale icon in menu bar)
3. Then run:

```bash
cd /Users/yoshikondo/awesome-generative-ai/repoboard
./START_DATABASE.sh
```

### Verify Docker is Running

```bash
docker ps
```

Should show running containers (or empty list if nothing running yet).

---

## Option 2: Install PostgreSQL Locally

### Install PostgreSQL

```bash
# Install PostgreSQL 14
brew install postgresql@14

# Or latest version
brew install postgresql
```

### Start PostgreSQL Service

```bash
# For PostgreSQL 14
brew services start postgresql@14

# Or for latest
brew services start postgresql
```

### Create Database

```bash
# Connect to PostgreSQL
psql postgres

# In psql, run:
CREATE USER repoboard WITH PASSWORD 'repoboard';
CREATE DATABASE repoboard OWNER repoboard;
GRANT ALL PRIVILEGES ON DATABASE repoboard TO repoboard;
\q
```

### Update .env File

Make sure your `.env` file has:
```bash
DATABASE_URL=postgresql://repoboard:repoboard@localhost:5432/repoboard
```

---

## Option 3: Use SQLite (Simplest, but limited)

If you just want to test quickly, you can modify the code to use SQLite instead of PostgreSQL. However, this is not recommended for production.

---

## After Installation

Once database is running:

1. **Start API:**
   ```bash
   cd /Users/yoshikondo/awesome-generative-ai/repoboard
   ./START_API.sh
   ```

2. **Start Bot:**
   ```bash
   ./START_BOT_CLEAN.sh
   ```

3. **Test:**
   ```bash
   curl "http://localhost:8000/search?q=Python&limit=5"
   ```

---

## Recommendation

**Use Docker** - it's the easiest and matches the project setup. Just install Docker Desktop and run `./START_DATABASE.sh`.


