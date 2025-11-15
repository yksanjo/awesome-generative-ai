"""Enhanced multi-strategy repository fetcher with comprehensive discovery."""

import os
import requests
import json
import time
from typing import List, Dict, Any, Optional, Set
from datetime import datetime, timedelta
from collections import defaultdict


class EnhancedRepoFetcher:
    """Enhanced fetcher with multiple strategies for comprehensive discovery."""
    
    def __init__(self, github_token: Optional[str] = None):
        self.github_token = github_token or os.getenv("GITHUB_TOKEN")
        self.headers = {
            "Accept": "application/vnd.github.v3+json",
        }
        if self.github_token:
            self.headers["Authorization"] = f"token {self.github_token}"
        self.fetched_urls: Set[str] = set()
        self.stats = defaultdict(int)
    
    def _make_request(self, url: str, params: Optional[Dict] = None) -> Dict[str, Any]:
        """Make API request with error handling."""
        try:
            response = requests.get(url, headers=self.headers, params=params, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"  ⚠️  API error: {e}")
            return {}
    
    def fetch_by_language(self, language: str, min_stars: int = 100, limit: int = 100) -> List[Dict[str, Any]]:
        """Fetch repos by programming language."""
        print(f"  📦 Fetching {language} repos (min_stars={min_stars})...")
        repos = []
        query = f"language:{language} stars:>={min_stars}"
        
        for page in range(1, (limit // 100) + 2):
            data = self._make_request(
                "https://api.github.com/search/repositories",
                params={
                    "q": query,
                    "sort": "stars",
                    "order": "desc",
                    "per_page": 100,
                    "page": page
                }
            )
            
            items = data.get("items", [])
            if not items:
                break
            
            for item in items:
                if item["html_url"] not in self.fetched_urls:
                    repos.append(item)
                    self.fetched_urls.add(item["html_url"])
            
            if len(repos) >= limit:
                break
            
            time.sleep(0.5)  # Rate limiting
        
        self.stats[f"language_{language}"] = len(repos)
        print(f"    ✅ Found {len(repos)} {language} repos")
        return repos[:limit]
    
    def fetch_by_topic(self, topic: str, min_stars: int = 50, limit: int = 100) -> List[Dict[str, Any]]:
        """Fetch repos by GitHub topic."""
        print(f"  🏷️  Fetching {topic} topic repos...")
        repos = []
        query = f"topic:{topic} stars:>={min_stars}"
        
        for page in range(1, (limit // 100) + 2):
            data = self._make_request(
                "https://api.github.com/search/repositories",
                params={
                    "q": query,
                    "sort": "stars",
                    "order": "desc",
                    "per_page": 100,
                    "page": page
                }
            )
            
            items = data.get("items", [])
            if not items:
                break
            
            for item in items:
                if item["html_url"] not in self.fetched_urls:
                    repos.append(item)
                    self.fetched_urls.add(item["html_url"])
            
            if len(repos) >= limit:
                break
            
            time.sleep(0.5)
        
        self.stats[f"topic_{topic}"] = len(repos)
        print(f"    ✅ Found {len(repos)} {topic} repos")
        return repos[:limit]
    
    def fetch_by_organization(self, org: str, min_stars: int = 100, limit: int = 200) -> List[Dict[str, Any]]:
        """Fetch repos from organization."""
        print(f"  🏢 Fetching {org} organization repos...")
        repos = []
        query = f"org:{org} stars:>={min_stars}"
        
        for page in range(1, (limit // 100) + 2):
            data = self._make_request(
                "https://api.github.com/search/repositories",
                params={
                    "q": query,
                    "sort": "stars",
                    "order": "desc",
                    "per_page": 100,
                    "page": page
                }
            )
            
            items = data.get("items", [])
            if not items:
                break
            
            for item in items:
                if item["html_url"] not in self.fetched_urls:
                    repos.append(item)
                    self.fetched_urls.add(item["html_url"])
            
            if len(repos) >= limit:
                break
            
            time.sleep(0.5)
        
        self.stats[f"org_{org}"] = len(repos)
        print(f"    ✅ Found {len(repos)} {org} repos")
        return repos[:limit]
    
    def fetch_trending(self, days: int = 7, min_stars: int = 50, limit: int = 200) -> List[Dict[str, Any]]:
        """Fetch trending repos (recently created with stars)."""
        print(f"  🔥 Fetching trending repos (last {days} days)...")
        repos = []
        since_date = (datetime.now() - timedelta(days=days)).strftime("%Y-%m-%d")
        query = f"created:>={since_date} stars:>={min_stars}"
        
        for page in range(1, (limit // 100) + 2):
            data = self._make_request(
                "https://api.github.com/search/repositories",
                params={
                    "q": query,
                    "sort": "stars",
                    "order": "desc",
                    "per_page": 100,
                    "page": page
                }
            )
            
            items = data.get("items", [])
            if not items:
                break
            
            for item in items:
                if item["html_url"] not in self.fetched_urls:
                    repos.append(item)
                    self.fetched_urls.add(item["html_url"])
            
            if len(repos) >= limit:
                break
            
            time.sleep(0.5)
        
        self.stats["trending"] = len(repos)
        print(f"    ✅ Found {len(repos)} trending repos")
        return repos[:limit]
    
    def fetch_recently_updated(self, days: int = 30, min_stars: int = 100, limit: int = 200) -> List[Dict[str, Any]]:
        """Fetch recently updated active repos."""
        print(f"  🔄 Fetching recently updated repos (last {days} days)...")
        repos = []
        since_date = (datetime.now() - timedelta(days=days)).strftime("%Y-%m-%d")
        query = f"pushed:>={since_date} stars:>={min_stars}"
        
        for page in range(1, (limit // 100) + 2):
            data = self._make_request(
                "https://api.github.com/search/repositories",
                params={
                    "q": query,
                    "sort": "updated",
                    "order": "desc",
                    "per_page": 100,
                    "page": page
                }
            )
            
            items = data.get("items", [])
            if not items:
                break
            
            for item in items:
                if item["html_url"] not in self.fetched_urls:
                    repos.append(item)
                    self.fetched_urls.add(item["html_url"])
            
            if len(repos) >= limit:
                break
            
            time.sleep(0.5)
        
        self.stats["recently_updated"] = len(repos)
        print(f"    ✅ Found {len(repos)} recently updated repos")
        return repos[:limit]
    
    def fetch_rising_stars(self, min_star_velocity: float = 5.0, limit: int = 100) -> List[Dict[str, Any]]:
        """Fetch repos with high star velocity (rising stars)."""
        print(f"  ⭐ Fetching rising stars (velocity > {min_star_velocity}/day)...")
        
        # Get recently created repos
        recent = self.fetch_trending(days=30, min_stars=10, limit=500)
        
        rising = []
        for repo in recent:
            created_at = datetime.fromisoformat(repo.get("created_at", "").replace("Z", "+00:00"))
            days_old = (datetime.now(created_at.tzinfo) - created_at).days or 1
            velocity = repo.get("stargazers_count", 0) / days_old
            
            if velocity >= min_star_velocity:
                rising.append(repo)
        
        rising.sort(key=lambda r: r.get("stargazers_count", 0), reverse=True)
        
        self.stats["rising_stars"] = len(rising)
        print(f"    ✅ Found {len(rising)} rising stars")
        return rising[:limit]
    
    def fetch_hidden_gems(self, max_stars: int = 500, min_quality_score: float = 0.7, limit: int = 50) -> List[Dict[str, Any]]:
        """Fetch hidden gems (high quality but low visibility)."""
        print(f"  💎 Fetching hidden gems (stars < {max_stars}, quality > {min_quality_score})...")
        
        # Get repos with moderate stars
        query = f"stars:10..{max_stars} pushed:>2024-01-01"
        repos = []
        
        for page in range(1, 6):  # Limit pages for hidden gems
            data = self._make_request(
                "https://api.github.com/search/repositories",
                params={
                    "q": query,
                    "sort": "updated",
                    "order": "desc",
                    "per_page": 100,
                    "page": page
                }
            )
            
            items = data.get("items", [])
            if not items:
                break
            
            for item in items:
                if item["html_url"] not in self.fetched_urls:
                    # Calculate quality score
                    has_license = item.get("license") is not None
                    has_wiki = item.get("has_wiki", False)
                    has_pages = item.get("has_pages", False)
                    has_description = bool(item.get("description"))
                    has_topics = len(item.get("topics", [])) > 0
                    
                    quality = (
                        (0.2 if has_license else 0) +
                        (0.2 if has_wiki or has_pages else 0) +
                        (0.2 if has_description else 0) +
                        (0.2 if has_topics else 0) +
                        (0.2 if not item.get("archived", False) else 0)
                    )
                    
                    if quality >= min_quality_score:
                        repos.append(item)
                        self.fetched_urls.add(item["html_url"])
            
            time.sleep(0.5)
        
        repos.sort(key=lambda r: r.get("stargazers_count", 0), reverse=True)
        
        self.stats["hidden_gems"] = len(repos)
        print(f"    ✅ Found {len(repos)} hidden gems")
        return repos[:limit]
    
    def comprehensive_fetch(
        self,
        languages: Optional[List[str]] = None,
        topics: Optional[List[str]] = None,
        orgs: Optional[List[str]] = None,
        include_trending: bool = True,
        include_updated: bool = True,
        include_rising: bool = True,
        include_hidden_gems: bool = True,
        per_category_limit: int = 50
    ) -> List[Dict[str, Any]]:
        """Comprehensive fetch using all strategies."""
        print("=" * 80)
        print("COMPREHENSIVE REPOSITORY FETCH")
        print("=" * 80)
        
        all_repos = []
        
        # Languages
        if languages:
            for lang in languages:
                repos = self.fetch_by_language(lang, min_stars=100, limit=per_category_limit)
                all_repos.extend(repos)
                time.sleep(1)
        
        # Topics
        if topics:
            for topic in topics:
                repos = self.fetch_by_topic(topic, min_stars=50, limit=per_category_limit)
                all_repos.extend(repos)
                time.sleep(1)
        
        # Organizations
        if orgs:
            for org in orgs:
                repos = self.fetch_by_organization(org, min_stars=100, limit=per_category_limit)
                all_repos.extend(repos)
                time.sleep(1)
        
        # Trending
        if include_trending:
            repos = self.fetch_trending(days=7, min_stars=50, limit=per_category_limit * 2)
            all_repos.extend(repos)
        
        # Recently updated
        if include_updated:
            repos = self.fetch_recently_updated(days=30, min_stars=100, limit=per_category_limit * 2)
            all_repos.extend(repos)
        
        # Rising stars
        if include_rising:
            repos = self.fetch_rising_stars(min_star_velocity=5.0, limit=per_category_limit)
            all_repos.extend(repos)
        
        # Hidden gems
        if include_hidden_gems:
            repos = self.fetch_hidden_gems(max_stars=500, limit=per_category_limit)
            all_repos.extend(repos)
        
        # Deduplicate
        seen = set()
        unique_repos = []
        for repo in all_repos:
            url = repo["html_url"]
            if url not in seen:
                seen.add(url)
                unique_repos.append(repo)
        
        print("\n" + "=" * 80)
        print("FETCH SUMMARY")
        print("=" * 80)
        print(f"Total unique repositories: {len(unique_repos)}")
        print("\nBreakdown by source:")
        for key, count in sorted(self.stats.items()):
            print(f"  {key}: {count}")
        
        return unique_repos


def main():
    """Example usage."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Enhanced repository fetcher")
    parser.add_argument("--languages", nargs="+", help="Languages to fetch")
    parser.add_argument("--topics", nargs="+", help="Topics to fetch")
    parser.add_argument("--orgs", nargs="+", help="Organizations to fetch")
    parser.add_argument("--limit", type=int, default=50, help="Per category limit")
    parser.add_argument("--output", type=str, default="fetched_repos.json", help="Output file")
    parser.add_argument("--no-trending", action="store_true", help="Skip trending")
    parser.add_argument("--no-updated", action="store_true", help="Skip recently updated")
    parser.add_argument("--no-rising", action="store_true", help="Skip rising stars")
    parser.add_argument("--no-gems", action="store_true", help="Skip hidden gems")
    
    args = parser.parse_args()
    
    fetcher = EnhancedRepoFetcher()
    
    repos = fetcher.comprehensive_fetch(
        languages=args.languages or ["python", "javascript", "go"],
        topics=args.topics or ["machine-learning", "web-development"],
        orgs=args.orgs,
        include_trending=not args.no_trending,
        include_updated=not args.no_updated,
        include_rising=not args.no_rising,
        include_hidden_gems=not args.no_gems,
        per_category_limit=args.limit
    )
    
    # Save to file
    with open(args.output, "w") as f:
        json.dump(repos, f, indent=2, default=str)
    
    print(f"\n💾 Saved {len(repos)} repositories to {args.output}")


if __name__ == "__main__":
    main()

