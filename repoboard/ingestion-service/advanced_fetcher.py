"""Advanced repository fetching with multiple strategies for large-scale ingestion."""

import sys
import os
import time
import requests
from typing import List, Dict, Any, Optional, Set
from datetime import datetime, timedelta
from collections import defaultdict
import re

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from ingestion_service.github_client import GitHubClient
except ImportError:
    # Fallback for direct import
    from github_client import GitHubClient

from shared.config import settings


class AdvancedRepoFetcher:
    """Advanced fetcher with multiple strategies for comprehensive repo discovery."""
    
    # Top languages to scan
    TOP_LANGUAGES = [
        "python", "javascript", "typescript", "java", "go", "rust",
        "cpp", "c", "csharp", "php", "ruby", "swift", "kotlin",
        "dart", "scala", "r", "matlab", "shell", "html", "css"
    ]
    
    # Popular topics to scan
    POPULAR_TOPICS = [
        "machine-learning", "deep-learning", "artificial-intelligence",
        "web-development", "frontend", "backend", "full-stack",
        "react", "vue", "angular", "nodejs", "django", "flask",
        "docker", "kubernetes", "devops", "ci-cd",
        "blockchain", "cryptocurrency", "web3",
        "mobile-app", "ios", "android", "react-native",
        "data-science", "data-visualization", "analytics",
        "security", "cryptography", "authentication",
        "game-development", "game-engine",
        "api", "rest-api", "graphql",
        "database", "sql", "nosql",
        "testing", "test-automation",
        "automation", "scraping", "bot"
    ]
    
    # Top organizations to monitor
    TOP_ORGS = [
        "google", "facebook", "microsoft", "apple", "amazon",
        "netflix", "uber", "airbnb", "twitter", "github",
        "mozilla", "apache", "kubernetes", "tensorflow", "pytorch",
        "nvidia", "openai", "anthropic", "huggingface"
    ]
    
    def __init__(self, github_token: Optional[str] = None):
        self.github_client = GitHubClient(github_token)
        self.fetched_urls: Set[str] = set()  # Track fetched repos to avoid duplicates
    
    def fetch_by_language(self, language: str, min_stars: int = 100, limit: int = 100) -> List[Dict[str, Any]]:
        """Fetch repos by programming language."""
        print(f"Fetching {language} repos (min_stars={min_stars}, limit={limit})...")
        
        repos = []
        query = f"language:{language} stars:>={min_stars}"
        
        for page in range(1, (limit // 100) + 2):
            try:
                params = {
                    "q": query,
                    "sort": "stars",
                    "order": "desc",
                    "per_page": 100,
                    "page": page
                }
                data = self.github_client._make_request("/search/repositories", params)
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
            except Exception as e:
                print(f"Error fetching {language} page {page}: {e}")
                break
        
        print(f"Fetched {len(repos)} {language} repos")
        return repos[:limit]
    
    def fetch_by_topic(self, topic: str, min_stars: int = 50, limit: int = 100) -> List[Dict[str, Any]]:
        """Fetch repos by GitHub topic."""
        print(f"Fetching {topic} topic repos (min_stars={min_stars}, limit={limit})...")
        
        repos = []
        query = f"topic:{topic} stars:>={min_stars}"
        
        for page in range(1, (limit // 100) + 2):
            try:
                params = {
                    "q": query,
                    "sort": "stars",
                    "order": "desc",
                    "per_page": 100,
                    "page": page
                }
                data = self.github_client._make_request("/search/repositories", params)
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
            except Exception as e:
                print(f"Error fetching {topic} page {page}: {e}")
                break
        
        print(f"Fetched {len(repos)} {topic} repos")
        return repos[:limit]
    
    def fetch_by_organization(self, org: str, min_stars: int = 100, limit: int = 200) -> List[Dict[str, Any]]:
        """Fetch repos from a specific organization."""
        print(f"Fetching {org} organization repos (min_stars={min_stars}, limit={limit})...")
        
        repos = []
        query = f"org:{org} stars:>={min_stars}"
        
        for page in range(1, (limit // 100) + 2):
            try:
                params = {
                    "q": query,
                    "sort": "stars",
                    "order": "desc",
                    "per_page": 100,
                    "page": page
                }
                data = self.github_client._make_request("/search/repositories", params)
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
            except Exception as e:
                print(f"Error fetching {org} page {page}: {e}")
                break
        
        print(f"Fetched {len(repos)} {org} repos")
        return repos[:limit]
    
    def fetch_trending_recent(self, days: int = 7, min_stars: int = 50, limit: int = 200) -> List[Dict[str, Any]]:
        """Fetch recently created repos that are gaining stars."""
        print(f"Fetching trending repos from last {days} days (min_stars={min_stars}, limit={limit})...")
        
        repos = []
        since_date = (datetime.now() - timedelta(days=days)).strftime("%Y-%m-%d")
        query = f"created:>={since_date} stars:>={min_stars}"
        
        for page in range(1, (limit // 100) + 2):
            try:
                params = {
                    "q": query,
                    "sort": "stars",
                    "order": "desc",
                    "per_page": 100,
                    "page": page
                }
                data = self.github_client._make_request("/search/repositories", params)
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
            except Exception as e:
                print(f"Error fetching trending page {page}: {e}")
                break
        
        print(f"Fetched {len(repos)} trending repos")
        return repos[:limit]
    
    def fetch_recently_updated(self, days: int = 30, min_stars: int = 100, limit: int = 200) -> List[Dict[str, Any]]:
        """Fetch repos that were recently updated (active projects)."""
        print(f"Fetching recently updated repos (last {days} days, min_stars={min_stars}, limit={limit})...")
        
        repos = []
        since_date = (datetime.now() - timedelta(days=days)).strftime("%Y-%m-%d")
        query = f"pushed:>={since_date} stars:>={min_stars}"
        
        for page in range(1, (limit // 100) + 2):
            try:
                params = {
                    "q": query,
                    "sort": "updated",
                    "order": "desc",
                    "per_page": 100,
                    "page": page
                }
                data = self.github_client._make_request("/search/repositories", params)
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
            except Exception as e:
                print(f"Error fetching updated repos page {page}: {e}")
                break
        
        print(f"Fetched {len(repos)} recently updated repos")
        return repos[:limit]
    
    def fetch_rising_stars(self, min_star_velocity: float = 5.0, limit: int = 100) -> List[Dict[str, Any]]:
        """Fetch repos with high star velocity (rising stars)."""
        print(f"Fetching rising stars (min_velocity={min_star_velocity}, limit={limit})...")
        
        # Get recently created repos and calculate velocity
        recent_repos = self.fetch_trending_recent(days=30, min_stars=10, limit=500)
        
        rising_stars = []
        for repo in recent_repos:
            velocity = self.github_client.calculate_star_velocity(repo)
            if velocity >= min_star_velocity:
                rising_stars.append(repo)
        
        # Sort by velocity
        rising_stars.sort(key=lambda r: self.github_client.calculate_star_velocity(r), reverse=True)
        
        print(f"Found {len(rising_stars)} rising stars")
        return rising_stars[:limit]
    
    def fetch_from_awesome_list(self, awesome_list_url: str) -> List[str]:
        """Extract repository URLs from an awesome list markdown file."""
        print(f"Fetching repos from awesome list: {awesome_list_url}")
        
        try:
            response = requests.get(awesome_list_url, timeout=10)
            response.raise_for_status()
            content = response.text
            
            # Extract GitHub URLs using regex
            pattern = r'https://github\.com/([a-zA-Z0-9_-]+/[a-zA-Z0-9_.-]+)'
            matches = re.findall(pattern, content)
            
            # Convert to full URLs
            repo_urls = [f"https://github.com/{match}" for match in matches]
            
            print(f"Extracted {len(repo_urls)} repo URLs from awesome list")
            return repo_urls
        except Exception as e:
            print(f"Error fetching awesome list: {e}")
            return []
    
    def comprehensive_fetch(
        self,
        languages: Optional[List[str]] = None,
        topics: Optional[List[str]] = None,
        orgs: Optional[List[str]] = None,
        include_trending: bool = True,
        include_updated: bool = True,
        include_rising: bool = True,
        per_category_limit: int = 50
    ) -> List[Dict[str, Any]]:
        """
        Comprehensive fetch using multiple strategies.
        Returns deduplicated list of repositories.
        """
        print("Starting comprehensive repository fetch...")
        all_repos = []
        
        # Fetch by languages
        if languages is None:
            languages = self.TOP_LANGUAGES[:10]  # Top 10 languages
        
        for lang in languages:
            repos = self.fetch_by_language(lang, min_stars=100, limit=per_category_limit)
            all_repos.extend(repos)
            time.sleep(1)  # Be nice to API
        
        # Fetch by topics
        if topics is None:
            topics = self.POPULAR_TOPICS[:20]  # Top 20 topics
        
        for topic in topics:
            repos = self.fetch_by_topic(topic, min_stars=50, limit=per_category_limit)
            all_repos.extend(repos)
            time.sleep(1)
        
        # Fetch by organizations
        if orgs is None:
            orgs = self.TOP_ORGS[:10]  # Top 10 orgs
        
        for org in orgs:
            repos = self.fetch_by_organization(org, min_stars=100, limit=per_category_limit)
            all_repos.extend(repos)
            time.sleep(1)
        
        # Fetch trending
        if include_trending:
            repos = self.fetch_trending_recent(days=7, min_stars=50, limit=per_category_limit * 2)
            all_repos.extend(repos)
        
        # Fetch recently updated
        if include_updated:
            repos = self.fetch_recently_updated(days=30, min_stars=100, limit=per_category_limit * 2)
            all_repos.extend(repos)
        
        # Fetch rising stars
        if include_rising:
            repos = self.fetch_rising_stars(min_star_velocity=5.0, limit=per_category_limit)
            all_repos.extend(repos)
        
        # Deduplicate by URL
        seen = set()
        unique_repos = []
        for repo in all_repos:
            url = repo["html_url"]
            if url not in seen:
                seen.add(url)
                unique_repos.append(repo)
        
        print(f"\nComprehensive fetch complete: {len(unique_repos)} unique repositories")
        return unique_repos
    
    def fetch_awesome_lists(self, awesome_list_urls: List[str]) -> List[str]:
        """Fetch repos from multiple awesome lists."""
        all_urls = []
        for url in awesome_list_urls:
            urls = self.fetch_from_awesome_list(url)
            all_urls.extend(urls)
        
        # Deduplicate
        return list(set(all_urls))


# Popular awesome lists to scrape
POPULAR_AWESOME_LISTS = [
    "https://raw.githubusercontent.com/sindresorhus/awesome/main/readme.md",
    "https://raw.githubusercontent.com/topics/awesome/README.md",
    # Add more awesome list URLs here
]


if __name__ == "__main__":
    # Example usage
    fetcher = AdvancedRepoFetcher()
    
    # Comprehensive fetch
    repos = fetcher.comprehensive_fetch(
        languages=["python", "javascript", "go"],
        topics=["machine-learning", "web-development"],
        per_category_limit=20
    )
    
    print(f"\nTotal unique repos fetched: {len(repos)}")

