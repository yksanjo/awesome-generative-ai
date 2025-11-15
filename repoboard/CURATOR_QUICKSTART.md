# 🚀 Repo Curator Quick Start

This guide shows you how to use the comprehensive repository curation system to build a competitive repository curator.

## Overview

The curation system includes:
- **Advanced Fetching**: Multi-source repository discovery
- **Smart Labeling**: Multi-dimensional labeling system
- **Insightfulness Scoring**: Identify the most notable repos
- **Quality Filtering**: Ensure only high-quality repos are curated

## Quick Start

### 1. Initialize Database

```bash
cd repoboard
python -c "from db.connection import init_db; init_db()"
```

This creates all necessary tables including the new `repo_labels` and `repo_insights` tables.

### 2. Run Comprehensive Curation

```bash
python jobs/comprehensive_curation.py
```

This will:
1. Fetch repos from multiple sources (languages, topics, organizations, trending)
2. Ingest them into the database
3. Generate summaries (if needed)
4. Label them comprehensively
5. Calculate insightfulness scores
6. Rank all repositories

### 3. Customize Your Curation

Edit `jobs/comprehensive_curation.py` to customize:

```python
curator.run_comprehensive_curation(
    languages=["python", "javascript", "go"],  # Your target languages
    topics=["machine-learning", "web-development"],  # Your target topics
    per_category_limit=50,  # Repos per category (adjust for rate limits)
    use_llm_labeling=True  # Use LLM for better labels (or False for heuristics)
)
```

## Fetching Strategies

### Strategy 1: Language-Based Fetching

```python
from ingestion_service.advanced_fetcher import AdvancedRepoFetcher

fetcher = AdvancedRepoFetcher()
repos = fetcher.fetch_by_language("python", min_stars=100, limit=100)
```

### Strategy 2: Topic-Based Fetching

```python
repos = fetcher.fetch_by_topic("machine-learning", min_stars=50, limit=100)
```

### Strategy 3: Organization-Based Fetching

```python
repos = fetcher.fetch_by_organization("google", min_stars=100, limit=200)
```

### Strategy 4: Trending Repos

```python
repos = fetcher.fetch_trending_recent(days=7, min_stars=50, limit=200)
```

### Strategy 5: Rising Stars

```python
repos = fetcher.fetch_rising_stars(min_star_velocity=5.0, limit=100)
```

### Strategy 6: Comprehensive Fetch

```python
repos = fetcher.comprehensive_fetch(
    languages=["python", "javascript"],
    topics=["machine-learning", "web-development"],
    orgs=["google", "facebook"],
    include_trending=True,
    include_updated=True,
    include_rising=True,
    per_category_limit=50
)
```

## Labeling System

### View Labels for a Repo

```python
from db.connection import get_db
from db.models import Repo, RepoLabel

with get_db() as db:
    repo = db.query(Repo).filter(Repo.full_name == "owner/repo").first()
    labels = db.query(RepoLabel).filter(RepoLabel.repo_id == repo.id).all()
    
    for label in labels:
        print(f"{label.label_type}: {label.label_value} (confidence: {label.confidence})")
```

### Label Types

- **category**: Primary categories (AI/ML, Web Development, etc.)
- **quality_***: Quality indicators (star_quality, documentation, maintenance, etc.)
- **technical_***: Technical labels (languages, frameworks, platform, etc.)
- **community_***: Community metrics (size, activity)
- **discovery**: Discovery labels (Hidden Gem, Rising Star, etc.)

## Insightfulness Scoring

### View Insightfulness Scores

```python
from db.models import RepoInsight

with get_db() as db:
    insight = db.query(RepoInsight).filter(RepoInsight.repo_id == repo.id).first()
    if insight:
        print(f"Total Insightfulness: {insight.total_insightfulness:.3f}")
        print(f"  Innovation: {insight.innovation_score:.3f}")
        print(f"  Best Practices: {insight.best_practices_score:.3f}")
        print(f"  Educational Value: {insight.educational_value:.3f}")
        print(f"  Production Use: {insight.production_use_score:.3f}")
        print(f"  Community Impact: {insight.community_impact:.3f}")
        print(f"  Technical Depth: {insight.technical_depth:.3f}")
```

## Quality Filtering

### Filter High-Quality Repos

```python
from db.models import Repo, RepoLabel, RepoInsight, CurationScore

with get_db() as db:
    # Get repos with high insightfulness
    high_insight = db.query(Repo).join(RepoInsight).filter(
        RepoInsight.total_insightfulness > 0.7
    ).all()
    
    # Get repos with high curation scores
    top_curated = db.query(Repo).join(CurationScore).filter(
        CurationScore.total_score > 0.7
    ).order_by(CurationScore.total_score.desc()).limit(100).all()
    
    # Get hidden gems (high quality, low visibility)
    hidden_gems = db.query(Repo).join(RepoLabel).filter(
        RepoLabel.label_type == "discovery",
        RepoLabel.label_value == "Hidden Gem",
        Repo.stars < 500
    ).all()
```

## Competitive Features

### 1. Export to Awesome List Format

```bash
python scripts/export_awesome_list.py --combined
```

### 2. Find Similar Repos

Use the embedding service for semantic search (already integrated).

### 3. Generate Curated Boards

```bash
python jobs/generate_boards.py
```

## Scheduled Curation

Set up a cron job for regular updates:

```bash
# Daily curation (runs at 2 AM)
0 2 * * * cd /path/to/repoboard && source venv/bin/activate && python jobs/comprehensive_curation.py
```

## Rate Limit Management

### Multiple GitHub Tokens

Set multiple tokens in your environment:

```bash
export GITHUB_TOKEN_1=token1
export GITHUB_TOKEN_2=token2
# ... etc
```

Modify `github_client.py` to rotate tokens.

### Caching Strategy

The system automatically tracks fetched repos to avoid duplicates. For better caching:

1. Only fetch repos updated since last run
2. Use GitHub's conditional requests (ETags)
3. Cache API responses

## Best Practices

1. **Start Small**: Begin with 1-2 languages and 5-10 topics
2. **Monitor Rate Limits**: Watch your GitHub API usage
3. **Quality Over Quantity**: Focus on high-quality repos
4. **Regular Updates**: Run curation weekly or daily
5. **Review Labels**: Periodically review and validate labels
6. **Track Metrics**: Monitor insightfulness and curation scores

## Troubleshooting

### Rate Limit Errors

- Reduce `per_category_limit`
- Add delays between requests
- Use multiple GitHub tokens
- Run during off-peak hours

### LLM API Errors

- Set `use_llm_labeling=False` to use heuristics
- Check your API key
- Monitor API usage and costs

### Database Errors

- Ensure database is initialized: `init_db()`
- Check database connection string
- Verify all migrations are applied

## Next Steps

1. Read [REPO_CURATOR_GUIDE.md](REPO_CURATOR_GUIDE.md) for detailed strategies
2. Customize fetching strategies for your use case
3. Set up scheduled curation jobs
4. Build your competitive features
5. Share your curated lists!

## Example: Building a Competitive ML Repo Curator

```python
from jobs.comprehensive_curation import ComprehensiveCurator

curator = ComprehensiveCurator()

# Focus on ML/AI repos
curator.run_comprehensive_curation(
    languages=["python"],  # Most ML repos are Python
    topics=[
        "machine-learning",
        "deep-learning",
        "artificial-intelligence",
        "neural-network",
        "pytorch",
        "tensorflow"
    ],
    per_category_limit=100,
    use_llm_labeling=True
)

# Export to awesome list
from scripts.export_awesome_list import export_combined_awesome_list
export_combined_awesome_list("AWESOME_ML.md")
```

This creates a comprehensive, competitive ML repository curator!

