"""Simple script to fetch repos and show recommendations - uses existing working jobs."""

import sys
import os
from typing import List, Dict, Any, Optional
from datetime import datetime
import subprocess

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from db.connection import get_db, init_db
from db.models import Repo, RepoLabel, RepoInsight, RepoSummary, CurationScore


def fetch_repos_via_job(limit: int = 20):
    """Fetch repos using the existing ingest_trending job."""
    print("=" * 80)
    print("FETCHING REPOSITORIES")
    print("=" * 80)
    
    # Initialize database
    print("\n[1/2] Initializing database...")
    try:
        init_db()
        print("✅ Database initialized")
    except Exception as e:
        print(f"⚠️  Database init: {e}")
    
    # Run the existing ingest job
    print(f"\n[2/2] Fetching {limit} repositories using ingest_trending job...")
    try:
        # Import and run the existing job
        from jobs.ingest_trending import main as ingest_main
        repos = ingest_main()
        print(f"✅ Fetched repositories")
        return repos
    except Exception as e:
        print(f"❌ Error: {e}")
        print("\n💡 Make sure you have:")
        print("   - Database running (PostgreSQL or Docker)")
        print("   - GITHUB_TOKEN set in .env (optional but recommended)")
        return []


def get_recommendations(
    category: Optional[str] = None,
    min_stars: int = 50,
    limit: int = 10
) -> List[Dict[str, Any]]:
    """Get repository recommendations."""
    print("\n" + "=" * 80)
    print("GENERATING RECOMMENDATIONS")
    print("=" * 80)
    
    recommendations = []
    
    with get_db() as db:
        # Check if we have repos
        repo_count = db.query(Repo).count()
        if repo_count == 0:
            print("\n⚠️  No repositories found in database.")
            print("   Run with --fetch first to fetch repositories.")
            return []
        
        print(f"\n📦 Found {repo_count} repositories in database")
        
        # Build query
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
        
        repos = query.order_by(Repo.stars.desc()).limit(limit * 2).all()
        
        # Score repos
        scored_repos = []
        for repo in repos:
            # Get scores
            insight = db.query(RepoInsight).filter(RepoInsight.repo_id == repo.id).first()
            curation = db.query(CurationScore).filter(CurationScore.repo_id == repo.id).first()
            summary = db.query(RepoSummary).filter(RepoSummary.repo_id == repo.id).first()
            
            # Get labels
            labels = db.query(RepoLabel).filter(RepoLabel.repo_id == repo.id).all()
            label_dict = {}
            for label in labels:
                if label.label_type not in label_dict:
                    label_dict[label.label_type] = []
                label_dict[label.label_type].append(label.label_value)
            
            # Calculate scores
            insight_score = insight.total_insightfulness if insight else 0.0
            curation_score = curation.total_score if curation else 0.0
            
            # Combined score
            combined_score = (
                0.5 * min(repo.stars / 1000.0, 1.0) +  # Normalize stars
                0.3 * insight_score +
                0.2 * curation_score
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
        
        # Sort and limit
        scored_repos.sort(key=lambda x: x["combined_score"], reverse=True)
        
        # Format recommendations
        for i, item in enumerate(scored_repos[:limit], 1):
            repo = item["repo"]
            summary = item["summary"]
            
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
                "insightfulness": item["insight_score"],
                "curation_score": item["curation_score"],
                "combined_score": item["combined_score"],
                "why_recommended": _generate_recommendation_reason(item)
            }
            recommendations.append(rec)
    
    return recommendations


def _generate_recommendation_reason(item: Dict[str, Any]) -> str:
    """Generate recommendation reason."""
    reasons = []
    repo = item["repo"]
    insight = item["insight"]
    
    if repo.stars > 1000:
        reasons.append(f"Highly popular ({repo.stars:,} stars)")
    elif repo.stars > 500:
        reasons.append(f"Popular ({repo.stars:,} stars)")
    
    if item["insight_score"] > 0.5:
        reasons.append("Insightful repository")
    
    if repo.pushed_at:
        days_since = (datetime.now() - repo.pushed_at).days
        if days_since < 30:
            reasons.append("Recently updated")
    
    if insight and insight.innovation_score > 0.6:
        reasons.append("Innovative")
    
    return "; ".join(reasons) if reasons else "Quality repository"


def print_recommendations(recommendations: List[Dict[str, Any]]):
    """Print recommendations."""
    if not recommendations:
        print("\n❌ No recommendations found.")
        return
    
    print(f"\n📊 Top {len(recommendations)} Recommendations:\n")
    
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
            print(f"   📖 {rec['summary']}...")
        
        print(f"   🎯 {rec['why_recommended']}")
        print(f"   📊 Score: {rec['combined_score']:.3f} (Insight: {rec['insightfulness']:.2f}, Curation: {rec['curation_score']:.2f})")
        print()


def main():
    """Main entry point."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Fetch repos and get recommendations")
    parser.add_argument("--fetch", action="store_true", help="Fetch new repositories")
    parser.add_argument("--limit", type=int, default=20, help="Number of repos to fetch")
    parser.add_argument("--category", type=str, help="Filter by category")
    parser.add_argument("--min-stars", type=int, default=50, help="Minimum stars")
    parser.add_argument("--recommend", type=int, default=10, help="Number of recommendations")
    
    args = parser.parse_args()
    
    # Fetch if requested
    if args.fetch:
        repos = fetch_repos_via_job(limit=args.limit)
        if repos:
            print(f"\n✅ Successfully processed repositories!")
        else:
            print("\n⚠️  Could not fetch repos. Check database and GitHub token.")
            return
    
    # Get recommendations
    recommendations = get_recommendations(
        category=args.category,
        min_stars=args.min_stars,
        limit=args.recommend
    )
    
    # Print
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

