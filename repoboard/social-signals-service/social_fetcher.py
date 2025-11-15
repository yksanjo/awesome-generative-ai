"""Service to fetch social signals from various platforms."""

import sys
import os
import re
import time
import requests
from typing import Dict, Any, Optional, List
from datetime import datetime, timedelta
from urllib.parse import quote

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from shared.config import settings


class SocialSignalsFetcher:
    """Fetches social signals from Reddit, HackerNews, Stack Overflow, npm, PyPI."""
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": "RepoBoard/1.0 (Social Signals Fetcher)"
        })
    
    def fetch_all_signals(self, repo_name: str, repo_url: str, description: Optional[str] = None) -> Dict[str, Any]:
        """Fetch all social signals for a repository."""
        signals = {
            "reddit_mentions": 0,
            "reddit_upvotes": 0,
            "reddit_subreddits": [],
            "hn_mentions": 0,
            "hn_points": 0,
            "hn_comments": 0,
            "stackoverflow_questions": 0,
            "stackoverflow_views": 0,
            "stackoverflow_score": 0,
            "npm_weekly_downloads": 0,
            "pypi_weekly_downloads": 0,
            "package_name": None,
            "twitter_mentions": 0,
        }
        
        # Extract package name from repo if it's a package repo
        package_name = self._extract_package_name(repo_name, description)
        if package_name:
            signals["package_name"] = package_name
        
        # Fetch Reddit signals
        try:
            reddit_data = self.fetch_reddit_signals(repo_name, repo_url)
            signals.update(reddit_data)
        except Exception as e:
            print(f"Error fetching Reddit signals: {e}")
        
        # Fetch HackerNews signals
        try:
            hn_data = self.fetch_hn_signals(repo_name, repo_url)
            signals.update(hn_data)
        except Exception as e:
            print(f"Error fetching HN signals: {e}")
        
        # Fetch Stack Overflow signals
        try:
            so_data = self.fetch_stackoverflow_signals(repo_name, description)
            signals.update(so_data)
        except Exception as e:
            print(f"Error fetching Stack Overflow signals: {e}")
        
        # Fetch npm downloads
        if package_name:
            try:
                npm_data = self.fetch_npm_downloads(package_name)
                signals.update(npm_data)
            except Exception as e:
                print(f"Error fetching npm downloads: {e}")
        
        # Fetch PyPI downloads
        if package_name:
            try:
                pypi_data = self.fetch_pypi_downloads(package_name)
                signals.update(pypi_data)
            except Exception as e:
                print(f"Error fetching PyPI downloads: {e}")
        
        # Calculate aggregated social score
        signals["social_score"] = self._calculate_social_score(signals)
        
        return signals
    
    def _extract_package_name(self, repo_name: str, description: Optional[str] = None) -> Optional[str]:
        """Try to extract package name from repo name or description."""
        # Common patterns: owner/repo-name -> repo-name
        # For npm: usually matches repo name
        # For PyPI: might be different (e.g., repo-name -> repo_name)
        
        # Simple heuristic: use repo name as package name
        # In production, you'd want to check package.json, setup.py, etc.
        return repo_name.lower().replace("-", "_")
    
    def fetch_reddit_signals(self, repo_name: str, repo_url: str) -> Dict[str, Any]:
        """Fetch Reddit mentions using Pushshift API (or Reddit search)."""
        # Note: Pushshift API is limited, so we'll use Reddit's search API
        # This is a simplified version - in production, you'd want to use Reddit API properly
        
        signals = {
            "reddit_mentions": 0,
            "reddit_upvotes": 0,
            "reddit_subreddits": [],
        }
        
        try:
            # Search Reddit for repo URL and name
            search_terms = [repo_url, f"r/{repo_name}", repo_name]
            subreddits_found = set()
            total_upvotes = 0
            mention_count = 0
            
            for term in search_terms:
                # Reddit search API (limited without auth)
                # In production, use Reddit API with proper authentication
                search_url = f"https://www.reddit.com/search.json"
                params = {
                    "q": term,
                    "limit": 25,
                    "sort": "relevance"
                }
                
                try:
                    response = self.session.get(search_url, params=params, timeout=5)
                    if response.status_code == 200:
                        data = response.json()
                        if "data" in data and "children" in data["data"]:
                            for post in data["data"]["children"]:
                                post_data = post.get("data", {})
                                subreddit = post_data.get("subreddit")
                                if subreddit:
                                    subreddits_found.add(subreddit)
                                upvotes = post_data.get("ups", 0)
                                total_upvotes += upvotes
                                mention_count += 1
                except Exception as e:
                    print(f"Reddit search error for {term}: {e}")
                    continue
                
                time.sleep(1)  # Rate limiting
            
            signals["reddit_mentions"] = mention_count
            signals["reddit_upvotes"] = total_upvotes
            signals["reddit_subreddits"] = list(subreddits_found)
        except Exception as e:
            print(f"Error in Reddit fetch: {e}")
        
        return signals
    
    def fetch_hn_signals(self, repo_name: str, repo_url: str) -> Dict[str, Any]:
        """Fetch HackerNews mentions using Algolia HN Search API."""
        signals = {
            "hn_mentions": 0,
            "hn_points": 0,
            "hn_comments": 0,
        }
        
        try:
            # Use Algolia HN Search API
            search_url = "https://hn.algolia.com/api/v1/search"
            
            # Search by URL
            params = {
                "query": repo_url,
                "tags": "story",
                "hitsPerPage": 50
            }
            
            response = self.session.get(search_url, params=params, timeout=5)
            if response.status_code == 200:
                data = response.json()
                hits = data.get("hits", [])
                
                total_points = 0
                total_comments = 0
                
                for hit in hits:
                    points = hit.get("points", 0)
                    num_comments = hit.get("num_comments", 0)
                    total_points += points
                    total_comments += num_comments
                
                signals["hn_mentions"] = len(hits)
                signals["hn_points"] = total_points
                signals["hn_comments"] = total_comments
            
            # Also search by repo name
            params_name = {
                "query": repo_name,
                "tags": "story",
                "hitsPerPage": 20
            }
            
            response_name = self.session.get(search_url, params=params_name, timeout=5)
            if response_name.status_code == 200:
                data = response_name.json()
                hits = data.get("hits", [])
                # Only count if URL matches (to avoid false positives)
                for hit in hits:
                    url = hit.get("url", "")
                    if repo_url in url or repo_name in url:
                        signals["hn_mentions"] += 1
                        signals["hn_points"] += hit.get("points", 0)
                        signals["hn_comments"] += hit.get("num_comments", 0)
            
        except Exception as e:
            print(f"Error in HN fetch: {e}")
        
        return signals
    
    def fetch_stackoverflow_signals(self, repo_name: str, description: Optional[str] = None) -> Dict[str, Any]:
        """Fetch Stack Overflow mentions using Stack Exchange API."""
        signals = {
            "stackoverflow_questions": 0,
            "stackoverflow_views": 0,
            "stackoverflow_score": 0,
        }
        
        try:
            # Stack Exchange API
            api_url = "https://api.stackexchange.com/2.3/search/advanced"
            
            # Search for questions mentioning the repo
            search_query = f"{repo_name} github.com"
            if description:
                # Add key terms from description
                key_terms = description.split()[:5]  # First 5 words
                search_query += " " + " ".join(key_terms)
            
            params = {
                "q": search_query,
                "site": "stackoverflow",
                "pagesize": 50,
                "sort": "relevance",
                "order": "desc"
            }
            
            response = self.session.get(api_url, params=params, timeout=5)
            if response.status_code == 200:
                data = response.json()
                items = data.get("items", [])
                
                total_views = 0
                total_score = 0
                
                for item in items:
                    # Check if it's actually about this repo
                    title = item.get("title", "").lower()
                    body = item.get("body", "").lower()
                    
                    if repo_name.lower() in title or repo_name.lower() in body:
                        total_views += item.get("view_count", 0)
                        total_score += item.get("score", 0)
                
                signals["stackoverflow_questions"] = len(items)
                signals["stackoverflow_views"] = total_views
                signals["stackoverflow_score"] = total_score
                
        except Exception as e:
            print(f"Error in Stack Overflow fetch: {e}")
        
        return signals
    
    def fetch_npm_downloads(self, package_name: str) -> Dict[str, Any]:
        """Fetch npm weekly downloads."""
        signals = {
            "npm_weekly_downloads": 0,
        }
        
        try:
            # npm API
            api_url = f"https://api.npmjs.org/downloads/point/last-week/{package_name}"
            
            response = self.session.get(api_url, timeout=5)
            if response.status_code == 200:
                data = response.json()
                signals["npm_weekly_downloads"] = data.get("downloads", 0)
            elif response.status_code == 404:
                # Package doesn't exist on npm
                pass
        except Exception as e:
            print(f"Error fetching npm downloads: {e}")
        
        return signals
    
    def fetch_pypi_downloads(self, package_name: str) -> Dict[str, Any]:
        """Fetch PyPI weekly downloads."""
        signals = {
            "pypi_weekly_downloads": 0,
        }
        
        try:
            # PyPI JSON API
            api_url = f"https://pypi.org/pypi/{package_name}/json"
            
            response = self.session.get(api_url, timeout=5)
            if response.status_code == 200:
                data = response.json()
                # PyPI doesn't provide download stats directly in the JSON API
                # You'd need to use pypistats.org API or similar
                # For now, we'll just mark that the package exists
                if "info" in data:
                    # Try pypistats API
                    stats_url = f"https://pypistats.org/api/packages/{package_name}/recent"
                    stats_response = self.session.get(stats_url, timeout=5)
                    if stats_response.status_code == 200:
                        stats_data = stats_response.json()
                        if "data" in stats_data and "last_week" in stats_data["data"]:
                            signals["pypi_weekly_downloads"] = stats_data["data"]["last_week"]
        except Exception as e:
            print(f"Error fetching PyPI downloads: {e}")
        
        return signals
    
    def _calculate_social_score(self, signals: Dict[str, Any]) -> float:
        """Calculate aggregated social score (0-100)."""
        score = 0.0
        
        # Reddit (max 20 points)
        reddit_score = min(20, (signals["reddit_upvotes"] / 100) * 20)
        score += reddit_score
        
        # HackerNews (max 25 points)
        hn_score = min(25, (signals["hn_points"] / 50) * 25)
        score += hn_score
        
        # Stack Overflow (max 20 points)
        so_score = min(20, (signals["stackoverflow_views"] / 10000) * 20)
        score += so_score
        
        # npm downloads (max 15 points)
        npm_score = min(15, (signals["npm_weekly_downloads"] / 100000) * 15)
        score += npm_score
        
        # PyPI downloads (max 15 points)
        pypi_score = min(15, (signals["pypi_weekly_downloads"] / 100000) * 15)
        score += pypi_score
        
        # Mentions bonus (max 5 points)
        mention_bonus = min(5, (signals["reddit_mentions"] + signals["hn_mentions"]) / 10)
        score += mention_bonus
        
        return min(100.0, score)

