"""Calculate insightfulness scores for repositories."""

import sys
import os
from typing import Dict, Any, Optional
from datetime import datetime
import re

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from db.models import Repo, RepoSummary


class InsightfulnessScorer:
    """Calculate how insightful/notable a repository is."""
    
    def __init__(self):
        # Weights for different insightfulness factors
        self.weights = {
            "innovation": 0.25,
            "best_practices": 0.20,
            "educational_value": 0.20,
            "production_use": 0.15,
            "community_impact": 0.10,
            "technical_depth": 0.10
        }
    
    def calculate_insightfulness(self, repo: Repo, summary: Optional[RepoSummary] = None) -> Dict[str, float]:
        """Calculate comprehensive insightfulness scores."""
        scores = {
            "innovation": self._score_innovation(repo, summary),
            "best_practices": self._score_best_practices(repo, summary),
            "educational_value": self._score_educational_value(repo, summary),
            "production_use": self._score_production_use(repo, summary),
            "community_impact": self._score_community_impact(repo),
            "technical_depth": self._score_technical_depth(repo, summary)
        }
        
        # Calculate weighted total
        total = sum(
            self.weights[factor] * score
            for factor, score in scores.items()
        )
        scores["total_insightfulness"] = total
        
        return scores
    
    def _score_innovation(self, repo: Repo, summary: Optional[RepoSummary] = None) -> float:
        """Score how innovative/novel the repository is."""
        score = 0.0
        
        # Check description and topics for innovation indicators
        text = (repo.description or "").lower()
        if repo.topics:
            text += " " + " ".join(repo.topics).lower()
        
        innovation_keywords = [
            "novel", "innovative", "breakthrough", "revolutionary",
            "cutting-edge", "state-of-the-art", "sota", "new approach",
            "first", "pioneering", "groundbreaking", "unique"
        ]
        
        for keyword in innovation_keywords:
            if keyword in text:
                score += 0.1
        
        # High star velocity suggests innovation
        if repo.star_velocity > 20:
            score += 0.3
        elif repo.star_velocity > 10:
            score += 0.2
        elif repo.star_velocity > 5:
            score += 0.1
        
        # Recent creation with high stars suggests innovation
        if repo.created_at:
            age_days = (datetime.now() - repo.created_at).days
            if age_days < 180 and repo.stars > 500:
                score += 0.2
            elif age_days < 365 and repo.stars > 1000:
                score += 0.1
        
        # Summary-based assessment
        if summary:
            if "innovative" in summary.summary.lower() or "novel" in summary.summary.lower():
                score += 0.2
        
        return min(score, 1.0)
    
    def _score_best_practices(self, repo: Repo, summary: Optional[RepoSummary] = None) -> float:
        """Score if repo demonstrates best practices."""
        score = 0.0
        
        # Check README for best practices indicators
        if repo.readme:
            readme_lower = repo.readme.lower()
            
            # Documentation quality
            if "documentation" in readme_lower or "docs" in readme_lower:
                score += 0.1
            
            # Testing
            if any(word in readme_lower for word in ["test", "testing", "ci", "travis", "github actions"]):
                score += 0.15
            
            # Code quality indicators
            if any(word in readme_lower for word in ["lint", "format", "code quality", "style guide"]):
                score += 0.1
            
            # Contributing guidelines
            if "contributing" in readme_lower or "contribute" in readme_lower:
                score += 0.1
            
            # License
            if repo.license:
                score += 0.05
            
            # Examples and demos
            if any(word in readme_lower for word in ["example", "demo", "usage", "quick start"]):
                score += 0.1
        
        # File tree indicators
        if repo.file_tree:
            tree_str = str(repo.file_tree).lower()
            
            # Has tests
            if "test" in tree_str or "spec" in tree_str:
                score += 0.1
            
            # Has CI/CD
            if ".github" in tree_str or "ci" in tree_str:
                score += 0.1
            
            # Has documentation
            if "docs" in tree_str or "documentation" in tree_str:
                score += 0.05
        
        # High stars with good maintenance suggests best practices
        if repo.stars > 1000 and repo.pushed_at:
            days_since = (datetime.now() - repo.pushed_at).days
            if days_since < 90:
                score += 0.15
        
        return min(score, 1.0)
    
    def _score_educational_value(self, repo: Repo, summary: Optional[RepoSummary] = None) -> float:
        """Score educational value."""
        score = 0.0
        
        if not repo.readme:
            return score
        
        readme_lower = repo.readme.lower()
        
        # Educational keywords
        educational_keywords = [
            "tutorial", "guide", "learn", "learning", "example",
            "demo", "walkthrough", "getting started", "beginner",
            "educational", "teaching", "course", "lesson"
        ]
        
        for keyword in educational_keywords:
            if keyword in readme_lower:
                score += 0.1
        
        # Comprehensive documentation
        if len(repo.readme) > 3000:
            score += 0.2
        elif len(repo.readme) > 1500:
            score += 0.1
        
        # Examples in file tree
        if repo.file_tree:
            tree_str = str(repo.file_tree).lower()
            if "example" in tree_str or "demo" in tree_str or "sample" in tree_str:
                score += 0.2
        
        # Summary mentions educational value
        if summary:
            if any(word in summary.summary.lower() for word in ["learn", "tutorial", "educational", "guide"]):
                score += 0.2
        
        # Topics indicate educational content
        if repo.topics:
            if any(topic in ["education", "tutorial", "learning", "examples"] for topic in repo.topics):
                score += 0.2
        
        return min(score, 1.0)
    
    def _score_production_use(self, repo: Repo, summary: Optional[RepoSummary] = None) -> float:
        """Score indicators of production use."""
        score = 0.0
        
        # High stars often indicate production use
        if repo.stars > 10000:
            score += 0.4
        elif repo.stars > 5000:
            score += 0.3
        elif repo.stars > 1000:
            score += 0.2
        elif repo.stars > 500:
            score += 0.1
        
        # Active maintenance suggests production use
        if repo.pushed_at:
            days_since = (datetime.now() - repo.pushed_at).days
            if days_since < 30:
                score += 0.2
            elif days_since < 90:
                score += 0.1
        
        # Multiple contributors
        if repo.contributor_count > 10:
            score += 0.1
        elif repo.contributor_count > 5:
            score += 0.05
        
        # README mentions production use
        if repo.readme:
            readme_lower = repo.readme.lower()
            if any(phrase in readme_lower for phrase in [
                "production", "used by", "adopted", "deployed",
                "in production", "production-ready"
            ]):
                score += 0.2
        
        # Summary mentions production
        if summary:
            if summary.use_cases:
                if any("production" in uc.lower() for uc in summary.use_cases):
                    score += 0.2
        
        return min(score, 1.0)
    
    def _score_community_impact(self, repo: Repo) -> float:
        """Score community impact and influence."""
        score = 0.0
        
        # Forks indicate community engagement
        if repo.forks > 1000:
            score += 0.3
        elif repo.forks > 500:
            score += 0.2
        elif repo.forks > 100:
            score += 0.1
        
        # Stars indicate community recognition
        if repo.stars > 10000:
            score += 0.3
        elif repo.stars > 5000:
            score += 0.2
        elif repo.stars > 1000:
            score += 0.1
        
        # Watchers indicate active interest
        if repo.watchers > 500:
            score += 0.1
        elif repo.watchers > 100:
            score += 0.05
        
        # High fork-to-star ratio suggests utility
        if repo.stars > 0:
            fork_ratio = repo.forks / repo.stars
            if fork_ratio > 0.3:  # High fork ratio
                score += 0.2
            elif fork_ratio > 0.2:
                score += 0.1
        
        # Topics suggest community categorization
        if repo.topics and len(repo.topics) > 5:
            score += 0.1
        
        return min(score, 1.0)
    
    def _score_technical_depth(self, repo: Repo, summary: Optional[RepoSummary] = None) -> float:
        """Score technical depth and sophistication."""
        score = 0.0
        
        # Multiple languages suggest complexity
        if repo.languages and len(repo.languages) > 3:
            score += 0.1
        
        # Large file tree suggests substantial codebase
        if repo.file_tree:
            tree_str = str(repo.file_tree)
            # Rough estimate of file count
            file_count = tree_str.count("type")
            if file_count > 100:
                score += 0.2
            elif file_count > 50:
                score += 0.1
        
        # Summary mentions technical depth
        if summary:
            depth_keywords = [
                "advanced", "complex", "sophisticated", "deep",
                "comprehensive", "detailed", "thorough"
            ]
            if any(keyword in summary.summary.lower() for keyword in depth_keywords):
                score += 0.2
            
            # High skill level suggests depth
            if summary.skill_level_numeric >= 8:
                score += 0.3
            elif summary.skill_level_numeric >= 6:
                score += 0.2
            elif summary.skill_level_numeric >= 4:
                score += 0.1
        
        # README length suggests depth
        if repo.readme:
            if len(repo.readme) > 5000:
                score += 0.2
            elif len(repo.readme) > 2000:
                score += 0.1
        
        # Topics suggest technical focus
        technical_topics = [
            "algorithm", "data-structure", "optimization", "performance",
            "architecture", "system", "engine", "framework"
        ]
        if repo.topics:
            if any(topic in technical_topics for topic in repo.topics):
                score += 0.1
        
        return min(score, 1.0)

