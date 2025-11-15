"""Advanced labeling system for repositories using LLM and heuristics."""

import sys
import os
from typing import List, Dict, Any, Optional, Set
from datetime import datetime
import re

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from llm_service.llm_client import LLMClient
from db.models import Repo, RepoSummary


class RepoLabeler:
    """Advanced labeling system for repositories."""
    
    # Label categories
    PRIMARY_CATEGORIES = [
        "AI/ML", "Web Development", "Mobile", "DevOps", "Data Science",
        "Security", "Gaming", "Tools", "Education", "Design",
        "Blockchain", "IoT", "Scientific Computing", "System Programming",
        "Database", "API", "Framework", "Library", "CLI Tool"
    ]
    
    QUALITY_LABELS = {
        "star_quality": ["Exceptional", "High", "Good", "Standard", "Basic"],
        "documentation": ["Excellent", "Good", "Adequate", "Poor", "Missing"],
        "maintenance": ["Active", "Maintained", "Slow", "Abandoned", "Archived"],
        "use_case": ["Production-Ready", "Prototype", "Educational", "Research", "Experimental"],
        "recognition": ["GitHub Stars", "Industry Awards", "Featured", "Trending", "Hidden Gem"],
        "innovation": ["Groundbreaking", "Innovative", "Standard", "Derivative", "Outdated"]
    }
    
    def __init__(self, llm_client: Optional[LLMClient] = None):
        self.llm_client = llm_client or LLMClient()
    
    def extract_labels_from_llm(self, repo: Repo, summary: Optional[RepoSummary] = None) -> Dict[str, List[str]]:
        """Use LLM to extract comprehensive labels."""
        prompt = self._build_labeling_prompt(repo, summary)
        
        try:
            response = self.llm_client.generate(prompt, max_tokens=500)
            labels = self._parse_llm_response(response)
            return labels
        except Exception as e:
            print(f"Error extracting labels with LLM: {e}")
            return self._extract_labels_heuristic(repo, summary)
    
    def _build_labeling_prompt(self, repo: Repo, summary: Optional[RepoSummary] = None) -> str:
        """Build prompt for LLM labeling."""
        context = f"""
Repository: {repo.full_name}
Description: {repo.description or "N/A"}
Stars: {repo.stars}
Languages: {', '.join(repo.languages.keys()) if repo.languages else "N/A"}
Topics: {', '.join(repo.topics) if repo.topics else "N/A"}
"""
        
        if summary:
            context += f"""
Summary: {summary.summary}
Category: {summary.category}
Tags: {', '.join(summary.tags)}
"""
        
        prompt = f"""
Analyze this GitHub repository and assign comprehensive labels.

{context}

Assign labels in the following categories:

1. PRIMARY CATEGORY (choose 1-2 from): {', '.join(self.PRIMARY_CATEGORIES)}
2. QUALITY LABELS:
   - Star Quality: {', '.join(self.QUALITY_LABELS['star_quality'])}
   - Documentation: {', '.join(self.QUALITY_LABELS['documentation'])}
   - Maintenance: {', '.join(self.QUALITY_LABELS['maintenance'])}
   - Use Case: {', '.join(self.QUALITY_LABELS['use_case'])}
   - Recognition: {', '.join(self.QUALITY_LABELS['recognition'])}
   - Innovation: {', '.join(self.QUALITY_LABELS['innovation'])}

3. TECHNICAL LABELS:
   - Languages (list all)
   - Frameworks (if any)
   - Architecture patterns
   - Platform (Web, Desktop, Mobile, CLI, Library, API)

4. COMMUNITY LABELS:
   - Community Size (Large/Medium/Small/Niche)
   - Contributor Activity (Very Active/Active/Moderate/Low/Inactive)

5. DISCOVERY LABELS:
   - Hidden Gem (if high quality but low visibility)
   - Rising Star (if rapidly gaining traction)
   - Established (if long-standing)
   - Experimental (if cutting-edge)
   - Production-Tested (if used in production)
   - Educational (if great for learning)
   - Reference Implementation (if best practices example)

Return labels in JSON format:
{{
    "primary_category": ["category1", "category2"],
    "quality": {{
        "star_quality": "value",
        "documentation": "value",
        "maintenance": "value",
        "use_case": "value",
        "recognition": "value",
        "innovation": "value"
    }},
    "technical": {{
        "languages": ["lang1", "lang2"],
        "frameworks": ["framework1"],
        "architecture": ["pattern1"],
        "platform": ["platform1"]
    }},
    "community": {{
        "size": "value",
        "activity": "value"
    }},
    "discovery": ["label1", "label2"]
}}
"""
        return prompt
    
    def _parse_llm_response(self, response: str) -> Dict[str, Any]:
        """Parse LLM response into structured labels."""
        import json
        
        try:
            # Try to extract JSON from response
            json_match = re.search(r'\{.*\}', response, re.DOTALL)
            if json_match:
                labels = json.loads(json_match.group())
                return labels
        except:
            pass
        
        # Fallback: return empty structure
        return {
            "primary_category": [],
            "quality": {},
            "technical": {},
            "community": {},
            "discovery": []
        }
    
    def _extract_labels_heuristic(self, repo: Repo, summary: Optional[RepoSummary] = None) -> Dict[str, Any]:
        """Extract labels using heuristics when LLM is unavailable."""
        labels = {
            "primary_category": [],
            "quality": {},
            "technical": {},
            "community": {},
            "discovery": []
        }
        
        # Primary category from summary or topics
        if summary and summary.category:
            labels["primary_category"].append(summary.category)
        
        # Quality labels based on metrics
        labels["quality"]["star_quality"] = self._assess_star_quality(repo.stars)
        labels["quality"]["documentation"] = self._assess_documentation(repo.readme)
        labels["quality"]["maintenance"] = self._assess_maintenance(repo)
        labels["quality"]["use_case"] = self._assess_use_case(repo, summary)
        
        # Technical labels
        labels["technical"]["languages"] = list(repo.languages.keys()) if repo.languages else []
        labels["technical"]["platform"] = self._detect_platform(repo)
        
        # Community labels
        labels["community"]["size"] = self._assess_community_size(repo.stars)
        labels["community"]["activity"] = self._assess_activity(repo)
        
        # Discovery labels
        labels["discovery"] = self._detect_discovery_labels(repo, summary)
        
        return labels
    
    def _assess_star_quality(self, stars: int) -> str:
        """Assess star quality based on count."""
        if stars >= 10000:
            return "Exceptional"
        elif stars >= 1000:
            return "High"
        elif stars >= 100:
            return "Good"
        elif stars >= 10:
            return "Standard"
        else:
            return "Basic"
    
    def _assess_documentation(self, readme: Optional[str]) -> str:
        """Assess documentation quality."""
        if not readme:
            return "Missing"
        
        readme_lower = readme.lower()
        score = 0
        
        # Check for key sections
        if any(word in readme_lower for word in ["installation", "install", "setup"]):
            score += 1
        if any(word in readme_lower for word in ["usage", "example", "demo"]):
            score += 1
        if any(word in readme_lower for word in ["documentation", "docs", "api"]):
            score += 1
        if any(word in readme_lower for word in ["contributing", "contribute"]):
            score += 1
        if len(readme) > 1000:
            score += 1
        
        if score >= 4:
            return "Excellent"
        elif score >= 3:
            return "Good"
        elif score >= 2:
            return "Adequate"
        else:
            return "Poor"
    
    def _assess_maintenance(self, repo: Repo) -> str:
        """Assess maintenance status."""
        if repo.archived:
            return "Archived"
        
        if not repo.pushed_at:
            return "Abandoned"
        
        days_since_update = (datetime.now() - repo.pushed_at).days
        
        if days_since_update < 30:
            return "Active"
        elif days_since_update < 180:
            return "Maintained"
        elif days_since_update < 365:
            return "Slow"
        else:
            return "Abandoned"
    
    def _assess_use_case(self, repo: Repo, summary: Optional[RepoSummary] = None) -> str:
        """Assess use case."""
        if summary and summary.use_cases:
            if any("production" in uc.lower() for uc in summary.use_cases):
                return "Production-Ready"
            if any("learn" in uc.lower() or "tutorial" in uc.lower() for uc in summary.use_cases):
                return "Educational"
        
        # Heuristic: high stars + recent updates = production-ready
        if repo.stars > 1000 and repo.pushed_at:
            days_since = (datetime.now() - repo.pushed_at).days
            if days_since < 90:
                return "Production-Ready"
        
        return "Prototype"
    
    def _detect_platform(self, repo: Repo) -> List[str]:
        """Detect platform(s) from repo metadata."""
        platforms = []
        
        if not repo.description and not repo.topics:
            return platforms
        
        text = (repo.description or "").lower() + " " + " ".join(repo.topics).lower()
        
        if any(word in text for word in ["web", "website", "browser", "html", "css"]):
            platforms.append("Web")
        if any(word in text for word in ["mobile", "ios", "android", "react-native", "flutter"]):
            platforms.append("Mobile")
        if any(word in text for word in ["desktop", "gui", "electron", "qt"]):
            platforms.append("Desktop")
        if any(word in text for word in ["cli", "command-line", "terminal"]):
            platforms.append("CLI")
        if any(word in text for word in ["library", "sdk", "framework"]):
            platforms.append("Library")
        if any(word in text for word in ["api", "rest", "graphql", "server"]):
            platforms.append("API")
        
        return platforms if platforms else ["Library"]
    
    def _assess_community_size(self, stars: int) -> str:
        """Assess community size."""
        if stars >= 10000:
            return "Large"
        elif stars >= 1000:
            return "Medium"
        elif stars >= 100:
            return "Small"
        else:
            return "Niche"
    
    def _assess_activity(self, repo: Repo) -> str:
        """Assess contributor activity."""
        if not repo.pushed_at:
            return "Inactive"
        
        days_since = (datetime.now() - repo.pushed_at).days
        
        if days_since < 7:
            return "Very Active"
        elif days_since < 30:
            return "Active"
        elif days_since < 90:
            return "Moderate"
        elif days_since < 180:
            return "Low"
        else:
            return "Inactive"
    
    def _detect_discovery_labels(self, repo: Repo, summary: Optional[RepoSummary] = None) -> List[str]:
        """Detect discovery labels (hidden gems, rising stars, etc.)."""
        labels = []
        
        # Hidden Gem: High quality but low visibility
        if repo.stars < 500 and summary and summary.project_health_score > 0.7:
            labels.append("Hidden Gem")
        
        # Rising Star: Fast star velocity
        if repo.star_velocity > 10:
            labels.append("Rising Star")
        
        # Established: Old and still active
        if repo.created_at:
            age_years = (datetime.now() - repo.created_at).days / 365
            if age_years > 3 and repo.pushed_at:
                days_since = (datetime.now() - repo.pushed_at).days
                if days_since < 90:
                    labels.append("Established")
        
        # Experimental: Very new
        if repo.created_at:
            age_days = (datetime.now() - repo.created_at).days
            if age_days < 90:
                labels.append("Experimental")
        
        # Educational: Good documentation and examples
        if repo.readme and len(repo.readme) > 2000:
            readme_lower = repo.readme.lower()
            if any(word in readme_lower for word in ["tutorial", "example", "guide", "learn"]):
                labels.append("Educational")
        
        return labels
    
    def label_repo(self, repo: Repo, summary: Optional[RepoSummary] = None, use_llm: bool = True) -> Dict[str, Any]:
        """Label a repository comprehensively."""
        if use_llm:
            labels = self.extract_labels_from_llm(repo, summary)
        else:
            labels = self._extract_labels_heuristic(repo, summary)
        
        return labels

