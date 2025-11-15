"""Fetch repositories and generate recommendations."""

import sys
import os
from typing import List, Dict, Any, Optional
from datetime import datetime

# Add parent directory to path (same as other jobs)
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, parent_dir)

from db.connection import get_db, init_db
from db.models import Repo, RepoLabel, RepoInsight, RepoSummary, CurationScore

# Import ingestion service (handle directory name with hyphen)
import importlib.util
ingestion_service_path = os.path.join(parent_dir, 'ingestion-service', 'ingester.py')
spec = importlib.util.spec_from_file_location("ingester", ingestion_service_path)
ingester_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(ingester_module)
RepoIngester = ingester_module.RepoIngester

# Advanced fetcher is optional
try:
    advanced_fetcher_path = os.path.join(parent_dir, 'ingestion-service', 'advanced_fetcher.py')
    spec2 = importlib.util.spec_from_file_location("advanced_fetcher", advanced_fetcher_path)
    advanced_fetcher_module = importlib.util.module_from_spec(spec2)
    spec2.loader.exec_module(advanced_fetcher_module)
    AdvancedRepoFetcher = advanced_fetcher_module.AdvancedRepoFetcher
except Exception:
    AdvancedRepoFetcher = None

from shared.config import settings


def fetch_repos_simple(limit: int = 50):
    """Fetch a small batch of repos to start with."""
    print("=" * 80)
    print("FETCHING REPOSITORIES")
    print("=" * 80)
    
    # Initialize database
    print("\n[1/3] Initializing database...")
    try:
        init_db()
        print("✅ Database initialized")
    except Exception as e:
        print(f"⚠️  Database init warning: {e}")
    
    # Fetch repos
    print(f"\n[2/3] Fetching {limit} trending repositories...")
    ingester = RepoIngester()
    
    try:
        repos = ingester.ingest_trending(limit=limit)
        print(f"✅ Fetched and ingested {len(repos)} repositories")
        return repos
    except Exception as e:
        print(f"❌ Error fetching repos: {e}")
        print("\nTrying alternative fetch method...")
        
        # Try advanced fetcher with smaller scope
        try:
            if AdvancedRepoFetcher is None:
                raise ImportError("AdvancedRepoFetcher not available")
            fetcher = AdvancedRepoFetcher()
            repos_data = fetcher.fetch_trending_recent(days=7, min_stars=100, limit=limit)
            
            ingested = []
            for repo_data in repos_data:
                try:
                    metadata = ingester.github_client.fetch_repo_metadata(repo_data)
                    with get_db() as db:
                        existing = db.query(Repo).filter(Repo.url == str(metadata.url)).first()
                        if existing:
                            for key, value in metadata.dict(exclude={"id", "created_at_db", "updated_at_db"}).items():
                                setattr(existing, key, value)
                            existing.updated_at_db = datetime.utcnow()
                            db.commit()
                            ingested.append(existing)
                        else:
                            repo = Repo(**metadata.dict(exclude={"id", "created_at_db", "updated_at_db"}))
                            db.add(repo)
                            db.commit()
                            db.refresh(repo)
                            ingested.append(repo)
                except Exception as e2:
                    print(f"  ⚠️  Error ingesting {repo_data.get('full_name', 'unknown')}: {e2}")
                    continue
            
            print(f"✅ Fetched and ingested {len(ingested)} repositories")
            return ingested
        except Exception as e2:
            print(f"❌ Error with advanced fetcher: {e2}")
            return []
    
    return []


def get_recommendations(
    category: Optional[str] = None,
    min_stars: int = 100,
    min_insightfulness: float = 0.5,
    limit: int = 10
) -> List[Dict[str, Any]]:
    """Get repository recommendations based on various criteria."""
    print("\n" + "=" * 80)
    print("GENERATING RECOMMENDATIONS")
    print("=" * 80)
    
    recommendations = []
    
    with get_db() as db:
        query = db.query(Repo).filter(
            Repo.archived == False,
            Repo.stars >= min_stars
        )
        
        # Filter by category if provided
        if category:
            query = query.join(RepoLabel).filter(
                RepoLabel.label_type == "category",
                RepoLabel.label_value.ilike(f"%{category}%")
            )
        
        repos = query.order_by(Repo.stars.desc()).limit(limit * 3).all()
        
        # Score and rank repos
        scored_repos = []
        for repo in repos:
            # Get insightfulness score
            insight = db.query(RepoInsight).filter(RepoInsight.repo_id == repo.id).first()
            insight_score = insight.total_insightfulness if insight else 0.0
            
            # Get curation score
            curation = db.query(CurationScore).filter(CurationScore.repo_id == repo.id).first()
            curation_score = curation.total_score if curation else 0.0
            
            # Get summary
            summary = db.query(RepoSummary).filter(RepoSummary.repo_id == repo.id).first()
            
            # Get labels
            labels = db.query(RepoLabel).filter(RepoLabel.repo_id == repo.id).all()
            label_dict = {}
            for label in labels:
                if label.label_type not in label_dict:
                    label_dict[label.label_type] = []
                label_dict[label.label_type].append(label.label_value)
            
            # Combined score (weighted)
            combined_score = (
                0.4 * (repo.stars / 10000.0) +  # Normalize stars
                0.3 * insight_score +
                0.3 * curation_score
            )
            
            scored_repos.append({
                "repo": repo,
                "summary": summary,
                "labels": label_dict,
                "insight_score": insight_score,
                "curation_score": curation_score,
                "combined_score": combined_score,
                "insight": insight
            })
        
        # Sort by combined score
        scored_repos.sort(key=lambda x: x["combined_score"], reverse=True)
        
        # Filter by min_insightfulness
        scored_repos = [r for r in scored_repos if r["insight_score"] >= min_insightfulness]
        
        # Format recommendations
        for i, item in enumerate(scored_repos[:limit], 1):
            repo = item["repo"]
            summary = item["summary"]
            labels = item["labels"]
            
            rec = {
                "rank": i,
                "name": repo.full_name,
                "url": repo.url,
                "description": repo.description or "No description",
                "stars": repo.stars,
                "forks": repo.forks,
                "languages": list(repo.languages.keys())[:3] if repo.languages else [],
                "topics": repo.topics[:5] if repo.topics else [],
                "summary": summary.summary[:200] if summary else None,
                "category": summary.category if summary else None,
                "labels": labels,
                "insightfulness": item["insight_score"],
                "curation_score": item["curation_score"],
                "combined_score": item["combined_score"],
                "why_recommended": _generate_recommendation_reason(item)
            }
            recommendations.append(rec)
    
    return recommendations


def _generate_recommendation_reason(item: Dict[str, Any]) -> str:
    """Generate a human-readable reason for recommendation."""
    reasons = []
    
    repo = item["repo"]
    insight = item["insight"]
    labels = item["labels"]
    
    # High stars
    if repo.stars > 1000:
        reasons.append(f"Highly popular ({repo.stars:,} stars)")
    elif repo.stars > 500:
        reasons.append(f"Popular ({repo.stars:,} stars)")
    
    # High insightfulness
    if item["insight_score"] > 0.7:
        reasons.append("Highly insightful")
    elif item["insight_score"] > 0.5:
        reasons.append("Insightful")
    
    # Discovery labels
    if "discovery" in labels:
        for label in labels["discovery"]:
            if label == "Hidden Gem":
                reasons.append("Hidden gem - high quality, low visibility")
            elif label == "Rising Star":
                reasons.append("Rising star - rapidly gaining traction")
            elif label == "Educational":
                reasons.append("Great for learning")
    
    # Quality labels
    if "quality_documentation" in labels:
        if "Excellent" in labels["quality_documentation"]:
            reasons.append("Excellent documentation")
    
    # Activity
    if repo.pushed_at:
        days_since = (datetime.now() - repo.pushed_at).days
        if days_since < 30:
            reasons.append("Recently updated")
    
    # Insight details
    if insight:
        if insight.innovation_score > 0.7:
            reasons.append("Innovative approach")
        if insight.best_practices_score > 0.7:
            reasons.append("Best practices example")
        if insight.production_use_score > 0.7:
            reasons.append("Production-ready")
    
    return "; ".join(reasons) if reasons else "Quality repository"


def print_recommendations(recommendations: List[Dict[str, Any]]):
    """Print recommendations in a nice format."""
    if not recommendations:
        print("\n❌ No recommendations found. Try fetching more repos first.")
        return
    
    print(f"\n📊 Found {len(recommendations)} recommendations:\n")
    
    for rec in recommendations:
        print("─" * 80)
        print(f"#{rec['rank']} {rec['name']}")
        print(f"   ⭐ {rec['stars']:,} stars | 🍴 {rec['forks']:,} forks")
        print(f"   🔗 {rec['url']}")
        print(f"   📝 {rec['description']}")
        
        if rec['languages']:
            print(f"   💻 Languages: {', '.join(rec['languages'])}")
        
        if rec['category']:
            print(f"   📂 Category: {rec['category']}")
        
        if rec['summary']:
            print(f"   📖 Summary: {rec['summary']}...")
        
        print(f"   🎯 Why recommended: {rec['why_recommended']}")
        print(f"   📊 Scores: Insightfulness={rec['insightfulness']:.2f}, Curation={rec['curation_score']:.2f}")
        print()


def main():
    """Main entry point."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Fetch repos and generate recommendations")
    parser.add_argument("--fetch", action="store_true", help="Fetch new repositories")
    parser.add_argument("--limit", type=int, default=50, help="Number of repos to fetch")
    parser.add_argument("--category", type=str, help="Filter by category")
    parser.add_argument("--min-stars", type=int, default=100, help="Minimum stars")
    parser.add_argument("--min-insight", type=float, default=0.3, help="Minimum insightfulness score")
    parser.add_argument("--recommend", type=int, default=10, help="Number of recommendations")
    
    args = parser.parse_args()
    
    # Fetch repos if requested
    if args.fetch:
        repos = fetch_repos_simple(limit=args.limit)
        if repos:
            print(f"\n✅ Successfully fetched {len(repos)} repositories!")
        else:
            print("\n⚠️  No repos fetched. Check your GitHub token and database connection.")
            return
    else:
        # Check if we have repos
        with get_db() as db:
            count = db.query(Repo).count()
            if count == 0:
                print("⚠️  No repositories in database. Run with --fetch first.")
                print("   Example: python jobs/fetch_and_recommend.py --fetch --limit 50")
                return
            else:
                print(f"📦 Found {count} repositories in database")
    
    # Get recommendations
    recommendations = get_recommendations(
        category=args.category,
        min_stars=args.min_stars,
        min_insightfulness=args.min_insight,
        limit=args.recommend
    )
    
    # Print recommendations
    print_recommendations(recommendations)
    
    # Save to file
    if recommendations:
        import json
        output_file = "recommendations.json"
        with open(output_file, "w") as f:
            json.dump(recommendations, f, indent=2, default=str)
        print(f"💾 Recommendations saved to {output_file}")


if __name__ == "__main__":
    main()

