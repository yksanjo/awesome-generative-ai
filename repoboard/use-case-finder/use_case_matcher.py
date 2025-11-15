"""Use-case finder: matches user queries with repositories using LLM."""

import sys
import os
import json
from typing import List, Dict, Any, Optional

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from llm_service.llm_client import LLMClient
from db.connection import SessionLocal
from db.models import Repo, RepoSummary
from sqlalchemy.orm import Session


class UseCaseFinder:
    """Finds repositories matching user use cases using LLM."""
    
    USE_CASE_PROMPT = """You are a Python library recommendation expert. A user wants to: "{user_query}"

Given the following Python repositories, recommend the best ones for this use case. Consider:
1. How well the repository matches the use case
2. Library maturity and maintenance status
3. Documentation quality
4. Community support
5. Ease of use

Repository candidates:
{repo_list}

Return a JSON response with this structure:
{{
    "recommendations": [
        {{
            "repo_id": <id>,
            "match_score": <0-100>,
            "reason": "<why this is a good match>",
            "pros": ["<advantage1>", "<advantage2>"],
            "cons": ["<limitation1>", "<limitation2>"],
            "alternatives": ["<alternative_lib1>", "<alternative_lib2>"]
        }}
    ],
    "use_case_category": "<category like 'web-api', 'data-processing', 'ml', etc>",
    "recommended_stack": ["<lib1>", "<lib2>", "<lib3>"],
    "getting_started_tip": "<brief tip on how to get started>"
}}

Only include repositories with match_score >= 50. Sort by match_score descending."""

    def __init__(self):
        self.llm_client = LLMClient()
    
    def find_repos_for_use_case(
        self, 
        user_query: str, 
        language: Optional[str] = "python",
        limit: int = 10,
        db: Optional[Session] = None
    ) -> Dict[str, Any]:
        """Find repositories matching a user's use case."""
        
        # Get candidate repositories
        if db is None:
            db = SessionLocal()
            should_close = True
        else:
            should_close = False
        
        try:
            # Filter by language if specified
            query = db.query(Repo).filter(Repo.archived == False)
            
            if language:
                # Filter repos that use this language
                # Languages is stored as JSON dict, so we check if language key exists
                if language.lower() == "python":
                    # For Python, also check if it's in topics or description
                    query = query.filter(
                        (Repo.languages.has_key("Python")) |
                        (Repo.description.ilike(f"%{language}%")) |
                        (Repo.topics.contains([language.lower()]))
                    )
            
            # Get repos with summaries (better for matching)
            repos = query.join(RepoSummary).limit(50).all()
            
            if not repos:
                return {
                    "recommendations": [],
                    "use_case_category": "unknown",
                    "recommended_stack": [],
                    "getting_started_tip": "No repositories found matching your criteria."
                }
            
            # Prepare repo list for LLM
            repo_list = []
            for repo in repos:
                summary = repo.summary
                repo_info = {
                    "id": repo.id,
                    "name": repo.name,
                    "full_name": repo.full_name,
                    "description": repo.description or "",
                    "summary": summary.summary if summary else "",
                    "tags": summary.tags if summary else [],
                    "category": summary.category if summary else "Other",
                    "stars": repo.stars,
                    "project_health": summary.project_health if summary else "unknown",
                    "use_cases": summary.use_cases if summary else []
                }
                repo_list.append(repo_info)
            
            # Format repo list for prompt
            repo_list_str = json.dumps(repo_list, indent=2)
            
            # Call LLM
            prompt = self.USE_CASE_PROMPT.format(
                user_query=user_query,
                repo_list=repo_list_str
            )
            
            system_prompt = "You are an expert Python developer who recommends the best libraries for specific use cases. Be practical and consider real-world usage."
            
            try:
                response = self.llm_client._call_llm(prompt, system_prompt)
                
                # Parse JSON response
                response = response.strip()
                if response.startswith("```json"):
                    response = response[7:]
                if response.startswith("```"):
                    response = response[3:]
                if response.endswith("```"):
                    response = response[:-3]
                response = response.strip()
                
                result = json.loads(response)
                
                # Enrich with full repo data
                enriched_recommendations = []
                for rec in result.get("recommendations", [])[:limit]:
                    repo_id = rec.get("repo_id")
                    repo = next((r for r in repos if r.id == repo_id), None)
                    if repo:
                        enriched_rec = {
                            **rec,
                            "repo": {
                                "id": repo.id,
                                "name": repo.name,
                                "full_name": repo.full_name,
                                "url": repo.url,
                                "description": repo.description,
                                "stars": repo.stars,
                                "forks": repo.forks,
                                "topics": repo.topics,
                                "languages": repo.languages,
                            }
                        }
                        enriched_recommendations.append(enriched_rec)
                
                result["recommendations"] = enriched_recommendations
                return result
                
            except Exception as e:
                print(f"Error in use-case matching: {e}")
                # Fallback: return top repos by stars
                return {
                    "recommendations": [
                        {
                            "repo_id": repo.id,
                            "match_score": 60,
                            "reason": "Popular repository that might match your needs",
                            "pros": ["Well-maintained", "Popular"],
                            "cons": [],
                            "alternatives": [],
                            "repo": {
                                "id": repo.id,
                                "name": repo.name,
                                "full_name": repo.full_name,
                                "url": repo.url,
                                "description": repo.description,
                                "stars": repo.stars,
                            }
                        }
                        for repo in repos[:limit]
                    ],
                    "use_case_category": "general",
                    "recommended_stack": [],
                    "getting_started_tip": "Check the repository README for getting started instructions."
                }
        finally:
            if should_close:
                db.close()
    
    def find_similar_use_cases(self, repo_id: int, db: Optional[Session] = None) -> List[str]:
        """Find similar use cases for a given repository."""
        if db is None:
            db = SessionLocal()
            should_close = True
        else:
            should_close = False
        
        try:
            repo = db.query(Repo).filter(Repo.id == repo_id).first()
            if not repo or not repo.summary:
                return []
            
            # Return use cases from summary
            return repo.summary.use_cases or []
        finally:
            if should_close:
                db.close()

