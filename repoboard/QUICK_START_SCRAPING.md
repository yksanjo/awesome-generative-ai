# Quick Start: Scraping, Labeling & Sorting GitHub Repos

## Your Current Setup

Based on your `.env` file:
- ✅ LLM Provider: Ollama (free, local)
- ⚠️  Database: PostgreSQL (needs setup)
- ⚠️  GitHub Token: Not set (optional but recommended)

## Option 1: Quick Start with Docker (Easiest)

### Step 1: Start Databases

```bash
cd /Users/yoshikondo/awesome-generative-ai/repoboard
docker-compose up -d
```

This starts PostgreSQL and Qdrant automatically.

### Step 2: Update .env

Make sure your `.env` has:
```bash
DATABASE_URL=postgresql://repoboard:repoboard@localhost:5432/repoboard
LLM_PROVIDER=ollama
OLLAMA_BASE_URL=http://localhost:11434
```

### Step 3: Start Ollama (if not running)

```bash
# Check if Ollama is running
ollama list

# If not, start it and pull a model
ollama pull llama3
```

### Step 4: Run the Pipeline

```bash
# Use the automated script
./RUN_SCRAPING_PIPELINE.sh

# OR run manually:
source venv/bin/activate
python -c "from db.connection import init_db; init_db()"
python jobs/ingest_trending.py
python jobs/process_repos.py
python jobs/generate_boards.py
```

## Option 2: Use Simple Standalone Script (No Database Needed)

If you want to skip the database setup:

```bash
cd /Users/yoshikondo/awesome-generative-ai/repoboard/scripts
python simple_scrape_label_sort.py
```

This script:
- ✅ No database required
- ✅ Works with or without API keys
- ✅ Saves results to JSON
- ✅ Quick and simple

## Option 3: Manual Setup

### Step 1: Install PostgreSQL

```bash
# macOS
brew install postgresql@14
brew services start postgresql@14
createdb repoboard

# Update .env
DATABASE_URL=postgresql://your_username@localhost:5432/repoboard
```

### Step 2: Install Qdrant (Vector DB)

```bash
# Using Docker (easiest)
docker run -d -p 6333:6333 qdrant/qdrant

# Or install locally
# See: https://qdrant.tech/documentation/guides/installation/
```

### Step 3: Activate Virtual Environment

```bash
cd /Users/yoshikondo/awesome-generative-ai/repoboard
source venv/bin/activate
```

### Step 4: Install Dependencies (if needed)

```bash
pip install -r requirements.txt
```

### Step 5: Initialize Database

```bash
python -c "from db.connection import init_db; init_db()"
```

### Step 6: Run the Pipeline

```bash
# Scrape repositories
python jobs/ingest_trending.py

# Label with AI (requires Ollama running)
python jobs/process_repos.py

# Sort & cluster
python jobs/generate_boards.py
```

## Troubleshooting

### "Database connection error"

**Solution 1**: Use Docker
```bash
docker-compose up -d
```

**Solution 2**: Check PostgreSQL is running
```bash
brew services list | grep postgresql
```

**Solution 3**: Use SQLite for testing (modify `db/connection.py`)

### "Ollama connection error"

Make sure Ollama is running:
```bash
ollama serve
# In another terminal:
ollama pull llama3
```

### "GitHub API rate limit"

Add a GitHub token to `.env`:
```bash
GITHUB_TOKEN=your_token_here
```

Get token from: https://github.com/settings/tokens

### "Module not found" errors

Activate virtual environment:
```bash
source venv/bin/activate
```

## Quick Test

To test with just a few repos, modify `jobs/ingest_trending.py`:

```python
# Change limit to 5 for testing
repos = ingester.ingest_trending(limit=5)
```

## Next Steps

After running the pipeline:

1. **View results via API**:
   ```bash
   cd api
   uvicorn main:app --reload
   # Visit http://localhost:8000/docs
   ```

2. **View results via Web UI**:
   ```bash
   cd web
   npm install
   npm run dev
   # Visit http://localhost:3000
   ```

3. **Query repositories**:
   ```bash
   curl http://localhost:8000/repos?category=Machine+Learning
   ```

## Need Help?

- Check `GITHUB_SCRAPING_GUIDE.md` for detailed documentation
- Check `START_HERE.md` for full setup guide
- Check `TROUBLESHOOT.md` for common issues


