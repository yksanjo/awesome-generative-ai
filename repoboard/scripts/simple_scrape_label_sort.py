#!/usr/bin/env python3
"""
Simple script to scrape GitHub repositories, label them, and sort them.
This is a simplified version that doesn't require the full RepoBoard setup.
"""

import requests
import json
from typing import List, Dict, Any, Optional
from datetime import datetime
from collections import Counter
import os

# Configuration
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")  # Optional but recommended
LLM_API_KEY = os.getenv("OPENAI_API_KEY")  # For labeling (optional)


class SimpleGitHubScraper:
    """Simple GitHub repository scraper."""
    
    BASE_URL = "https://api.github.com"
    
    def __init__(self, token: Optional[str] = None):
        self.token = token or GITHUB_TOKEN
        self.headers = {
            "Accept": "application/vnd.github.v3+json",
        }
        if self.token:
            self.headers["Authorization"] = f"token {self.token}"
    
    def search_repos(self, query: str, sort: str = "stars", order: str = "desc", per_page: int = 100) -> List[Dict]:
        """Search for repositories."""
        url = f"{self.BASE_URL}/search/repositories"
        params = {
            "q": query,
            "sort": sort,
            "order": order,
            "per_page": min(per_page, 100),  # GitHub max is 100
        }
        
        response = requests.get(url, headers=self.headers, params=params)
        response.raise_for_status()
        return response.json().get("items", [])
    
    def get_repo_details(self, owner: str, repo: str) -> Dict:
        """Get detailed repository information."""
        url = f"{self.BASE_URL}/repos/{owner}/{repo}"
        response = requests.get(url, headers=self.headers)
        response.raise_for_status()
        return response.json()
    
    def get_repo_readme(self, owner: str, repo: str) -> Optional[str]:
        """Get README content."""
        try:
            url = f"{self.BASE_URL}/repos/{owner}/{repo}/readme"
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            data = response.json()
            import base64
            return base64.b64decode(data["content"]).decode("utf-8")
        except:
            return None
    
    def scrape_repos(self, query: str, limit: int = 50) -> List[Dict]:
        """Scrape repositories based on search query."""
        print(f"Scraping repositories with query: {query}")
        repos = self.search_repos(query, per_page=min(limit, 100))
        
        # Enrich with README
        for repo in repos[:limit]:
            owner = repo["owner"]["login"]
            name = repo["name"]
            repo["readme"] = self.get_repo_readme(owner, name)
            # Calculate star velocity
            created = datetime.fromisoformat(repo["created_at"].replace("Z", "+00:00"))
            days_old = (datetime.now(created.tzinfo) - created).days or 1
            repo["star_velocity"] = repo["stargazers_count"] / days_old
        
        return repos[:limit]


class SimpleLabeler:
    """Simple labeler using heuristics (or LLM if available)."""
    
    def __init__(self, use_llm: bool = False):
        self.use_llm = use_llm and bool(LLM_API_KEY)
    
    def label_with_heuristics(self, repo: Dict) -> Dict:
        """Label repository using heuristics."""
        # Extract languages
        languages = repo.get("language") or "Unknown"
        all_languages = [languages] if languages else []
        
        # Extract topics
        topics = repo.get("topics", [])
        
        # Determine category from language/topics
        category = self._infer_category(languages, topics, repo.get("description", ""))
        
        # Generate tags
        tags = self._generate_tags(languages, topics, repo.get("description", ""))
        
        # Calculate health score
        health_score = self._calculate_health(repo)
        
        # Estimate skill level
        skill_level = self._estimate_skill_level(repo)
        
        return {
            "category": category,
            "tags": tags,
            "health_score": health_score,
            "skill_level": skill_level,
            "summary": repo.get("description", "No description available.")
        }
    
    def _infer_category(self, language: str, topics: List[str], description: str) -> str:
        """Infer category from language and topics."""
        text = f"{language} {' '.join(topics)} {description}".lower()
        
        categories = {
            "Machine Learning": ["ml", "machine learning", "ai", "neural", "tensorflow", "pytorch", "keras"],
            "Web Framework": ["web", "framework", "react", "vue", "angular", "django", "flask", "express"],
            "Developer Tools": ["tool", "cli", "dev", "utility", "library", "sdk"],
            "Data Science": ["data", "analysis", "pandas", "numpy", "jupyter", "notebook"],
            "Game Engine": ["game", "engine", "unity", "unreal", "gaming"],
            "Mobile": ["mobile", "ios", "android", "react native", "flutter"],
            "DevOps": ["devops", "docker", "kubernetes", "ci/cd", "deployment"],
            "Blockchain": ["blockchain", "crypto", "ethereum", "bitcoin", "web3"],
        }
        
        for cat, keywords in categories.items():
            if any(kw in text for kw in keywords):
                return cat
        
        return "Other"
    
    def _generate_tags(self, language: str, topics: List[str], description: str) -> List[str]:
        """Generate tags from repository data."""
        tags = set()
        
        # Add language
        if language:
            tags.add(language.lower())
        
        # Add topics
        tags.update([t.lower() for t in topics[:5]])
        
        # Extract keywords from description
        desc_lower = description.lower()
        common_keywords = ["api", "cli", "sdk", "library", "framework", "tool", "plugin", "extension"]
        for kw in common_keywords:
            if kw in desc_lower:
                tags.add(kw)
        
        return list(tags)[:10]  # Limit to 10 tags
    
    def _calculate_health(self, repo: Dict) -> float:
        """Calculate project health score (0.0-1.0)."""
        score = 0.0
        
        # Has description
        if repo.get("description"):
            score += 0.1
        
        # Has README
        if repo.get("readme"):
            score += 0.2
            readme_len = len(repo["readme"])
            if readme_len > 1000:
                score += 0.1
        
        # Recent activity
        updated = datetime.fromisoformat(repo["updated_at"].replace("Z", "+00:00"))
        days_since_update = (datetime.now(updated.tzinfo) - updated).days
        if days_since_update < 30:
            score += 0.2
        elif days_since_update < 90:
            score += 0.1
        
        # Has topics
        if repo.get("topics"):
            score += 0.1
        
        # Not archived
        if not repo.get("archived", False):
            score += 0.1
        
        # Has license
        if repo.get("license"):
            score += 0.1
        
        # Star velocity (normalized)
        star_velocity = repo.get("star_velocity", 0)
        if star_velocity > 10:
            score += 0.1
        
        return min(score, 1.0)
    
    def _estimate_skill_level(self, repo: Dict) -> str:
        """Estimate skill level."""
        stars = repo.get("stargazers_count", 0)
        forks = repo.get("forks_count", 0)
        
        if stars > 10000 or forks > 1000:
            return "expert"
        elif stars > 1000 or forks > 100:
            return "advanced"
        elif stars > 100 or forks > 10:
            return "intermediate"
        else:
            return "beginner"
    
    def label_with_llm(self, repo: Dict) -> Dict:
        """Label repository using LLM (OpenAI)."""
        if not LLM_API_KEY:
            return self.label_with_heuristics(repo)
        
        try:
            try:
                import openai
            except ImportError:
                print("OpenAI library not installed. Install with: pip install openai")
                return self.label_with_heuristics(repo)
            
            openai.api_key = LLM_API_KEY
            
            prompt = f"""Analyze this GitHub repository and provide labels:

Name: {repo['name']}
Description: {repo.get('description', 'N/A')}
Language: {repo.get('language', 'N/A')}
Topics: {', '.join(repo.get('topics', []))}
Stars: {repo.get('stargazers_count', 0)}
README (first 500 chars): {repo.get('readme', '')[:500]}

Provide JSON with:
- category: One primary category
- tags: Array of 5-10 tags
- health_score: 0.0-1.0
- skill_level: beginner/intermediate/advanced/expert
- summary: 2-3 sentence summary
"""
            
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.7
            )
            
            result = json.loads(response.choices[0].message.content)
            return result
        except Exception as e:
            print(f"LLM labeling failed: {e}, using heuristics")
            return self.label_with_heuristics(repo)
    
    def label(self, repo: Dict) -> Dict:
        """Label a repository."""
        if self.use_llm:
            return self.label_with_llm(repo)
        else:
            return self.label_with_heuristics(repo)


class SimpleSorter:
    """Simple sorter/ranker for repositories."""
    
    def __init__(self, weights: Optional[Dict[str, float]] = None):
        self.weights = weights or {
            "star_velocity": 0.35,
            "health": 0.25,
            "stars": 0.20,
            "recent_activity": 0.20,
        }
    
    def calculate_score(self, repo: Dict, labels: Dict) -> float:
        """Calculate total score for a repository."""
        # Normalize star velocity (assume max 100 stars/day)
        star_velocity_score = min(repo.get("star_velocity", 0) / 100.0, 1.0)
        
        # Health score from labels
        health_score = labels.get("health_score", 0.5)
        
        # Normalize stars (assume max 100k stars)
        stars_score = min(repo.get("stargazers_count", 0) / 100000.0, 1.0)
        
        # Recent activity score
        updated = datetime.fromisoformat(repo["updated_at"].replace("Z", "+00:00"))
        days_since_update = (datetime.now(updated.tzinfo) - updated).days
        activity_score = max(0, 1.0 - (days_since_update / 365.0))
        
        # Weighted sum
        total_score = (
            self.weights["star_velocity"] * star_velocity_score +
            self.weights["health"] * health_score +
            self.weights["stars"] * stars_score +
            self.weights["recent_activity"] * activity_score
        )
        
        return total_score
    
    def sort_repos(self, repos: List[Dict], labels: Dict[int, Dict]) -> List[Dict]:
        """Sort repositories by score."""
        scored_repos = []
        for repo in repos:
            repo_id = repo.get("id")
            repo_labels = labels.get(repo_id, {})
            score = self.calculate_score(repo, repo_labels)
            scored_repos.append({
                **repo,
                "labels": repo_labels,
                "score": score
            })
        
        # Sort by score (descending)
        scored_repos.sort(key=lambda x: x["score"], reverse=True)
        return scored_repos


def main():
    """Main function to scrape, label, and sort repositories."""
    print("=" * 60)
    print("GitHub Repository Scraper, Labeler, and Sorter")
    print("=" * 60)
    
    # Configuration
    query = input("Enter search query (e.g., 'language:python stars:>100'): ").strip() or "language:python stars:>100"
    limit = int(input("How many repos to scrape? (default 20): ").strip() or "20")
    use_llm = input("Use LLM for labeling? (y/n, default n): ").strip().lower() == "y"
    
    # 1. Scrape
    print("\n[1/3] Scraping repositories...")
    scraper = SimpleGitHubScraper()
    repos = scraper.scrape_repos(query, limit=limit)
    print(f"✓ Scraped {len(repos)} repositories")
    
    # 2. Label
    print("\n[2/3] Labeling repositories...")
    labeler = SimpleLabeler(use_llm=use_llm)
    labels = {}
    for repo in repos:
        repo_labels = labeler.label(repo)
        labels[repo["id"]] = repo_labels
        print(f"  ✓ {repo['name']}: {repo_labels['category']} - {', '.join(repo_labels['tags'][:3])}")
    
    # 3. Sort
    print("\n[3/3] Sorting repositories...")
    sorter = SimpleSorter()
    sorted_repos = sorter.sort_repos(repos, labels)
    print(f"✓ Sorted {len(sorted_repos)} repositories")
    
    # Display results
    print("\n" + "=" * 60)
    print("TOP 10 REPOSITORIES (by score)")
    print("=" * 60)
    
    for i, repo in enumerate(sorted_repos[:10], 1):
        print(f"\n{i}. {repo['full_name']}")
        print(f"   ⭐ {repo['stargazers_count']:,} stars | 🍴 {repo['forks_count']:,} forks")
        print(f"   📊 Score: {repo['score']:.3f}")
        print(f"   🏷️  Category: {repo['labels']['category']}")
        print(f"   🏷️  Tags: {', '.join(repo['labels']['tags'][:5])}")
        print(f"   💚 Health: {repo['labels']['health_score']:.2f} | Level: {repo['labels']['skill_level']}")
        print(f"   🔗 {repo['html_url']}")
    
    # Save to JSON
    output_file = "scraped_repos.json"
    with open(output_file, "w") as f:
        json.dump(sorted_repos, f, indent=2, default=str)
    print(f"\n✓ Results saved to {output_file}")
    
    # Statistics
    print("\n" + "=" * 60)
    print("STATISTICS")
    print("=" * 60)
    categories = Counter([r["labels"]["category"] for r in sorted_repos])
    print("\nCategories:")
    for cat, count in categories.most_common():
        print(f"  {cat}: {count}")
    
    all_tags = []
    for r in sorted_repos:
        all_tags.extend(r["labels"]["tags"])
    tag_counts = Counter(all_tags)
    print("\nTop Tags:")
    for tag, count in tag_counts.most_common(10):
        print(f"  {tag}: {count}")


if __name__ == "__main__":
    main()

