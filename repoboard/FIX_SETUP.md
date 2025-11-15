# Fix Setup Issues

## Problem: Missing Dependencies

You're getting `ModuleNotFoundError: No module named 'sqlalchemy'` because dependencies aren't installed in the current Python environment.

## Solution

### Option 1: Use the Virtual Environment (Recommended)

```bash
cd /Users/yoshikondo/awesome-generative-ai/repoboard

# Activate virtual environment
source venv/bin/activate

# Install all dependencies
pip install -r requirements.txt

# Now run API
cd api
uvicorn main:app --reload
```

### Option 2: Install in Current Environment

If you want to use your conda/miniconda environment:

```bash
cd /Users/yoshikondo/awesome-generative-ai/repoboard

# Install dependencies
pip install -r requirements.txt

# Run API
cd api
uvicorn main:app --reload
```

## Quick Fix Commands

```bash
# Navigate to repoboard
cd /Users/yoshikondo/awesome-generative-ai/repoboard

# Activate venv (if it exists)
source venv/bin/activate

# Install all dependencies
pip install -r requirements.txt

# Verify installation
python -c "import sqlalchemy; print('SQLAlchemy OK')"
python -c "import fastapi; print('FastAPI OK')"

# Run API
cd api
uvicorn main:app --reload
```

## If Virtual Environment Doesn't Exist

```bash
cd /Users/yoshikondo/awesome-generative-ai/repoboard

# Create virtual environment
python3 -m venv venv

# Activate it
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run API
cd api
uvicorn main:app --reload
```

## Check Your Setup

```bash
# Check Python version
python --version

# Check if dependencies are installed
python -c "import sqlalchemy, fastapi, uvicorn; print('All OK!')"

# If error, install:
pip install sqlalchemy fastapi uvicorn psycopg2-binary pydantic pydantic-settings requests
```


