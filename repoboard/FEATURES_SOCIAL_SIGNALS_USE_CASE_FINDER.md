# 🚀 New Features: Social Signals & Use-Case Finder

Two powerful new features have been added to RepoBoard:

1. **Awesome with Social Signals** - Rank repositories by real-world usage
2. **Python Use-Case Finder** - AI-powered library recommendations

---

## 1. Awesome with Social Signals

### Overview

Rank repositories by real-world usage metrics, not just GitHub stars. This feature tracks:
- **Reddit** mentions and upvotes
- **HackerNews** mentions, points, and comments
- **Stack Overflow** questions, views, and scores
- **npm** weekly downloads (for JavaScript packages)
- **PyPI** weekly downloads (for Python packages)
- **Aggregated Social Score** (0-100) combining all metrics

### Database Schema

A new `SocialSignals` table has been added to track these metrics:

```python
class SocialSignals(Base):
    repo_id: int
    reddit_mentions: int
    reddit_upvotes: int
    reddit_subreddits: List[str]
    hn_mentions: int
    hn_points: int
    hn_comments: int
    stackoverflow_questions: int
    stackoverflow_views: int
    stackoverflow_score: int
    npm_weekly_downloads: int
    pypi_weekly_downloads: int
    package_name: str
    twitter_mentions: int
    social_score: float  # Aggregated score 0-100
```

### API Endpoints

#### Get Social Signals for a Repository
```http
GET /repos/{repo_id}/social-signals
```

**Response:**
```json
{
  "repo_id": 1,
  "reddit_mentions": 15,
  "reddit_upvotes": 450,
  "reddit_subreddits": ["r/programming", "r/Python"],
  "hn_mentions": 3,
  "hn_points": 120,
  "hn_comments": 45,
  "stackoverflow_questions": 250,
  "stackoverflow_views": 15000,
  "stackoverflow_score": 500,
  "npm_weekly_downloads": 0,
  "pypi_weekly_downloads": 50000,
  "package_name": "requests",
  "twitter_mentions": 0,
  "social_score": 75.5,
  "last_updated": "2024-01-15T10:30:00Z"
}
```

#### Get Repositories Ranked by Social Signals
```http
GET /repos/ranked-by-social-signals?skip=0&limit=20
```

**Response:**
```json
[
  {
    "repo": { /* RepoMetadata */ },
    "summary": { /* RepoSummary */ },
    "social_signals": {
      "social_score": 85.2,
      "reddit_upvotes": 1200,
      "hn_points": 500,
      "npm_weekly_downloads": 1000000,
      "pypi_weekly_downloads": 0
    }
  }
]
```

### Updating Social Signals

Run the update job to fetch social signals for repositories:

```bash
# Update all repos
python jobs/update_social_signals.py

# Update first 100 repos
python jobs/update_social_signals.py --limit 100

# Custom batch size
python jobs/update_social_signals.py --batch-size 25
```

**Note:** This job makes external API calls and may take time. Consider running it periodically (e.g., weekly) via a cron job.

### Social Score Calculation

The aggregated social score (0-100) is calculated as:
- Reddit upvotes: max 20 points (100 upvotes = 20 points)
- HackerNews points: max 25 points (50 points = 25 points)
- Stack Overflow views: max 20 points (10,000 views = 20 points)
- npm downloads: max 15 points (100,000 weekly downloads = 15 points)
- PyPI downloads: max 15 points (100,000 weekly downloads = 15 points)
- Mentions bonus: max 5 points (10 mentions = 5 points)

---

## 2. Python Use-Case Finder

### Overview

AI-powered library recommendation system. Users describe what they want to build, and the system recommends the best Python libraries for that use case.

### How It Works

1. User provides a natural language query (e.g., "I want to build a REST API")
2. System finds candidate Python repositories
3. LLM analyzes the query and repositories
4. Returns ranked recommendations with:
   - Match score (0-100)
   - Reasoning
   - Pros and cons
   - Alternatives
   - Recommended stack
   - Getting started tips

### API Endpoint

#### Find Repositories for a Use Case
```http
GET /use-case-finder?query=build+a+REST+API&language=python&limit=10
```

**Parameters:**
- `query` (required): Natural language description of what you want to build
- `language` (optional): Programming language filter (default: "python")
- `limit` (optional): Number of recommendations (default: 10, max: 20)

**Example Queries:**
- "I want to build a REST API"
- "scrape websites"
- "process images"
- "create a web scraper"
- "build a machine learning model"
- "work with databases"
- "create a CLI tool"

**Response:**
```json
{
  "recommendations": [
    {
      "repo_id": 42,
      "match_score": 95,
      "reason": "FastAPI is the most popular modern Python web framework for building REST APIs. It's fast, has automatic API documentation, and is production-ready.",
      "pros": [
        "Fast performance",
        "Automatic OpenAPI docs",
        "Type hints support",
        "Async support"
      ],
      "cons": [
        "Newer than Flask/Django",
        "Smaller ecosystem"
      ],
      "alternatives": ["Flask", "Django REST Framework"],
      "repo": {
        "id": 42,
        "name": "fastapi",
        "full_name": "tiangolo/fastapi",
        "url": "https://github.com/tiangolo/fastapi",
        "description": "Fast, web framework for building APIs",
        "stars": 70000,
        "forks": 5800,
        "topics": ["python", "api", "rest", "fastapi"],
        "languages": {"Python": 100}
      }
    }
  ],
  "use_case_category": "web-api",
  "recommended_stack": ["fastapi", "uvicorn", "pydantic"],
  "getting_started_tip": "Install FastAPI with 'pip install fastapi uvicorn', then create a simple app.py file with @app.get('/') decorator."
}
```

### Implementation Details

The use-case finder:
1. Queries the database for Python repositories with summaries
2. Formats repository data for LLM analysis
3. Uses LLM (OpenAI/Anthropic/Ollama) to match use cases
4. Returns structured recommendations with scores

**LLM Prompt:**
The system uses a carefully crafted prompt that asks the LLM to:
- Analyze how well each repository matches the use case
- Consider maturity, documentation, community support
- Provide pros/cons and alternatives
- Suggest a complete stack

---

## Setup & Configuration

### Database Migration

You'll need to create the new `social_signals` table:

```python
# Run this in Python or create a migration script
from db.connection import engine
from db.models import Base, SocialSignals

# Create the table
Base.metadata.create_all(engine, tables=[SocialSignals.__table__])
```

Or use Alembic (if configured):
```bash
alembic revision --autogenerate -m "Add social signals table"
alembic upgrade head
```

### Environment Variables

No new environment variables are required. The features use existing:
- `OPENAI_API_KEY` or `ANTHROPIC_API_KEY` (for use-case finder)
- `OLLAMA_BASE_URL` (if using Ollama)

### Dependencies

The social signals service uses:
- `requests` (for API calls)

The use-case finder uses:
- Existing LLM client (OpenAI/Anthropic/Ollama)

Both are already in `requirements.txt`.

---

## Usage Examples

### Example 1: Find Libraries for Web Scraping

```bash
curl "http://localhost:8000/use-case-finder?query=scrape+websites&language=python&limit=5"
```

### Example 2: Get Social Signals for a Repository

```bash
curl "http://localhost:8000/repos/1/social-signals"
```

### Example 3: Get Top Repos by Real-World Usage

```bash
curl "http://localhost:8000/repos/ranked-by-social-signals?limit=10"
```

### Example 4: Update Social Signals

```bash
# Update first 50 repos
python jobs/update_social_signals.py --limit 50
```

---

## Integration with Existing Features

### Ranking Algorithm

You can integrate social signals into the existing ranking algorithm:

```python
# In curation-engine/ranker.py
def calculate_score_with_social_signals(repo, social_signals):
    base_score = calculate_base_score(repo)
    social_weight = 0.2  # 20% weight for social signals
    social_component = (social_signals.social_score / 100) * social_weight
    return base_score + social_component
```

### Use-Case Finder in Chat

The use-case finder can be integrated into the chat endpoint:

```python
# In api/main.py chat endpoint
if "I want to build" in user_message or "recommend" in user_message.lower():
    from use_case_finder.use_case_matcher import UseCaseFinder
    finder = UseCaseFinder()
    result = finder.find_repos_for_use_case(user_message, db=db)
    # Return recommendations
```

---

## Performance Considerations

### Social Signals

- **Rate Limiting**: External APIs (Reddit, HN, Stack Overflow) have rate limits
- **Caching**: Social signals are cached in the database and updated periodically
- **Batch Processing**: Update job processes repos in batches to avoid overwhelming APIs

### Use-Case Finder

- **LLM Costs**: Each query uses LLM API calls (costs apply)
- **Response Time**: LLM calls can take 2-5 seconds
- **Caching**: Consider caching common queries
- **Candidate Limit**: Currently limits to 50 candidate repos for LLM analysis

---

## Future Enhancements

### Social Signals
- [ ] Add Twitter/X API integration (requires API access)
- [ ] Add GitHub Discussions mentions
- [ ] Add Dev.to and Medium article mentions
- [ ] Historical trend tracking
- [ ] Social score predictions

### Use-Case Finder
- [ ] Support for multiple languages (JavaScript, Go, Rust, etc.)
- [ ] Learning path generation
- [ ] Comparison tables (lib1 vs lib2)
- [ ] Code examples for each recommendation
- [ ] User feedback loop (thumbs up/down)

---

## Troubleshooting

### Social Signals Not Updating

1. Check API rate limits (Reddit, HN, Stack Overflow)
2. Verify network connectivity
3. Check logs for API errors
4. Try updating a single repo first

### Use-Case Finder Returns Empty Results

1. Ensure you have Python repos with summaries in the database
2. Check LLM API key is configured
3. Verify LLM service is accessible
4. Check logs for LLM errors

### Import Errors

If you see import errors:
```bash
# Make sure you're in the repoboard directory
cd repoboard

# Check Python path
export PYTHONPATH="${PYTHONPATH}:$(pwd)"
```

---

## Contributing

To add new social signal sources or improve the use-case finder:

1. **Social Signals**: Add methods to `social-signals-service/social_fetcher.py`
2. **Use-Case Finder**: Modify prompts in `use-case-finder/use_case_matcher.py`

---

## License

Same as RepoBoard project.

