# Terminal Instructions for Testing New Features

## Quick Start

### 1. Navigate to repoboard directory
```bash
cd repoboard
```

### 2. Activate virtual environment
```bash
source venv/bin/activate
```

### 3. Test the features

#### Option A: Run the test script
```bash
python test_new_features.py
```

#### Option B: Start the API server
```bash
python api/main.py
```

Then in another terminal window:
```bash
# Test use-case finder
curl "http://localhost:8000/use-case-finder?query=build+a+REST+API&language=python&limit=5"

# Test social signals (if you have data)
curl "http://localhost:8000/repos/1/social-signals"

# View API docs
open http://localhost:8000/docs
```

#### Option C: Update social signals
```bash
# Update social signals for first 10 repos
python jobs/update_social_signals.py --limit 10
```

## Common Issues

### Issue: "ModuleNotFoundError: No module named 'use_case_finder'"
**Fixed!** The import has been updated to handle the hyphenated directory name.

### Issue: "Database connection failed"
Make sure your database is running:
```bash
# Check if PostgreSQL is running
psql -U repoboard -d repoboard -c "SELECT 1;"
```

### Issue: "Table 'social_signals' does not exist"
Run the database migration:
```python
# In Python shell
from db.connection import engine
from db.models import Base, SocialSignals
Base.metadata.create_all(engine, tables=[SocialSignals.__table__])
```

## Full Test Sequence

```bash
# 1. Activate venv
cd repoboard
source venv/bin/activate

# 2. Run tests
python test_new_features.py

# 3. Start API (in background or new terminal)
python api/main.py &
# OR
python api/main.py  # Keep it running

# 4. Test endpoints
curl "http://localhost:8000/"
curl "http://localhost:8000/use-case-finder?query=scrape+websites&language=python"
```

## Troubleshooting

If something doesn't work:
1. Make sure venv is activated: `which python` should show `venv/bin/python`
2. Check Python path: `python -c "import sys; print(sys.path)"`
3. Verify imports: `python -c "from api.main import app; print('OK')"`

