"""Advanced recommendation engine with multiple recommendation types."""

import json
import os
from typing import List, Dict, Any, Optional
from datetime import datetime
from collections import defaultdict


class AdvancedRecommendationEngine:
    """Advanced recommendation engine with multiple strategies."""
    
    def __init__(self, repos: List[Dict[str, Any]]):
        self.repos = repos
        self._analyze_repos()
    
    def _analyze_repos(self):
        """Pre-analyze all repos for faster recommendations."""
        self.analyzed = []
        
        for repo in self.repos:
            stars = repo.get("stargazers_count", 0)
            forks = repo.get("forks_count", 0)
            watchers = repo.get("watchers_count", 0)
            
            # Calculate metrics
            created_at = datetime.fromisoformat(repo.get("created_at", "").replace("Z", "+00:00"))
            days_old = (datetime.now(created_at.tzinfo) - created_at).days or 1
            star_velocity = stars / days_old
            
            updated_at = datetime.fromisoformat(repo.get("updated_at", "").replace("Z", "+00:00"))
            days_since_update = (datetime.now(updated_at.tzinfo) - updated_at).days
            
            # Quality indicators
            has_license = repo.get("license") is not None
            has_wiki = repo.get("has_wiki", False)
            has_pages = repo.get("has_pages", False)
            has_description = bool(repo.get("description"))
            has_topics = len(repo.get("topics", [])) > 0
            is_archived = repo.get("archived", False)
            
            quality_score = (
                (0.2 if has_license else 0) +
                (0.2 if has_wiki or has_pages else 0) +
                (0.2 if has_description else 0) +
                (0.2 if has_topics else 0) +
                (0.2 if not is_archived else 0)
            )
            
            activity_score = max(0, 1.0 - (days_since_update / 365.0))
            popularity_score = min(stars / 10000.0, 1.0)
            velocity_score = min(star_velocity / 50.0, 1.0)
            
            combined_score = (
                0.3 * popularity_score +
                0.25 * velocity_score +
                0.25 * activity_score +
                0.2 * quality_score
            )
            
            self.analyzed.append({
                "repo": repo,
                "stars": stars,
                "forks": forks,
                "language": repo.get("language"),
                "topics": repo.get("topics", []),
                "star_velocity": star_velocity,
                "days_old": days_old,
                "days_since_update": days_since_update,
                "quality_score": quality_score,
                "activity_score": activity_score,
                "popularity_score": popularity_score,
                "velocity_score": velocity_score,
                "combined_score": combined_score,
                "is_archived": is_archived,
                "has_license": has_license
            })
    
    def recommend_top_overall(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Recommend top repos overall."""
        sorted_repos = sorted(self.analyzed, key=lambda x: x["combined_score"], reverse=True)
        return self._format_recommendations(sorted_repos[:limit], "Top Overall")
    
    def recommend_by_language(self, language: str, limit: int = 10) -> List[Dict[str, Any]]:
        """Recommend top repos by language."""
        lang_repos = [r for r in self.analyzed if r["language"] == language]
        sorted_repos = sorted(lang_repos, key=lambda x: x["combined_score"], reverse=True)
        return self._format_recommendations(sorted_repos[:limit], f"Top {language}")
    
    def recommend_rising_stars(self, min_velocity: float = 5.0, limit: int = 10) -> List[Dict[str, Any]]:
        """Recommend rising stars (high velocity)."""
        rising = [r for r in self.analyzed if r["star_velocity"] >= min_velocity and not r["is_archived"]]
        sorted_repos = sorted(rising, key=lambda x: x["star_velocity"], reverse=True)
        return self._format_recommendations(sorted_repos[:limit], "Rising Stars")
    
    def recommend_hidden_gems(self, max_stars: int = 500, min_quality: float = 0.7, limit: int = 10) -> List[Dict[str, Any]]:
        """Recommend hidden gems (high quality, low visibility)."""
        gems = [
            r for r in self.analyzed
            if r["stars"] <= max_stars
            and r["quality_score"] >= min_quality
            and not r["is_archived"]
        ]
        sorted_repos = sorted(gems, key=lambda x: x["quality_score"], reverse=True)
        return self._format_recommendations(sorted_repos[:limit], "Hidden Gems")
    
    def recommend_recently_updated(self, max_days: int = 30, limit: int = 10) -> List[Dict[str, Any]]:
        """Recommend recently updated repos."""
        recent = [r for r in self.analyzed if r["days_since_update"] <= max_days and not r["is_archived"]]
        sorted_repos = sorted(recent, key=lambda x: (x["combined_score"], -x["days_since_update"]), reverse=True)
        return self._format_recommendations(sorted_repos[:limit], "Recently Updated")
    
    def recommend_by_topic(self, topic: str, limit: int = 10) -> List[Dict[str, Any]]:
        """Recommend repos by topic."""
        topic_repos = [
            r for r in self.analyzed
            if topic.lower() in [t.lower() for t in r["topics"]]
        ]
        sorted_repos = sorted(topic_repos, key=lambda x: x["combined_score"], reverse=True)
        return self._format_recommendations(sorted_repos[:limit], f"Topic: {topic}")
    
    def recommend_educational(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Recommend educational repos."""
        educational_keywords = ["learn", "tutorial", "guide", "course", "education", "book", "awesome"]
        educational = []
        for r in self.analyzed:
            repo = r["repo"]
            description = (repo.get("description") or "").lower()
            name = (repo.get("name") or "").lower()
            topics = [t.lower() for t in r["topics"]]
            
            if any(
                keyword in description
                or keyword in name
                or any(keyword in t for t in topics)
                for keyword in educational_keywords
            ):
                educational.append(r)
        sorted_repos = sorted(educational, key=lambda x: x["combined_score"], reverse=True)
        return self._format_recommendations(sorted_repos[:limit], "Educational")
    
    def recommend_production_ready(self, min_stars: int = 1000, limit: int = 10) -> List[Dict[str, Any]]:
        """Recommend production-ready repos."""
        production = [
            r for r in self.analyzed
            if r["stars"] >= min_stars
            and r["has_license"]
            and r["quality_score"] >= 0.7
            and not r["is_archived"]
            and r["days_since_update"] < 90
        ]
        sorted_repos = sorted(production, key=lambda x: x["combined_score"], reverse=True)
        return self._format_recommendations(sorted_repos[:limit], "Production Ready")
    
    def recommend_by_organization(self, org: str, limit: int = 10) -> List[Dict[str, Any]]:
        """Recommend repos from an organization."""
        org_repos = [
            r for r in self.analyzed
            if r["repo"].get("owner", {}).get("login", "").lower() == org.lower()
        ]
        sorted_repos = sorted(org_repos, key=lambda x: x["combined_score"], reverse=True)
        return self._format_recommendations(sorted_repos[:limit], f"Organization: {org}")
    
    def _format_recommendations(self, repos: List[Dict[str, Any]], category: str) -> List[Dict[str, Any]]:
        """Format recommendations."""
        recommendations = []
        for i, item in enumerate(repos, 1):
            repo = item["repo"]
            rec = {
                "rank": i,
                "category": category,
                "name": repo.get("full_name", "Unknown"),
                "url": repo.get("html_url", ""),
                "description": repo.get("description", "No description"),
                "stars": item["stars"],
                "forks": item["forks"],
                "language": item["language"],
                "topics": item["topics"][:5],
                "score": item["combined_score"],
                "star_velocity": item["star_velocity"],
                "quality_score": item["quality_score"],
                "activity_score": item["activity_score"],
                "why_recommended": self._generate_reason(item)
            }
            recommendations.append(rec)
        return recommendations
    
    def _generate_reason(self, item: Dict[str, Any]) -> str:
        """Generate recommendation reason."""
        reasons = []
        
        if item["stars"] > 1000:
            reasons.append(f"Highly popular ({item['stars']:,} stars)")
        elif item["stars"] > 500:
            reasons.append(f"Popular ({item['stars']:,} stars)")
        
        if item["star_velocity"] > 10:
            reasons.append("Rising star")
        
        if item["days_since_update"] < 30:
            reasons.append("Recently updated")
        
        if item["quality_score"] > 0.8:
            reasons.append("High quality")
        
        if item["has_license"]:
            reasons.append("Has license")
        
        return "; ".join(reasons) if reasons else "Quality repository"
    
    def get_all_recommendations(self, limit_per_category: int = 10) -> Dict[str, List[Dict[str, Any]]]:
        """Get all recommendation types."""
        return {
            "top_overall": self.recommend_top_overall(limit_per_category),
            "rising_stars": self.recommend_rising_stars(limit=limit_per_category),
            "hidden_gems": self.recommend_hidden_gems(limit=limit_per_category),
            "recently_updated": self.recommend_recently_updated(limit=limit_per_category),
            "educational": self.recommend_educational(limit=limit_per_category),
            "production_ready": self.recommend_production_ready(limit=limit_per_category)
        }
    
    def get_language_recommendations(self, languages: List[str], limit: int = 10) -> Dict[str, List[Dict[str, Any]]]:
        """Get recommendations by language."""
        return {
            lang: self.recommend_by_language(lang, limit)
            for lang in languages
        }
    
    def get_topic_recommendations(self, topics: List[str], limit: int = 10) -> Dict[str, List[Dict[str, Any]]]:
        """Get recommendations by topic."""
        return {
            topic: self.recommend_by_topic(topic, limit)
            for topic in topics
        }


def main():
    """Example usage."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Advanced recommendation engine")
    parser.add_argument("--input", type=str, required=True, help="Input JSON file with repos")
    parser.add_argument("--output", type=str, default="recommendations.json", help="Output file")
    parser.add_argument("--limit", type=int, default=10, help="Recommendations per category")
    parser.add_argument("--languages", nargs="+", help="Languages to recommend")
    parser.add_argument("--topics", nargs="+", help="Topics to recommend")
    parser.add_argument("--all", action="store_true", help="Generate all recommendation types")
    
    args = parser.parse_args()
    
    # Load repos
    with open(args.input, "r") as f:
        repos = json.load(f)
    
    print(f"📦 Loaded {len(repos)} repositories")
    
    # Create engine
    engine = AdvancedRecommendationEngine(repos)
    
    # Generate recommendations
    all_recs = {}
    
    if args.all:
        print("\n🔍 Generating all recommendation types...")
        all_recs = engine.get_all_recommendations(limit_per_category=args.limit)
    
    if args.languages:
        print(f"\n🔍 Generating language recommendations: {', '.join(args.languages)}")
        lang_recs = engine.get_language_recommendations(args.languages, limit=args.limit)
        all_recs.update(lang_recs)
    
    if args.topics:
        print(f"\n🔍 Generating topic recommendations: {', '.join(args.topics)}")
        topic_recs = engine.get_topic_recommendations(args.topics, limit=args.limit)
        all_recs.update(topic_recs)
    
    if not all_recs:
        # Default: top overall
        all_recs = {"top_overall": engine.recommend_top_overall(args.limit)}
    
    # Save
    with open(args.output, "w") as f:
        json.dump(all_recs, f, indent=2, default=str)
    
    # Print summary
    print("\n" + "=" * 80)
    print("RECOMMENDATIONS SUMMARY")
    print("=" * 80)
    for category, recs in all_recs.items():
        print(f"\n{category}: {len(recs)} recommendations")
        for rec in recs[:3]:
            print(f"  - {rec['name']} ({rec['stars']:,} stars)")
    
    print(f"\n💾 Saved to {args.output}")


if __name__ == "__main__":
    main()

