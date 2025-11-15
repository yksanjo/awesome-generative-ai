# 🚀 Quick Start: Social Signals & Use-Case Finder

## What Was Built

Two new features based on your favorite remix ideas:

1. ✅ **Awesome with Social Signals** - Rank repos by real-world usage (Reddit, HN, Stack Overflow, npm, PyPI)
2. ✅ **Python Use-Case Finder** - AI-powered library recommendations ("I want to build X")

## Quick Setup

### 1. Database Migration

Create the new `social_signals` table:

```python
# In Python shell or script
from db.connection import engine
from db.models import Base, SocialSignals

Base.metadata.create_all(engine, tables=[SocialSignals.__table__])
```

### 2. Test the Features

#### Use-Case Finder (No setup needed!)
```bash
# Start API
python api/main.py

# Test in another terminal
curl "http://localhost:8000/use-case-finder?query=build+a+REST+API&language=python&limit=5"
```

#### Social Signals (Requires data)
```bash
# Update social signals for repos
python jobs/update_social_signals.py --limit 10

# Get social signals for a repo
curl "http://localhost:8000/repos/1/social-signals"

# Get repos ranked by social signals
curl "http://localhost:8000/repos/ranked-by-social-signals?limit=10"
```

## API Endpoints

### Use-Case Finder
```
GET /use-case-finder?query=<your query>&language=python&limit=10
```

**Example queries:**
- `query=build+a+REST+API`
- `query=scrape+websites`
- `query=process+images`
- `query=create+a+CLI+tool`

### Social Signals
```
GET /repos/{repo_id}/social-signals
GET /repos/ranked-by-social-signals?skip=0&limit=20
```

## Files Created

### Social Signals
- `db/models.py` - Added `SocialSignals` model
- `social-signals-service/social_fetcher.py` - Fetches metrics from APIs
- `jobs/update_social_signals.py` - Job to update signals
- `api/main.py` - Added endpoints

### Use-Case Finder
- `use-case-finder/use_case_matcher.py` - LLM-powered matcher
- `api/main.py` - Added endpoint

## Next Steps

1. **Run database migration** (create social_signals table)
2. **Test use-case finder** (works immediately if you have repos with summaries)
3. **Update social signals** (run the job to fetch metrics)
4. **Integrate into ranking** (optional - modify `curation-engine/ranker.py`)

## Full Documentation

See `FEATURES_SOCIAL_SIGNALS_USE_CASE_FINDER.md` for complete documentation.

