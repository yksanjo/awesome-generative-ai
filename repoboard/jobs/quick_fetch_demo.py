"""Quick demo: Fetch repos and show recommendations without full database setup."""

import os
import requests
import json
from typing import List, Dict, Any, Optional
from datetime import datetime


def fetch_trending_repos(limit: int = 20, github_token: Optional[str] = None) -> List[Dict[str, Any]]:
    """Fetch trending repos directly from GitHub API."""
    print("=" * 80)
    print("FETCHING TRENDING REPOSITORIES FROM GITHUB")
    print("=" * 80)
    
    headers = {
        "Accept": "application/vnd.github.v3+json",
    }
    if github_token:
        headers["Authorization"] = f"token {github_token}"
    
    # Fetch trending repos (by stars, recently updated)
    url = "https://api.github.com/search/repositories"
    params = {
        "q": "stars:>100 pushed:>2024-01-01",
        "sort": "stars",
        "order": "desc",
        "per_page": min(limit, 100)
    }
    
    try:
        print(f"\n📡 Fetching top {limit} repositories...")
        response = requests.get(url, headers=headers, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        repos = data.get("items", [])
        print(f"✅ Fetched {len(repos)} repositories\n")
        return repos
    except Exception as e:
        print(f"❌ Error fetching repos: {e}")
        if "rate limit" in str(e).lower():
            print("💡 Tip: Set GITHUB_TOKEN in environment to increase rate limit")
        return []


def analyze_and_recommend(repos: List[Dict[str, Any]], limit: int = 10) -> List[Dict[str, Any]]:
    """Analyze repos and generate recommendations."""
    print("=" * 80)
    print("ANALYZING & GENERATING RECOMMENDATIONS")
    print("=" * 80)
    
    scored_repos = []
    
    for repo in repos:
        # Calculate scores
        stars = repo.get("stargazers_count", 0)
        forks = repo.get("forks_count", 0)
        watchers = repo.get("watchers_count", 0)
        open_issues = repo.get("open_issues_count", 0)
        
        # Star velocity (rough estimate)
        created_at = datetime.fromisoformat(repo.get("created_at", "").replace("Z", "+00:00"))
        days_old = (datetime.now(created_at.tzinfo) - created_at).days or 1
        star_velocity = stars / days_old
        
        # Quality indicators
        has_readme = repo.get("has_wiki", False) or repo.get("has_pages", False)
        has_license = repo.get("license") is not None
        is_archived = repo.get("archived", False)
        is_disabled = repo.get("disabled", False)
        
        # Activity score
        updated_at = datetime.fromisoformat(repo.get("updated_at", "").replace("Z", "+00:00"))
        days_since_update = (datetime.now(updated_at.tzinfo) - updated_at).days
        activity_score = max(0, 1.0 - (days_since_update / 365.0))
        
        # Combined score
        popularity_score = min(stars / 10000.0, 1.0)  # Normalize to 0-1
        velocity_score = min(star_velocity / 50.0, 1.0)  # Normalize
        quality_score = (0.3 if has_readme else 0) + (0.2 if has_license else 0) + (0.5 if not is_archived else 0)
        
        combined_score = (
            0.4 * popularity_score +
            0.3 * velocity_score +
            0.2 * activity_score +
            0.1 * quality_score
        )
        
        # Determine why it's recommended
        reasons = []
        if stars > 1000:
            reasons.append(f"Highly popular ({stars:,} stars)")
        elif stars > 500:
            reasons.append(f"Popular ({stars:,} stars)")
        
        if star_velocity > 10:
            reasons.append("Rising star (fast growth)")
        
        if days_since_update < 30:
            reasons.append("Recently updated")
        
        if has_license:
            reasons.append("Has license")
        
        if not is_archived:
            reasons.append("Active project")
        
        scored_repos.append({
            "repo": repo,
            "score": combined_score,
            "popularity": popularity_score,
            "velocity": velocity_score,
            "activity": activity_score,
            "quality": quality_score,
            "reasons": reasons,
            "star_velocity": star_velocity
        })
    
    # Sort by score
    scored_repos.sort(key=lambda x: x["score"], reverse=True)
    
    # Format recommendations
    recommendations = []
    for i, item in enumerate(scored_repos[:limit], 1):
        repo = item["repo"]
        rec = {
            "rank": i,
            "name": repo.get("full_name", "Unknown"),
            "url": repo.get("html_url", ""),
            "description": repo.get("description", "No description"),
            "stars": repo.get("stargazers_count", 0),
            "forks": repo.get("forks_count", 0),
            "language": repo.get("language", "N/A"),
            "topics": repo.get("topics", [])[:5],
            "created_at": repo.get("created_at", ""),
            "updated_at": repo.get("updated_at", ""),
            "score": item["score"],
            "star_velocity": item["star_velocity"],
            "why_recommended": "; ".join(item["reasons"]) or "Quality repository"
        }
        recommendations.append(rec)
    
    return recommendations


def print_recommendations(recommendations: List[Dict[str, Any]]):
    """Print recommendations in a nice format."""
    if not recommendations:
        print("\n❌ No recommendations found.")
        return
    
    print(f"\n📊 Top {len(recommendations)} Recommended Repositories:\n")
    
    for rec in recommendations:
        print("─" * 80)
        print(f"#{rec['rank']} {rec['name']}")
        print(f"   ⭐ {rec['stars']:,} stars | 🍴 {rec['forks']:,} forks | 💻 {rec['language']}")
        print(f"   🔗 {rec['url']}")
        print(f"   📝 {rec['description']}")
        
        if rec['topics']:
            print(f"   🏷️  Topics: {', '.join(rec['topics'])}")
        
        print(f"   🎯 Why recommended: {rec['why_recommended']}")
        print(f"   📊 Score: {rec['score']:.3f} | Star velocity: {rec['star_velocity']:.1f} stars/day")
        print()


def main():
    """Main entry point."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Quick fetch and recommend repos")
    parser.add_argument("--limit", type=int, default=20, help="Number of repos to fetch")
    parser.add_argument("--recommend", type=int, default=10, help="Number of recommendations")
    parser.add_argument("--token", type=str, help="GitHub token (or set GITHUB_TOKEN env var)")
    
    args = parser.parse_args()
    
    # Get GitHub token
    github_token = args.token or os.getenv("GITHUB_TOKEN")
    
    # Fetch repos
    repos = fetch_trending_repos(limit=args.limit, github_token=github_token)
    
    if not repos:
        print("\n❌ Could not fetch repositories.")
        if not github_token:
            print("💡 Tip: Set GITHUB_TOKEN environment variable for better rate limits")
        return
    
    # Analyze and recommend
    recommendations = analyze_and_recommend(repos, limit=args.recommend)
    
    # Print
    print_recommendations(recommendations)
    
    # Save to file
    if recommendations:
        output_file = "recommendations.json"
        with open(output_file, "w") as f:
            json.dump(recommendations, f, indent=2, default=str)
        print(f"💾 Recommendations saved to {output_file}")
        
        # Also save as markdown
        md_file = "recommendations.md"
        with open(md_file, "w") as f:
            f.write("# Repository Recommendations\n\n")
            f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            for rec in recommendations:
                f.write(f"## {rec['rank']}. {rec['name']}\n\n")
                f.write(f"- **Stars**: {rec['stars']:,} | **Forks**: {rec['forks']:,} | **Language**: {rec['language']}\n")
                f.write(f"- **URL**: {rec['url']}\n")
                f.write(f"- **Description**: {rec['description']}\n")
                f.write(f"- **Why recommended**: {rec['why_recommended']}\n")
                f.write(f"- **Score**: {rec['score']:.3f}\n\n")
        print(f"📄 Recommendations also saved to {md_file}")


if __name__ == "__main__":
    main()

