# Troubleshooting Guide

## Let's Debug Step by Step

### Step 1: Check Your Location

```bash
cd /Users/yoshikondo/awesome-generative-ai/repoboard
pwd
# Should show: /Users/yoshikondo/awesome-generative-ai/repoboard
```

### Step 2: Activate Virtual Environment

```bash
source venv/bin/activate
```

**You should see `(venv)` in your prompt:**
```
(venv) user@computer repoboard %
```

If you don't see `(venv)`, the activation didn't work. Try:
```bash
which python
# Should show: .../repoboard/venv/bin/python
```

### Step 3: Check Dependencies

```bash
python -c "import sqlalchemy; print('SQLAlchemy OK')"
python -c "import fastapi; print('FastAPI OK')"
python -c "import uvicorn; print('Uvicorn OK')"
```

If any fail, install:
```bash
pip install sqlalchemy fastapi uvicorn psycopg2-binary pydantic pydantic-settings
```

### Step 4: Test API Import

```bash
cd api
python -c "import main; print('API imports OK')"
```

If this fails, check the error message.

### Step 5: Start API

```bash
# Make sure you're in api directory
cd /Users/yoshikondo/awesome-generative-ai/repoboard/api

# Make sure venv is activated
source ../venv/bin/activate

# Start API
uvicorn main:app --reload --host 127.0.0.1 --port 8000
```

## Common Errors and Fixes

### Error: "No module named 'sqlalchemy'"
**Fix:**
```bash
source venv/bin/activate
pip install -r ../requirements.txt
```

### Error: "Cannot connect to database"
**Fix:** This is OK for now! The API will start but won't work until database is set up.
You can still test the bot with mock data.

### Error: "Address already in use"
**Fix:** Port 8000 is already in use. Either:
- Kill the process: `lsof -ti:8000 | xargs kill`
- Use different port: `uvicorn main:app --reload --port 8001`

### Error: "TELEGRAM_BOT_TOKEN not set"
**Fix:** 
```bash
# Create .env file
cd /Users/yoshikondo/awesome-generative-ai/repoboard
echo "TELEGRAM_BOT_TOKEN=your_token_here" >> .env
echo "REPOBOARD_API_URL=http://localhost:8000" >> .env
```

## Quick Test Script

Run this to test everything:

```bash
#!/bin/bash
cd /Users/yoshikondo/awesome-generative-ai/repoboard

echo "1. Checking location..."
pwd

echo "2. Activating venv..."
source venv/bin/activate

echo "3. Checking Python..."
which python
python --version

echo "4. Checking dependencies..."
python -c "import sqlalchemy, fastapi, uvicorn; print('✅ All dependencies OK')" || {
    echo "❌ Installing dependencies..."
    pip install -r requirements.txt
}

echo "5. Testing API import..."
cd api
python -c "import main; print('✅ API imports OK')" || {
    echo "❌ API import failed - check error above"
    exit 1
}

echo "✅ Everything looks good! You can start the API now."
```

## Still Not Working?

Tell me:
1. What command are you running?
2. What error message do you see?
3. Are you in the repoboard directory?
4. Is venv activated? (Do you see `(venv)` in prompt?)


