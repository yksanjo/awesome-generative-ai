"""Comprehensive curation job that fetches, labels, and scores repositories."""

import sys
import os
from typing import List, Optional
from datetime import datetime

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from db.connection import get_db, init_db
from db.models import Repo, RepoLabel, RepoInsight, RepoSummary
from ingestion_service.ingester import RepoIngester
from ingestion_service.advanced_fetcher import AdvancedRepoFetcher
from llm_service.labeler import RepoLabeler
from curation_engine.insightfulness_scorer import InsightfulnessScorer
from curation_engine.ranker import RepoRanker
from shared.config import settings


class ComprehensiveCurator:
    """Comprehensive curation pipeline."""
    
    def __init__(self):
        self.ingester = RepoIngester()
        self.fetcher = AdvancedRepoFetcher()
        self.labeler = RepoLabeler()
        self.insightfulness_scorer = InsightfulnessScorer()
        self.ranker = RepoRanker()
    
    def run_comprehensive_curation(
        self,
        languages: Optional[List[str]] = None,
        topics: Optional[List[str]] = None,
        per_category_limit: int = 50,
        use_llm_labeling: bool = True
    ):
        """Run the complete curation pipeline."""
        print("=" * 80)
        print("COMPREHENSIVE REPOSITORY CURATION PIPELINE")
        print("=" * 80)
        
        # Step 1: Fetch repositories
        print("\n[1/5] Fetching repositories...")
        repos_data = self.fetcher.comprehensive_fetch(
            languages=languages,
            topics=topics,
            per_category_limit=per_category_limit
        )
        print(f"Fetched {len(repos_data)} repository metadata entries")
        
        # Step 2: Ingest repositories
        print("\n[2/5] Ingesting repositories into database...")
        ingested_repos = []
        for i, repo_data in enumerate(repos_data, 1):
            try:
                metadata = self.ingester.github_client.fetch_repo_metadata(repo_data)
                
                with get_db() as db:
                    existing = db.query(Repo).filter(Repo.url == str(metadata.url)).first()
                    
                    if existing:
                        # Update existing
                        for key, value in metadata.dict(exclude={"id", "created_at_db", "updated_at_db"}).items():
                            setattr(existing, key, value)
                        existing.updated_at_db = datetime.utcnow()
                        db.commit()
                        ingested_repos.append(existing)
                    else:
                        # Create new
                        repo = Repo(**metadata.dict(exclude={"id", "created_at_db", "updated_at_db"}))
                        db.add(repo)
                        db.commit()
                        db.refresh(repo)
                        ingested_repos.append(repo)
                
                if i % 10 == 0:
                    print(f"  Ingested {i}/{len(repos_data)} repos...")
            except Exception as e:
                print(f"  Error ingesting {repo_data.get('full_name', 'unknown')}: {e}")
                continue
        
        print(f"Ingested {len(ingested_repos)} repositories")
        
        # Step 3: Generate summaries (if not exists)
        print("\n[3/5] Generating summaries for repositories...")
        from llm_service.summarizer import RepoSummarizer
        summarizer = RepoSummarizer()
        
        repos_to_summarize = []
        with get_db() as db:
            for repo in ingested_repos:
                summary = db.query(RepoSummary).filter(RepoSummary.repo_id == repo.id).first()
                if not summary:
                    repos_to_summarize.append(repo)
        
        print(f"Found {len(repos_to_summarize)} repos without summaries")
        for i, repo in enumerate(repos_to_summarize, 1):
            try:
                summarizer.summarize_repo(repo.id)
                if i % 5 == 0:
                    print(f"  Summarized {i}/{len(repos_to_summarize)} repos...")
            except Exception as e:
                print(f"  Error summarizing repo {repo.id}: {e}")
                continue
        
        # Step 4: Label repositories
        print("\n[4/5] Labeling repositories...")
        labeled_count = 0
        with get_db() as db:
            for repo in ingested_repos:
                try:
                    summary = db.query(RepoSummary).filter(RepoSummary.repo_id == repo.id).first()
                    
                    # Get labels
                    labels = self.labeler.label_repo(repo, summary, use_llm=use_llm_labeling)
                    
                    # Clear existing labels for this repo
                    db.query(RepoLabel).filter(RepoLabel.repo_id == repo.id).delete()
                    
                    # Store labels
                    for label_type, label_data in labels.items():
                        if label_type == "primary_category":
                            for category in label_data:
                                label = RepoLabel(
                                    repo_id=repo.id,
                                    label_type="category",
                                    label_value=category,
                                    confidence=0.8,
                                    source="llm" if use_llm_labeling else "heuristic"
                                )
                                db.add(label)
                        elif label_type == "quality" and isinstance(label_data, dict):
                            for quality_type, value in label_data.items():
                                if value:
                                    label = RepoLabel(
                                        repo_id=repo.id,
                                        label_type=f"quality_{quality_type}",
                                        label_value=str(value),
                                        confidence=0.7,
                                        source="llm" if use_llm_labeling else "heuristic"
                                    )
                                    db.add(label)
                        elif label_type == "technical" and isinstance(label_data, dict):
                            for tech_type, values in label_data.items():
                                if isinstance(values, list):
                                    for value in values:
                                        label = RepoLabel(
                                            repo_id=repo.id,
                                            label_type=f"technical_{tech_type}",
                                            label_value=str(value),
                                            confidence=0.8,
                                            source="llm" if use_llm_labeling else "heuristic"
                                        )
                                        db.add(label)
                        elif label_type == "community" and isinstance(label_data, dict):
                            for comm_type, value in label_data.items():
                                if value:
                                    label = RepoLabel(
                                        repo_id=repo.id,
                                        label_type=f"community_{comm_type}",
                                        label_value=str(value),
                                        confidence=0.7,
                                        source="llm" if use_llm_labeling else "heuristic"
                                    )
                                    db.add(label)
                        elif label_type == "discovery" and isinstance(label_data, list):
                            for discovery_label in label_data:
                                label = RepoLabel(
                                    repo_id=repo.id,
                                    label_type="discovery",
                                    label_value=discovery_label,
                                    confidence=0.6,
                                    source="llm" if use_llm_labeling else "heuristic"
                                )
                                db.add(label)
                    
                    db.commit()
                    labeled_count += 1
                    
                    if labeled_count % 10 == 0:
                        print(f"  Labeled {labeled_count}/{len(ingested_repos)} repos...")
                except Exception as e:
                    print(f"  Error labeling repo {repo.id}: {e}")
                    db.rollback()
                    continue
        
        print(f"Labeled {labeled_count} repositories")
        
        # Step 5: Calculate insightfulness and curation scores
        print("\n[5/5] Calculating insightfulness and curation scores...")
        scored_count = 0
        with get_db() as db:
            for repo in ingested_repos:
                try:
                    summary = db.query(RepoSummary).filter(RepoSummary.repo_id == repo.id).first()
                    
                    # Calculate insightfulness
                    insight_scores = self.insightfulness_scorer.calculate_insightfulness(repo, summary)
                    
                    # Store insightfulness
                    existing_insight = db.query(RepoInsight).filter(RepoInsight.repo_id == repo.id).first()
                    if existing_insight:
                        for key, value in insight_scores.items():
                            if hasattr(existing_insight, key):
                                setattr(existing_insight, key, value)
                        existing_insight.computed_at = datetime.utcnow()
                    else:
                        insight = RepoInsight(
                            repo_id=repo.id,
                            innovation_score=insight_scores["innovation"],
                            best_practices_score=insight_scores["best_practices"],
                            educational_value=insight_scores["educational_value"],
                            production_use_score=insight_scores["production_use"],
                            community_impact=insight_scores["community_impact"],
                            technical_depth=insight_scores["technical_depth"],
                            total_insightfulness=insight_scores["total_insightfulness"]
                        )
                        db.add(insight)
                    
                    db.commit()
                    scored_count += 1
                    
                    if scored_count % 10 == 0:
                        print(f"  Scored {scored_count}/{len(ingested_repos)} repos...")
                except Exception as e:
                    print(f"  Error scoring repo {repo.id}: {e}")
                    db.rollback()
                    continue
        
        print(f"Scored {scored_count} repositories")
        
        # Step 6: Rank all repositories
        print("\n[6/6] Ranking all repositories...")
        scores = self.ranker.rank_repos()
        print(f"Ranked {len(scores)} repositories")
        
        print("\n" + "=" * 80)
        print("CURATION PIPELINE COMPLETE")
        print("=" * 80)
        print(f"\nSummary:")
        print(f"  - Fetched: {len(repos_data)} repos")
        print(f"  - Ingested: {len(ingested_repos)} repos")
        print(f"  - Labeled: {labeled_count} repos")
        print(f"  - Scored: {scored_count} repos")
        print(f"  - Ranked: {len(scores)} repos")
        
        # Show top repos
        print(f"\nTop 10 Repositories by Curation Score:")
        for i, score in enumerate(scores[:10], 1):
            with get_db() as db:
                repo = db.query(Repo).filter(Repo.id == score.repo_id).first()
                if repo:
                    print(f"  {i}. {repo.full_name} - Score: {score.total_score:.3f} ⭐ {repo.stars}")


def main():
    """Main entry point."""
    print("Initializing database...")
    init_db()
    
    curator = ComprehensiveCurator()
    
    # Run comprehensive curation
    curator.run_comprehensive_curation(
        languages=["python", "javascript", "go", "rust"],  # Top languages
        topics=["machine-learning", "web-development", "devops"],  # Popular topics
        per_category_limit=30,  # Adjust based on rate limits
        use_llm_labeling=True  # Set to False to use heuristics only
    )


if __name__ == "__main__":
    main()

