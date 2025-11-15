"""Job to update social signals for repositories."""

import sys
import os
from typing import List, Optional

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(base_dir)

from db.connection import SessionLocal
from db.models import Repo, SocialSignals

# Import social fetcher (handle hyphenated directory name)
import importlib.util
social_fetcher_path = os.path.join(base_dir, "social-signals-service", "social_fetcher.py")
spec = importlib.util.spec_from_file_location("social_fetcher", social_fetcher_path)
social_fetcher_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(social_fetcher_module)
SocialSignalsFetcher = social_fetcher_module.SocialSignalsFetcher


def update_social_signals(batch_size: int = 50, limit: Optional[int] = None):
    """Update social signals for repositories."""
    db = SessionLocal()
    fetcher = SocialSignalsFetcher()
    
    try:
        # Get repos without social signals or with old signals
        query = db.query(Repo).filter(Repo.archived == False)
        
        if limit:
            query = query.limit(limit)
        
        repos = query.all()
        
        print(f"Updating social signals for {len(repos)} repositories...")
        
        updated = 0
        for i, repo in enumerate(repos, 1):
            try:
                print(f"[{i}/{len(repos)}] Processing {repo.full_name}...")
                
                # Fetch social signals
                signals_data = fetcher.fetch_all_signals(
                    repo_name=repo.name,
                    repo_url=repo.url,
                    description=repo.description
                )
                
                # Update or create social signals record
                signals = db.query(SocialSignals).filter(
                    SocialSignals.repo_id == repo.id
                ).first()
                
                if signals:
                    # Update existing
                    signals.reddit_mentions = signals_data["reddit_mentions"]
                    signals.reddit_upvotes = signals_data["reddit_upvotes"]
                    signals.reddit_subreddits = signals_data["reddit_subreddits"]
                    signals.hn_mentions = signals_data["hn_mentions"]
                    signals.hn_points = signals_data["hn_points"]
                    signals.hn_comments = signals_data["hn_comments"]
                    signals.stackoverflow_questions = signals_data["stackoverflow_questions"]
                    signals.stackoverflow_views = signals_data["stackoverflow_views"]
                    signals.stackoverflow_score = signals_data["stackoverflow_score"]
                    signals.npm_weekly_downloads = signals_data["npm_weekly_downloads"]
                    signals.pypi_weekly_downloads = signals_data["pypi_weekly_downloads"]
                    signals.package_name = signals_data["package_name"]
                    signals.twitter_mentions = signals_data["twitter_mentions"]
                    signals.social_score = signals_data["social_score"]
                else:
                    # Create new
                    signals = SocialSignals(
                        repo_id=repo.id,
                        reddit_mentions=signals_data["reddit_mentions"],
                        reddit_upvotes=signals_data["reddit_upvotes"],
                        reddit_subreddits=signals_data["reddit_subreddits"],
                        hn_mentions=signals_data["hn_mentions"],
                        hn_points=signals_data["hn_points"],
                        hn_comments=signals_data["hn_comments"],
                        stackoverflow_questions=signals_data["stackoverflow_questions"],
                        stackoverflow_views=signals_data["stackoverflow_views"],
                        stackoverflow_score=signals_data["stackoverflow_score"],
                        npm_weekly_downloads=signals_data["npm_weekly_downloads"],
                        pypi_weekly_downloads=signals_data["pypi_weekly_downloads"],
                        package_name=signals_data["package_name"],
                        twitter_mentions=signals_data["twitter_mentions"],
                        social_score=signals_data["social_score"],
                    )
                    db.add(signals)
                
                updated += 1
                
                # Commit in batches
                if updated % batch_size == 0:
                    db.commit()
                    print(f"Committed {updated} updates...")
                
            except Exception as e:
                print(f"Error processing {repo.full_name}: {e}")
                db.rollback()
                continue
        
        # Final commit
        db.commit()
        print(f"Social signals update complete! Updated {updated} repositories.")
        
    except Exception as e:
        print(f"Error updating social signals: {e}")
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Update social signals for repositories")
    parser.add_argument("--batch-size", type=int, default=50, help="Batch size for commits")
    parser.add_argument("--limit", type=int, default=None, help="Limit number of repos to process")
    
    args = parser.parse_args()
    
    update_social_signals(batch_size=args.batch_size, limit=args.limit)

