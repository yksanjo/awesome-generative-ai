# RepoBoard for Personal Research & Awesome Lists

## Simplified Setup for Personal Use

This guide shows you how to use RepoBoard as a personal curation tool to create awesome-style GitHub lists.

## Why This Approach?

✅ **Ultra Low Cost** - $5-30/month  
✅ **Full Control** - Your curation, your rules  
✅ **Immediate Value** - Create awesome lists people love  
✅ **No Maintenance Burden** - Just for you  
✅ **Portfolio Piece** - Shows your curation skills  

## Minimal Setup

### 1. Local Development (Free)

```bash
# Use your computer - no hosting needed
cd repoboard
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Use SQLite instead of PostgreSQL (simpler)
# Modify db/connection.py to use SQLite
```

### 2. Or Small VPS ($5-10/month)

```bash
# DigitalOcean Droplet or similar
# 1GB RAM, 1 CPU is enough
docker-compose up -d
```

### 3. Configure

```bash
cp .env.example .env
# Edit .env:
# - LLM_PROVIDER=openai (or ollama for free)
# - OPENAI_API_KEY=your_key
# - DATABASE_URL=sqlite:///repoboard.db (for local)
```

## Workflow

### Weekly Curation Process

```bash
# 1. Ingest trending repos (weekly)
python jobs/ingest_trending.py --limit 100

# 2. Process repos (generate summaries)
python jobs/process_repos.py

# 3. Generate boards
python jobs/generate_boards.py

# 4. Export to markdown
python scripts/export_awesome_list.py --combined

# 5. Push to GitHub
git add AWESOME.md
git commit -m "Update curated list - $(date +%Y-%m-%d)"
git push
```

### Automated (Cron Job)

```bash
# Add to crontab (crontab -e)
0 2 * * 0 cd /path/to/repoboard && \
  source venv/bin/activate && \
  python jobs/ingest_trending.py && \
  python jobs/process_repos.py && \
  python jobs/generate_boards.py && \
  python scripts/export_awesome_list.py --combined && \
  cd /path/to/awesome-list-repo && \
  git add . && git commit -m "Auto-update $(date +%Y-%m-%d)" && git push
```

## Output Examples

### Single Board Export

```markdown
# Machine Learning Tools

Curated collection of ML tools and frameworks.

*Auto-curated by RepoBoard - Last updated: 2024-01-15*

---

- [scikit-learn/scikit-learn](https://github.com/scikit-learn/scikit-learn) - Machine learning library for Python `python, ml, sklearn` ⭐ 58000 | Python
- [tensorflow/tensorflow](https://github.com/tensorflow/tensorflow) - Open source machine learning framework `tensorflow, ml, deep-learning` ⭐ 180000 | C++
...
```

### Combined Awesome List

```markdown
# Awesome Curated Repositories

*Auto-curated by RepoBoard - Last updated: 2024-01-15*

## Machine Learning

### ML Frameworks
- [scikit-learn/scikit-learn](https://github.com/...) - Machine learning library ⭐ 58000
...

### Deep Learning
- [tensorflow/tensorflow](https://github.com/...) - ML framework ⭐ 180000
...
```

## Cost Breakdown

### Option A: Fully Local (Free)

```
- Your computer: $0
- Ollama (local LLM): $0
- SQLite database: $0
- GitHub Pages: $0
Total: $0/month
```

### Option B: Small VPS ($5-10/month)

```
- VPS: $5-10/month
- OpenAI API: $5-20/month (pay per use)
- Total: $10-30/month
```

### Option C: Cloud Free Tiers

```
- Railway free tier: $0
- OpenAI API: $5-20/month
- Total: $5-20/month
```

## Publishing Your Lists

### 1. Create GitHub Repo

```bash
# Create new repo: awesome-your-topic
git init
git add AWESOME.md README.md
git commit -m "Initial awesome list"
git remote add origin https://github.com/yourusername/awesome-your-topic.git
git push -u origin main
```

### 2. Add README

```markdown
# Awesome Your Topic

Curated list of [topic] repositories, automatically updated weekly.

## How It's Curated

This list is automatically generated using [RepoBoard](https://github.com/yksanjo/repoboard), 
an AI-powered GitHub repository curation tool.

## Categories

- [Category 1](#category-1)
- [Category 2](#category-2)
...

See [AWESOME.md](AWESOME.md) for the full list.
```

### 3. Enable GitHub Pages (Optional)

- Settings → Pages
- Source: Deploy from branch
- Branch: main
- Your list will be at: `https://yourusername.github.io/awesome-your-topic/`

## Example Use Cases

### 1. Research Curation

```bash
# Curate repos for your research area
python jobs/ingest_trending.py --language python --limit 200
python jobs/process_repos.py
python jobs/generate_boards.py
python scripts/export_awesome_list.py --combined
# Publish as: awesome-python-research
```

### 2. Learning Path

```bash
# Curate beginner-friendly repos
# Filter by skill_level=beginner
# Export as: awesome-learn-python
```

### 3. Industry Focus

```bash
# Curate repos for specific industry
# Filter by category
# Export as: awesome-fintech-tools
```

## Benefits vs Public Release

| Aspect | Personal Use | Public Release |
|--------|--------------|----------------|
| **Cost** | $0-30/month | $20-40/month (you) |
| **Time** | 1-2 hrs/week | 2-5 hrs/week |
| **Support** | None | High |
| **Value** | Your research | Community |
| **Risk** | Low | Medium |

## Next Steps

1. **Set up locally** - Use your computer or small VPS
2. **Run first curation** - Ingest and process repos
3. **Export list** - Generate markdown
4. **Publish** - Create GitHub repo
5. **Automate** - Set up weekly cron job
6. **Share** - Post on Twitter, Reddit, etc.

## When to Consider Public Release

Consider open-sourcing the tool when:
- ✅ Your lists are popular (100+ stars)
- ✅ People ask "how did you curate this?"
- ✅ You have time for maintenance
- ✅ You want community contributions

Until then, enjoy the low-cost, high-value personal curation tool!

