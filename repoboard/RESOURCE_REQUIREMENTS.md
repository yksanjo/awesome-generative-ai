# RepoBoard Resource Requirements

## Infrastructure Overview

### Minimum Viable Setup (Testing/Development)

**For 100-500 repos, 10-20 boards:**

| Component | Resource | Cost |
|-----------|----------|------|
| **API Server** | 512MB RAM, 0.5 CPU | Free (Railway free tier) |
| **PostgreSQL** | 256MB storage | Free (Railway free tier) |
| **Qdrant** | 256MB RAM | Free (local or Railway) |
| **Frontend** | Static hosting | Free (Vercel/Netlify) |
| **LLM API** | Pay-per-use | $5-20/month (OpenAI) |
| **GitHub API** | Free tier | Free (5000 req/hour) |
| **Total** | | **$5-20/month** |

### Production Setup (1,000-10,000 repos)

**For active usage with 50-100 boards:**

| Component | Resource | Monthly Cost |
|-----------|----------|--------------|
| **API Server** | 2GB RAM, 2 CPU | $20-40 (Railway/Render) |
| **PostgreSQL** | 10GB storage | $15-25 (managed DB) |
| **Qdrant** | 1GB RAM | $10-15 (or self-hosted) |
| **Frontend** | CDN hosting | $0-5 (Vercel) |
| **LLM API** | ~10K requests | $50-200 (OpenAI) |
| **GitHub API** | Free tier | Free |
| **Redis Cache** | 256MB | $5-10 (optional) |
| **Total** | | **$100-300/month** |

### Enterprise Setup (10,000+ repos)

**For high-traffic, many users:**

| Component | Resource | Monthly Cost |
|-----------|----------|--------------|
| **API Servers** | 4GB RAM, 4 CPU (2x) | $80-150 |
| **PostgreSQL** | 100GB, read replicas | $100-200 |
| **Qdrant Cluster** | 4GB RAM | $50-100 |
| **CDN** | CloudFlare/CloudFront | $20-50 |
| **LLM API** | ~100K requests | $500-2000 |
| **Redis Cluster** | 2GB | $30-50 |
| **Monitoring** | Datadog/New Relic | $50-100 |
| **Total** | | **$800-2,500/month** |

## Cost Breakdown by Component

### 1. Compute (API Server)

**Options:**
- **Railway**: $5-20/month (pay-as-you-go)
- **Render**: $7-25/month (free tier available)
- **Fly.io**: $5-15/month (generous free tier)
- **DigitalOcean**: $12/month (Droplet)
- **AWS/GCP**: $15-30/month (EC2/Compute Engine)

**Recommendation:** Start with Railway/Render free tier, scale as needed.

### 2. Database (PostgreSQL)

**Options:**
- **Railway PostgreSQL**: $5-20/month
- **Render PostgreSQL**: $7-20/month (free tier)
- **Supabase**: Free tier, $25/month for production
- **Neon**: Free tier, $19/month for production
- **Self-hosted**: $5-10/month (VPS)

**Storage needs:**
- 1,000 repos: ~500MB
- 10,000 repos: ~5GB
- 100,000 repos: ~50GB

### 3. Vector Database (Qdrant)

**Options:**
- **Qdrant Cloud**: $25/month (starter)
- **Self-hosted**: $5-10/month (VPS)
- **Railway**: Included in compute

**Storage needs:**
- 1,000 repos: ~150MB (embeddings)
- 10,000 repos: ~1.5GB
- 100,000 repos: ~15GB

### 4. LLM API Costs

**OpenAI (GPT-4o-mini):**
- Summary generation: ~$0.001 per repo
- Board naming: ~$0.0005 per board
- **1,000 repos**: ~$1-2
- **10,000 repos**: ~$10-20
- **100,000 repos**: ~$100-200

**Anthropic (Claude Haiku):**
- Similar pricing to OpenAI
- Slightly cheaper for some tasks

**Ollama (Self-hosted):**
- **Free** (runs locally)
- Requires: 8GB+ RAM, GPU recommended
- Good for: Development, privacy-focused setups

**Recommendation:** Start with OpenAI GPT-4o-mini, consider Ollama for cost savings.

### 5. GitHub API

- **Free tier**: 5,000 requests/hour
- **Authenticated**: 5,000 requests/hour
- **Enterprise**: Higher limits
- **Cost**: Free for most use cases

### 6. Frontend Hosting

**Options:**
- **Vercel**: Free (generous limits)
- **Netlify**: Free (generous limits)
- **GitHub Pages**: Free
- **CloudFlare Pages**: Free

**Cost**: $0 for most setups

## Scaling Considerations

### Horizontal Scaling

**API Servers:**
- Stateless design allows easy scaling
- Load balancer: $10-20/month
- Multiple instances: Add $20-40 per instance

**Database:**
- Read replicas: $15-25 each
- Connection pooling: Built-in
- Caching layer (Redis): $5-10/month

### Vertical Scaling

**When to scale up:**
- CPU > 70% consistently
- Memory > 80% usage
- Response times > 500ms

**Cost impact:**
- 2x resources ≈ 2x cost
- Usually cheaper than horizontal scaling initially

## Cost Optimization Strategies

### 1. Use Free Tiers
- Railway/Render free tiers
- Vercel for frontend
- GitHub API free tier

### 2. Batch Processing
- Process repos in batches
- Cache LLM responses
- Reuse embeddings

### 3. Use Ollama for Development
- Free local LLM
- Only use paid APIs for production

### 4. Smart Caching
- Cache API responses
- Redis for frequently accessed data
- CDN for static assets

### 5. Optimize LLM Usage
- Batch requests when possible
- Use cheaper models (GPT-4o-mini)
- Cache summaries (don't regenerate)

## Resource Usage Estimates

### Per 1,000 Repositories

**Storage:**
- PostgreSQL: ~500MB
- Qdrant: ~150MB
- Total: ~650MB

**Compute:**
- API: Minimal (mostly I/O bound)
- Processing: CPU-intensive during ingestion
- Memory: ~512MB-1GB

**API Calls:**
- GitHub: ~1,000 requests (one-time)
- LLM: ~1,000 requests (one-time)
- Ongoing: Minimal (just updates)

### Per 10,000 Repositories

**Storage:**
- PostgreSQL: ~5GB
- Qdrant: ~1.5GB
- Total: ~6.5GB

**Compute:**
- API: 1-2GB RAM
- Processing: 2-4 CPU cores during ingestion
- Memory: ~2GB

## Recommended Starting Setup

### For Testing/Development
```
- Railway free tier (API + DB)
- Ollama (local LLM)
- Vercel (frontend)
- Local Qdrant (Docker)
Cost: $0/month
```

### For Production (Small Scale)
```
- Railway Pro ($20/month)
- OpenAI API ($10-20/month)
- Vercel (free)
- Qdrant Cloud ($25/month)
Cost: $55-65/month
```

### For Production (Medium Scale)
```
- Railway Pro ($40/month)
- Managed PostgreSQL ($20/month)
- OpenAI API ($50-100/month)
- Qdrant Cloud ($50/month)
- Redis ($10/month)
Cost: $170-220/month
```

## Monitoring & Alerts

**Free options:**
- Railway built-in metrics
- GitHub Actions for health checks
- UptimeRobot (free tier)

**Paid options:**
- Datadog: $15-31/month
- New Relic: $25/month
- Sentry: $26/month (error tracking)

## Summary

**Minimum to start:** $0-20/month (using free tiers)
**Production ready:** $100-300/month
**Enterprise scale:** $800-2,500/month

**Biggest costs:**
1. LLM API (if using OpenAI/Anthropic)
2. Database hosting
3. Compute resources

**Cost-saving tips:**
- Use Ollama for development
- Leverage free tiers
- Cache aggressively
- Batch process efficiently

