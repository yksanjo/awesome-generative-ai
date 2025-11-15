"""Analyze and generate insights about fetched repositories."""

import json
from typing import List, Dict, Any
from collections import defaultdict, Counter
from datetime import datetime


class RepoAnalyzer:
    """Analyze repositories and generate insights."""
    
    def __init__(self, repos: List[Dict[str, Any]]):
        self.repos = repos
        self.analysis = {}
    
    def analyze(self) -> Dict[str, Any]:
        """Run all analyses."""
        print("=" * 80)
        print("REPOSITORY ANALYSIS")
        print("=" * 80)
        
        self.analysis = {
            "summary": self._analyze_summary(),
            "languages": self._analyze_languages(),
            "topics": self._analyze_topics(),
            "organizations": self._analyze_organizations(),
            "trends": self._analyze_trends(),
            "quality": self._analyze_quality(),
            "activity": self._analyze_activity(),
            "insights": self._generate_insights()
        }
        
        return self.analysis
    
    def _analyze_summary(self) -> Dict[str, Any]:
        """Basic summary statistics."""
        print("\n📊 Analyzing summary statistics...")
        
        total_stars = sum(r.get("stargazers_count", 0) for r in self.repos)
        total_forks = sum(r.get("forks_count", 0) for r in self.repos)
        avg_stars = total_stars / len(self.repos) if self.repos else 0
        avg_forks = total_forks / len(self.repos) if self.repos else 0
        
        return {
            "total_repos": len(self.repos),
            "total_stars": total_stars,
            "total_forks": total_forks,
            "avg_stars": round(avg_stars, 2),
            "avg_forks": round(avg_forks, 2),
            "max_stars": max((r.get("stargazers_count", 0) for r in self.repos), default=0),
            "min_stars": min((r.get("stargazers_count", 0) for r in self.repos), default=0)
        }
    
    def _analyze_languages(self) -> Dict[str, Any]:
        """Analyze programming languages."""
        print("  💻 Analyzing languages...")
        
        languages = Counter(r.get("language") for r in self.repos if r.get("language"))
        lang_stars = defaultdict(int)
        
        for repo in self.repos:
            lang = repo.get("language")
            if lang:
                lang_stars[lang] += repo.get("stargazers_count", 0)
        
        return {
            "top_languages": dict(languages.most_common(10)),
            "language_stars": dict(sorted(lang_stars.items(), key=lambda x: x[1], reverse=True)[:10])
        }
    
    def _analyze_topics(self) -> Dict[str, Any]:
        """Analyze GitHub topics."""
        print("  🏷️  Analyzing topics...")
        
        all_topics = []
        for repo in self.repos:
            all_topics.extend(repo.get("topics", []))
        
        topic_counts = Counter(all_topics)
        
        return {
            "top_topics": dict(topic_counts.most_common(20)),
            "total_unique_topics": len(topic_counts)
        }
    
    def _analyze_organizations(self) -> Dict[str, Any]:
        """Analyze organizations."""
        print("  🏢 Analyzing organizations...")
        
        orgs = Counter(
            r.get("owner", {}).get("login", "Unknown")
            for r in self.repos
        )
        
        org_stars = defaultdict(int)
        for repo in self.repos:
            org = repo.get("owner", {}).get("login", "")
            if org:
                org_stars[org] += repo.get("stargazers_count", 0)
        
        return {
            "top_organizations": dict(orgs.most_common(10)),
            "organization_stars": dict(sorted(org_stars.items(), key=lambda x: x[1], reverse=True)[:10])
        }
    
    def _analyze_trends(self) -> Dict[str, Any]:
        """Analyze trends (star velocity, growth)."""
        print("  📈 Analyzing trends...")
        
        velocities = []
        for repo in self.repos:
            created_at = datetime.fromisoformat(repo.get("created_at", "").replace("Z", "+00:00"))
            days_old = (datetime.now(created_at.tzinfo) - created_at).days or 1
            velocity = repo.get("stargazers_count", 0) / days_old
            velocities.append({
                "name": repo.get("full_name"),
                "velocity": velocity,
                "stars": repo.get("stargazers_count", 0)
            })
        
        velocities.sort(key=lambda x: x["velocity"], reverse=True)
        
        return {
            "top_velocity": velocities[:10],
            "avg_velocity": sum(v["velocity"] for v in velocities) / len(velocities) if velocities else 0
        }
    
    def _analyze_quality(self) -> Dict[str, Any]:
        """Analyze quality indicators."""
        print("  ⭐ Analyzing quality...")
        
        has_license = sum(1 for r in self.repos if r.get("license"))
        has_wiki = sum(1 for r in self.repos if r.get("has_wiki", False))
        has_pages = sum(1 for r in self.repos if r.get("has_pages", False))
        has_description = sum(1 for r in self.repos if r.get("description"))
        has_topics = sum(1 for r in self.repos if r.get("topics"))
        archived = sum(1 for r in self.repos if r.get("archived", False))
        
        return {
            "has_license": has_license,
            "has_wiki": has_wiki,
            "has_pages": has_pages,
            "has_description": has_description,
            "has_topics": has_topics,
            "archived": archived,
            "quality_percentage": {
                "license": round(has_license / len(self.repos) * 100, 1) if self.repos else 0,
                "description": round(has_description / len(self.repos) * 100, 1) if self.repos else 0,
                "topics": round(has_topics / len(self.repos) * 100, 1) if self.repos else 0
            }
        }
    
    def _analyze_activity(self) -> Dict[str, Any]:
        """Analyze activity patterns."""
        print("  🔄 Analyzing activity...")
        
        days_since_update = []
        for repo in self.repos:
            updated_at = datetime.fromisoformat(repo.get("updated_at", "").replace("Z", "+00:00"))
            days = (datetime.now(updated_at.tzinfo) - updated_at).days
            days_since_update.append(days)
        
        recent_updates = sum(1 for d in days_since_update if d < 30)
        active = sum(1 for d in days_since_update if d < 90)
        
        return {
            "recently_updated_30d": recent_updates,
            "active_90d": active,
            "avg_days_since_update": round(sum(days_since_update) / len(days_since_update), 1) if days_since_update else 0
        }
    
    def _generate_insights(self) -> List[str]:
        """Generate human-readable insights."""
        print("  💡 Generating insights...")
        
        insights = []
        
        # Summary insights
        summary = self.analysis.get("summary", {})
        insights.append(f"Analyzed {summary.get('total_repos', 0)} repositories with {summary.get('total_stars', 0):,} total stars")
        
        # Language insights
        languages = self.analysis.get("languages", {})
        top_lang = list(languages.get("top_languages", {}).keys())[0] if languages.get("top_languages") else None
        if top_lang:
            insights.append(f"Most popular language: {top_lang} ({languages['top_languages'][top_lang]} repos)")
        
        # Quality insights
        quality = self.analysis.get("quality", {})
        license_pct = quality.get("quality_percentage", {}).get("license", 0)
        insights.append(f"{license_pct}% of repos have licenses")
        
        # Activity insights
        activity = self.analysis.get("activity", {})
        recent = activity.get("recently_updated_30d", 0)
        insights.append(f"{recent} repos updated in the last 30 days")
        
        # Trend insights
        trends = self.analysis.get("trends", {})
        if trends.get("top_velocity"):
            top_vel = trends["top_velocity"][0]
            insights.append(f"Fastest growing: {top_vel['name']} ({top_vel['velocity']:.1f} stars/day)")
        
        return insights
    
    def print_report(self):
        """Print analysis report."""
        if not self.analysis:
            self.analyze()
        
        print("\n" + "=" * 80)
        print("ANALYSIS REPORT")
        print("=" * 80)
        
        # Summary
        summary = self.analysis["summary"]
        print(f"\n📊 Summary:")
        print(f"  Total repositories: {summary['total_repos']:,}")
        print(f"  Total stars: {summary['total_stars']:,}")
        print(f"  Average stars: {summary['avg_stars']:,.0f}")
        print(f"  Max stars: {summary['max_stars']:,}")
        
        # Languages
        languages = self.analysis["languages"]
        print(f"\n💻 Top Languages:")
        for lang, count in list(languages["top_languages"].items())[:5]:
            stars = languages["language_stars"].get(lang, 0)
            print(f"  {lang}: {count} repos ({stars:,} stars)")
        
        # Topics
        topics = self.analysis["topics"]
        print(f"\n🏷️  Top Topics:")
        for topic, count in list(topics["top_topics"].items())[:5]:
            print(f"  {topic}: {count} repos")
        
        # Organizations
        orgs = self.analysis["organizations"]
        print(f"\n🏢 Top Organizations:")
        for org, count in list(orgs["top_organizations"].items())[:5]:
            stars = orgs["organization_stars"].get(org, 0)
            print(f"  {org}: {count} repos ({stars:,} stars)")
        
        # Quality
        quality = self.analysis["quality"]
        print(f"\n⭐ Quality Metrics:")
        for metric, pct in quality["quality_percentage"].items():
            print(f"  {metric.capitalize()}: {pct}%")
        
        # Activity
        activity = self.analysis["activity"]
        print(f"\n🔄 Activity:")
        print(f"  Updated in last 30 days: {activity['recently_updated_30d']}")
        print(f"  Active (90 days): {activity['active_90d']}")
        print(f"  Avg days since update: {activity['avg_days_since_update']}")
        
        # Insights
        print(f"\n💡 Key Insights:")
        for insight in self.analysis["insights"]:
            print(f"  • {insight}")
    
    def export_json(self, filename: str = "analysis.json"):
        """Export analysis to JSON."""
        if not self.analysis:
            self.analyze()
        
        with open(filename, "w") as f:
            json.dump(self.analysis, f, indent=2, default=str)
        print(f"\n💾 Analysis exported to {filename}")


def main():
    """Example usage."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Analyze repositories")
    parser.add_argument("--input", type=str, required=True, help="Input JSON file with repos")
    parser.add_argument("--output", type=str, default="analysis.json", help="Output JSON file")
    
    args = parser.parse_args()
    
    # Load repos
    with open(args.input, "r") as f:
        repos = json.load(f)
    
    print(f"📦 Loaded {len(repos)} repositories")
    
    # Analyze
    analyzer = RepoAnalyzer(repos)
    analyzer.analyze()
    analyzer.print_report()
    analyzer.export_json(args.output)


if __name__ == "__main__":
    main()

